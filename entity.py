from dataclasses import dataclass
from dataclasses_json import dataclass_json #, DataClassJsonMixin
from enum import Enum

class Size(Enum):
    S = 1
    M = 2
    L = 3

@dataclass_json
@dataclass
class User:           #class User(DataClassJsonMixin):    <-- damit werden die Methoden to_json() und from_json() auch in PyCharm angezeigt; funktioniert aber auch so zur Laufzeit
    username: str
    password: str

@dataclass_json
@dataclass
class Product:        # class Product(DataClassJsonMixin):    <-- damit werden die Methoden to_json() und from_json() auch in PyCharm angezeigt; funktioniert aber auch so zur Laufzeit
    product_id: int
    title: str
    description: str
    price: float
    pic_urls: list[str]
    is_sale: bool
    #sizes: list[Size]

