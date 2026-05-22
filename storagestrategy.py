from abc import ABC, abstractmethod
import pickle

class StorageStrategy(ABC):
    @abstractmethod
    def save(self, data: dict) -> None:
        """Метод для збереження даних книги"""
        pass

    @abstractmethod
    def load(self):
        """Повертає словник {name: Record} зі знайденими контактами"""
        pass

class FileStorage(StorageStrategy):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, data) -> None:
        with open(self.filename, 'wb') as f:
            pickle.dump(data, f)
        print(f"Дані успішно збережено у файл {self.filename}")

    def load(self):
        # Для файлу простіше прочитати його (або шукати в пам'яті AddressBook)
        print(f"Шукаємо у файлі {self.filename}...")
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}