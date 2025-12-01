from pydantic import BaseModel
from typing import Optional

# Esquemas para Usuario
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

# Esquemas para Departamento
class DepartmentCreate(BaseModel):
    name: str
    location: str

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    location: str
    is_active: bool

    class Config:
        from_attributes = True