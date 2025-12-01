from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['agenda_db']

# Colecciones
contacts_collection = db['contacts']

# Helper para formatear ID de Mongo
def contact_helper(contact) -> dict:
    return {
        "id": str(contact["_id"]),
        "name": contact["name"],
        "phone": contact["phone"],
        "is_deleted": contact.get("is_deleted", False)
    }