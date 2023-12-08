from pydantic import BaseModel,validator,Field
from typing import Optional

class UserData(BaseModel):
    username:str
    email:str
    password:str =Field(min_length=8,max_length=32)

    @validator('email')
    def email_validation(value):
        if '@' not in value or '.com' not in value:
            raise ValueError('Provide a valid email address')
        return value
    
class LoginData(BaseModel):
    email:str
    

    @validator('email')
    def email_validation(value):
        if '@' not in value or '.com' not in value:
            raise ValueError('Provide a valid email address')
        return value
    
class Edit(BaseModel):
    role:str
    description:Optional[str]
    location:Optional[str]
    company:Optional[str]
    requirements:Optional[str]
    posted:Optional[str]


    

