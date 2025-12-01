from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.postgres import get_db
from ..models import User, Department, Role
from ..schemas import (
    UserCreate, UserUpdate, UserResponse,
    DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    RoleCreate, RoleUpdate, RoleResponse
)

router = APIRouter()

# Usuarios endpoints
@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_active == True).all()
    return users

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_active = False
    db.commit()
    return {"message": "User deleted"}

# Departmamentos endpoints
@router.get("/departments", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).filter(Department.is_active == True).all()
    return departments

@router.post("/departments", response_model=DepartmentResponse)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    db_dept = Department(**dept.dict())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.patch("/departments/{dept_id}", response_model=DepartmentResponse)
def update_department(dept_id: int, dept_update: DepartmentUpdate, db: Session = Depends(get_db)):
    db_dept = db.query(Department).filter(Department.id == dept_id, Department.is_active == True).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    update_data = dept_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dept, key, value)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.delete("/departments/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    db_dept = db.query(Department).filter(Department.id == dept_id, Department.is_active == True).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db_dept.is_active = False
    db.commit()
    return {"message": "Department deleted"}

# Roles endpoints
@router.get("/roles", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).filter(Role.is_active == True).all()
    return roles

@router.post("/roles", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.patch("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id, Role.is_active == True).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    update_data = role_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id, Role.is_active == True).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db_role.is_active = False
    db.commit()
    return {"message": "Role deleted"}