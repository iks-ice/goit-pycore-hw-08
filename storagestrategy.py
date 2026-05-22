from abc import ABC, abstractmethod
import json

class StorageStrategy(ABC):
    @abstractmethod
    def save(self, data: dict) -> None:
        """Метод для збереження даних книги"""
        pass

    @abstractmethod
    def search(self, query: str) -> dict:
        """Повертає словник {name: Record} зі знайденими контактами"""
        pass

class FileStorage(StorageStrategy):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, data: dict) -> None:
        # Перетворюємо об'єкти Record у простий словник для JSON
        serialized = {k: {"name": v.name, "phone": v.phone} for k, v in data.items()}
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(serialized, f, ensure_ascii=False, indent=4)
        print(f" Дані успішно збережено у файл {self.filename}")

    def search(self, query: str) -> dict:
        # Для файлу простіше прочитати його (або шукати в пам'яті AddressBook)
        print(f"Шукаємо '{query}' у файлі {self.filename}...")
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Фільтруємо збіги по імені або телефону
                return {k: v for k, v in data.items() if query.lower() in k.lower() or query in v['phone']}
        except FileNotFoundError:
            return {}