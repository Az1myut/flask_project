from repository_db import Repository
from entity import User, Product
from pymongo import MongoClient

#Verbindung zur Datenbank
username = "abc22222"
password = username + "_secret"
auth_source = username
host = "im-vm-005"
port = 27017

client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}")
db = client[f"{auth_source}"]

#Erzeugen der Repo-Objekte
user_repo = Repository[User](db["users"], User, primary_key="username")
product_repo = Repository[Product](db["products"], Product, primary_key="product_id")

#Nutzung der Repos
products = product_repo.find({ "price" : { "$gt" : 80} })
print(products)
