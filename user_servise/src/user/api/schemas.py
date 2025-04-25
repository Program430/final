from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional

class UserCreateSchema(BaseModel):
    login: str = Field(min_length=4, max_length=100, examples=["user123"])
    name: str = Field(min_length=4, max_length=100, examples=["John Doe"])
    mail: EmailStr = Field(min_length=6, max_length=255, examples=["user@example.com"])
    password: str = Field(min_length=6, max_length=128, examples=["secure123"])
    password_2: str = Field(min_length=6, max_length=128, examples=["secure123"])

    command_code: Optional[str] = Field(None, examples=["qwertyuiop"])

    @model_validator(mode='after')
    def validate_passwords_match(self):
        if self.password != self.password_2:
            raise ValueError('Passwords do not match')
        return self
    
class UserLoginSchema(BaseModel):
    login: str = Field(min_length=4, max_length=100, examples=["user123"])
    password: str = Field(min_length=6, max_length=128, examples=["secure123"])

class UserUpdateSchema(BaseModel):
    id: int
    login: str = Field(min_length=4, max_length=100, examples=["user123"])
    name: str = Field(min_length=4, max_length=100, examples=["John Doe"])
    mail: EmailStr = Field(min_length=6, max_length=255, examples=["user@example.com"])
    password: str = Field(min_length=6, max_length=128, examples=["secure123"])
 