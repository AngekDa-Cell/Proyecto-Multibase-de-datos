from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

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

# Esquemas para Contact
class ContactCreate(BaseModel):
    name: str
    phone: str

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class ContactResponse(BaseModel):
    id: str
    name: str
    phone: str
    is_deleted: bool

# Esquemas para Event
class EventCreate(BaseModel):
    title: str
    date: datetime
    description: Optional[str] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None

class EventResponse(BaseModel):
    id: str
    title: str
    date: datetime
    description: str
    is_deleted: bool

# Esquemas para AppConfig
class AppConfigCreate(BaseModel):
    key: str
    data: Dict[str, Any]

class AppConfigUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None

class AppConfigResponse(BaseModel):
    key: str
    data: Dict[str, Any]
    active: bool

# Esquemas para UserSession
class UserSessionCreate(BaseModel):
    user_id: str
    session_data: Dict[str, Any]

class UserSessionUpdate(BaseModel):
    session_data: Optional[Dict[str, Any]] = None

class UserSessionResponse(BaseModel):
    user_id: str
    session_data: Dict[str, Any]
    active: bool

# Esquemas para Role
class RoleCreate(BaseModel):
    name: str
    description: str

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool

    class Config:
        from_attributes = True