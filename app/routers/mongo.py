from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..database.mongo import contacts_collection, events_collection, contact_helper, event_helper
from ..schemas import (
    ContactCreate, ContactUpdate, ContactResponse,
    EventCreate, EventUpdate, EventResponse
)

router = APIRouter()

# Contacts endpoints
@router.get("/contacts", response_model=list[ContactResponse])
def get_contacts():
    contacts = []
    for contact in contacts_collection.find({"is_deleted": {"$ne": True}}):
        contacts.append(contact_helper(contact))
    return contacts

@router.post("/contacts", response_model=ContactResponse)
def create_contact(contact: ContactCreate):
    new_contact = {"name": contact.name, "phone": contact.phone, "is_deleted": False}
    result = contacts_collection.insert_one(new_contact)
    new_contact["_id"] = result.inserted_id
    return contact_helper(new_contact)

@router.patch("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: str, contact_update: ContactUpdate):
    update_data = contact_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = contacts_collection.update_one(
        {"_id": ObjectId(contact_id), "is_deleted": {"$ne": True}},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    updated_contact = contacts_collection.find_one({"_id": ObjectId(contact_id)})
    return contact_helper(updated_contact)

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str):
    result = contacts_collection.update_one(
        {"_id": ObjectId(contact_id)},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}

# Events endpoints
@router.get("/events", response_model=list[EventResponse])
def get_events():
    events = []
    for event in events_collection.find({"is_deleted": {"$ne": True}}):
        events.append(event_helper(event))
    return events

@router.post("/events", response_model=EventResponse)
def create_event(event: EventCreate):
    new_event = {
        "title": event.title,
        "date": event.date,
        "description": event.description or "",
        "is_deleted": False
    }
    result = events_collection.insert_one(new_event)
    new_event["_id"] = result.inserted_id
    return event_helper(new_event)

@router.patch("/events/{event_id}", response_model=EventResponse)
def update_event(event_id: str, event_update: EventUpdate):
    update_data = event_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = events_collection.update_one(
        {"_id": ObjectId(event_id), "is_deleted": {"$ne": True}},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    updated_event = events_collection.find_one({"_id": ObjectId(event_id)})
    return event_helper(updated_event)

@router.delete("/events/{event_id}")
def delete_event(event_id: str):
    result = events_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}