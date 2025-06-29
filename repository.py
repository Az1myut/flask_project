

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from bson import ObjectId
from nanoid import generate
import time
import random
from icecream import ic


T = TypeVar("T")

def fix_id(doc: dict) -> dict:

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

  
        if(primary_key != "_id"):
            self.collection.create_index([(self.primary_key, 1)], unique=True)

    def save(self, obj: T) -> Any:

        doc = obj.to_dict()
       
       
        if self.primary_key != '_id':
            primary_key_value = doc.get(self.primary_key)
            existing = self.collection.find_one({self.primary_key: primary_key_value})
            if not existing:
                self.collection.insert_one(doc)
            else:
                self.collection.replace_one(
                {self.primary_key: doc[self.primary_key]},
                doc) 
               
                 
                
            return primary_key_value
        
        
        object_id = doc.get('id')
        if object_id is None:
           
            object_id = ObjectId()
            setattr(obj, 'id', object_id)
         
    
        doc = obj.to_dict()
  

        db_doc = doc.copy()
   
        db_doc['_id'] = object_id


        
        self.collection.replace_one(
            {'_id': object_id},
            db_doc,
            upsert=True
        )
        return object_id

    def find_by_id(self, id_value: Any) -> Optional[T]:
      
        doc = self.collection.find_one({self.primary_key: id_value})
      
        if doc:
           
            return self.model_cls.from_dict(fix_id(doc))
        return None


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

