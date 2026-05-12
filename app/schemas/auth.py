from pydantic import BaseModel, EmailStr, Field


class RegisterUser(BaseModel):
    email : EmailStr
    password: str = Field(min_length=2, max_length=20)

class LoginUser(BaseModel):
    email : EmailStr
    password : str = Field(min_length=2, max_length=20)

class RefreshTokenRequest(BaseModel):
    refresh_token: str