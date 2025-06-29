from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config 
from enum import Enum
from datetime import datetime,date
from typing import List, Optional
from bson import ObjectId
from marshmallow_enum import EnumField
class Role(Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"

@dataclass_json
@dataclass
class Adress:  
    street: str
    postal_code: str
    country: str
    house_number : int
    id : Optional[ObjectId] = None

@dataclass_json
@dataclass
class User:    
    
    username: str
    password: str
    profile_id : ObjectId #Id von Profile
    date_time_registration : datetime = field(default_factory=datetime.now)
    date_time_last_login : Optional[datetime] = None

   
   
@dataclass_json
@dataclass
class Profile:
    favorite_movies :List[ObjectId] #Liste von Movie_ids
    comments : List[ObjectId]       #Liste von coment_ids
    role: str = Role.USER.value
    email : Optional[str] = None
    mobile_number : Optional[str] = None
    id : Optional[ObjectId] = None 
    adress : Optional[ObjectId] = None #Id von Adress wo User wohnt
    




@dataclass_json
@dataclass
class Genre:      
    name : str
    related_movies : List[ObjectId] #Liste von movie_ids
    id : Optional[ObjectId] = None 
    
    

@dataclass_json
@dataclass
class Movie:
    title: str
    description: str
    runtime_in_minutes: int
    released_in: datetime
    rating : float 
    image_url: str
    genres : List[ObjectId]   
    comments: List[ObjectId] = field(default_factory=list)
    id : Optional[ObjectId] = None 
    
@dataclass_json
@dataclass
class Like:
    movie_id: ObjectId
    user_profile_id : ObjectId
    id : Optional[ObjectId] = None 
    

@dataclass_json
@dataclass
class Comment:        
    content: str
    author_id: ObjectId #id von zugehoerigen User, der kommentriert hat
    movie_id: ObjectId #id von zugehoerigen Article
    author_name : str
    created_at: datetime
    id : Optional[ObjectId] = None
    



   