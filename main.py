from utility_classes import AddressBook, Record
from mock import mock


def parse_input(input: str):
    command, *args = input.split(" ")
    return (command, *args)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper

@input_error
def add(name: str, phone: str, book: AddressBook):
    if not all((name, phone)):
        raise ValueError("Missing required argements: add <name> <phone>")
    record = Record(name).add_phone(phone)
    book.add_record(record)

@input_error
def change(name: str, phone: str, changed_phone: str, book: AddressBook):
    if not all((name, phone)):
        raise ValueError("Missing required argements: change <name> <phone>")
    record = book.find(name)
    record.edit_phone(phone, changed_phone)

@input_error
def show_phone(name: str, book: AddressBook):
    if not all((name)):
        raise ValueError("Missing required argement: phone <name>")
    record = book.find(name)
    print(record)

@input_error
def add_birthday(name: str, birthday: str, book: AddressBook):
    if not all((name, birthday)):
        raise ValueError("Missing required argements: add-birthday <name> <birthday>")
    record = book.find(name)
    record.add_birthday(birthday)

@input_error
def show_birthday(name: str, book: AddressBook):
    record = book.find(name)
    bd = record.birthday
    if bd:
        print(f"{name}'s birthday is {bd}")
    else:
        answer = input(f"Would you like to set {name}'s birthday?(y/n): ")
        if answer.lower() == "y":
            bd = input(f"Enter birthday in DD.MM.YYYY format: ")
            record.add_birthday(bd)
            print(f"{name}'s birthday set to {record.birthday}")

@input_error
def birthdays(book: AddressBook):
    bd_list = book.get_upcoming_birthdays()
    for bd in bd_list:
        print(bd)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            add(*args, book)

        elif command == "change":
            change(*args, book)

        elif command == "phone":
            show_phone(*args, book)

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            add_birthday(*args, book)

        elif command == "show-birthday":
            show_birthday(*args, book)

        elif command == "birthdays":
            bd_list = book.get_upcoming_birthdays()
            for i in bd_list:
                print(i)
        elif command == "fill":
            
            for i in mock():
                r = Record(i["name"])
                if i.get("birthday"):
                    r.add_birthday(i["birthday"])
                for phone in i["phones"]:
                    r.add_phone(phone)
                book.add_record(r)
        else:
            print("Invalid command.")


main()