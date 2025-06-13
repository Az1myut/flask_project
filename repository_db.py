"""
# Beispiel-Dataclass mit username als Primärschlüssel
@dataclass_json
@dataclass
class User:
    username: str
    password: str


username = "xyz00000"
password = username + "_secret"
auth_source = username
host = "im-vm-005"
port = 27017

client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}")
db = client[f"{auth_source}"]

user_repo = Repository[User](db["users"], User, primary_key="username")
product_repo = Repository[Product](db["products"], Product, primary_key="product_id")

user = User("brigitte", "secret")
product = Product(Repository.random_int(), "Jeans", "Super Hose", 99.90, ["http://one", "http://two"], False)

product_repo.save(product)
print("product saved")

#user_repo.save(user)
#print("user saved")

#user = user_repo.find_by_id("brigitte")
#print("found:")
#print(user)

all = product_repo.find_all()
print(all)

page_3 = product_repo.find_all(skip=20, limit=10)
print("Einträge 21 bis 30 -- die ersten 20 auslassen dann die nächsten 10 anzeigen")
print(page_3)


client.close()
"""

# Credit to ChatGPT :-)
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from bson import ObjectId
from nanoid import generate
import time
import random

T = TypeVar("T")

def fix_id(doc: dict) -> dict:
    """Konvertiert ObjectId in string im _id Feld, falls vorhanden."""
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

class Repository(Generic[T]):
    @staticmethod
    def random_string(length: int = None) -> str:
        if length is None:
            return generate()
        else:
            return generate(size=length)
    @staticmethod
    def random_int():
        t = int(time.time() * 1000)
        r = random.randint(0, 999)
        return int(str(t)[-6:] + f"{r:03d}")

    def __init__(self, collection: Collection, model_cls: Type[T], primary_key: str = "_id"):
        self.collection = collection
        self.model_cls = model_cls
        self.primary_key = primary_key

        # Erstelle Unique Index auf primären Schlüssel
        self.collection.create_index(self.primary_key, unique=True)

    def save(self, obj: T) -> Any:
        doc = obj.to_dict()
        key_value = doc.get(self.primary_key)
        if key_value is None:
            raise ValueError(f"Primärschlüssel-Feld '{self.primary_key}' darf nicht leer sein.")

        # Upsert: Ersetze bestehendes Dokument oder füge neu ein
        self.collection.replace_one(
            {self.primary_key: key_value},
            doc,
            upsert=True
        )
        return key_value

    def find_by_id(self, id_value: Any) -> Optional[T]:
        doc = self.collection.find_one({self.primary_key: id_value})
        if doc:
            return self.model_cls.from_dict(fix_id(doc))
        return None

    #def find(self, query: Dict[str, Any]) -> List[T]:
    #    return [self.model_cls.from_dict(fix_id(doc)) for doc in self.collection.find(query)]

    def find(self, query: Dict[str, Any], skip: int = 0, limit: int = 0) -> List[T]:
        cursor = self.collection.find(query).skip(skip)
        if limit > 0:
            cursor = cursor.limit(limit)
        return [self.model_cls.from_dict(fix_id(doc)) for doc in cursor]

    def find_all(self, skip: int = 0, limit: int = 0) -> List[T]:
        cursor = self.collection.find().skip(skip)
        if limit > 0:
            cursor = cursor.limit(limit)
        return [self.model_cls.from_dict(fix_id(doc)) for doc in cursor]

    def update_by_id(self, id_value: Any, update_fields: Dict[str, Any]) -> bool:
        result = self.collection.update_one(
            {self.primary_key: id_value},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def delete_by_id(self, id_value: Any) -> bool:
        result = self.collection.delete_one({self.primary_key: id_value})
        return result.deleted_count > 0

