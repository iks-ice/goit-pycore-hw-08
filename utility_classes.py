from datetime import date, timedelta
from re import sub
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __format__(self, format_spec):
        return format(self.value, format_spec)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    # реалізація класу
	def __init__(self, phone):
            pattern = r"[^0-9]+"
            only_digits = sub(pattern,"", phone)

            if len(only_digits) != 10:
                raise ValueError("Incorrect phone number format")
            
            super().__init__(phone)

class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"
    def __init__(self, value):
        try:
            self.value = date.strptime(value, Birthday.DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def _format_date(self, date: date):
        return date.strftime(Birthday.DATE_FORMAT)
    
    def __str__(self):
        return f"{self._format_date(self.value)}"
    
class ContactCongratulation(Birthday):
    def __init__(self, value, name):
        super().__init__(value)
        self.name = name

    def __str__(self):
        return f"On {self.value} congratulate {self.name} "

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __find_phone_index(self, phone):
        try:
            return [obj.value for obj in self.phones].index(phone)
        except ValueError:
            print(f"{phone} not found in the record")

    def add_phone(self, phone) -> Record:
        self.phones.append(Phone(phone))
        return self

    def remove_phone(self, phone) -> Record:
        index = self.__find_phone_index(phone)
        self.phones.pop(index)
        return self

    def edit_phone(self, phone, change_phone) -> Record:
        index = self.__find_phone_index(phone)
        self.phones[index] = Phone(change_phone)
        return self

    def find_phone(self, phone) -> Record:
        index = self.__find_phone_index(phone)
        return self.phones[index]
    
    def add_birthday(self, value) -> Record:
        self.birthday = Birthday(value)
        return self

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict[str, Record]):

    def add_record(self, record: Record):
        if not isinstance(record, Record):
            raise TypeError("Objects of only Record class can be saved")
        
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        if name not in self.data:
            raise ValueError("Record not found")
        return self.data[name]
    
    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, from_date = None) -> list[ContactCongratulation]:

        weekdays = (5, 6)
        
        today_date = date.today()

        if from_date is not None:
            today_date = date.strptime(from_date, Birthday.DATE_FORMAT)
        
        current_year = today_date.year

        bd_list = []

        for name, record in self.data.items():
            if record.birthday is None:
                continue

            birth_date = record.birthday.value

            congrats_date = birth_date.replace(year = current_year)

            if congrats_date < today_date:
                congrats_date = congrats_date.replace(year = current_year + 1)

            days_left = (congrats_date - today_date).days
            
            if -1 < days_left < 8:

                weekday = congrats_date.weekday()

                if weekday in weekdays:
                    congrats_date = congrats_date + timedelta(days = 7 - weekday)

                bd_list.append(ContactCongratulation(congrats_date.strftime(Birthday.DATE_FORMAT), name))    

        return bd_list

    def __str__(self):
        s = ""
        header = f"Name         Birthday     Phones\n"
        for name, record in self.data.items():
            s += f"{name:<12} {str(record.birthday):<12} {'; '.join(p.value for p in record.phones)}\n"
        return header + s.strip()