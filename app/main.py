from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json

# Importaciones locales
from db_postgres import get_db, UserDB
from db_mongo import contacts_collection, contact_helper
from db_redis import redis_client
from bson import ObjectId

app = FastAPI(title="Agenda Multibase API")

# --- MODELOS PYDANTIC (Para validar entrada de datos) ---
class UserCreate(BaseModel):
    name: str
    email: str

class ContactCreate(BaseModel):
    name: str
    phone: str

class ConfigCreate(BaseModel):
    key: str
    value: str

# ==========================================
# 1. POSTGRESQL (Recurso: Users)
# ==========================================

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    # Solo traer los que is_active = True
    return db.query(UserDB).filter(UserDB.is_active == True).all()

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(name=user.name, email=user.email, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # BORRADO LÓGICO
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False # Marcamos como borrado
    db.commit()
    return {"message": "User logically deleted"}

# ==========================================
# 2. MONGODB (Recurso: Contacts)
# ==========================================

@app.get("/contacts/")
def get_contacts():
    # Filtrar donde is_deleted sea False o no exista
    contacts = []
    for contact in contacts_collection.find({"is_deleted": {"$ne": True}}):
        contacts.append(contact_helper(contact))
    return contacts

@app.post("/contacts/")
def create_contact(contact: ContactCreate):
    new_contact = {"name": contact.name, "phone": contact.phone, "is_deleted": False}
    result = contacts_collection.insert_one(new_contact)
    return {"id": str(result.inserted_id), **new_contact}

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str):
    # BORRADO LÓGICO: Update set is_deleted = true
    result = contacts_collection.update_one(
        {"_id": ObjectId(contact_id)},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact logically deleted"}

# ==========================================
# 3. REDIS (Recurso: Config/Settings)
# ==========================================
# Estrategia Redis: Usaremos un Hash llamado "app_config"
# Borrado Lógico en Redis: Agregaremos un campo "deleted:key" o moveremos a otra key.
# Simulación: El valor JSON tendrá un campo "active": true/false

@app.get("/config/{key}")
def get_config(key: str):
    val = redis_client.hget("app_configs", key)
    if not val:
        raise HTTPException(status_code=404, detail="Config not found")
    
    data = json.loads(val)
    if not data.get("active"):
         raise HTTPException(status_code=404, detail="Config is deleted")
    return data

@app.post("/config/")
def create_config(config: ConfigCreate):
    data = {"value": config.value, "active": True}
    redis_client.hset("app_configs", config.key, json.dumps(data))
    return {"message": "Config set"}

@app.delete("/config/{key}")
def delete_config(key: str):
    # BORRADO LÓGICO EN REDIS
    val = redis_client.hget("app_configs", key)
    if not val:
        raise HTTPException(status_code=404, detail="Config not found")
    
    data = json.loads(val)
    data["active"] = False # Marcamos como inactivo
    
    redis_client.hset("app_configs", key, json.dumps(data))
    return {"message": "Config logically deleted"}