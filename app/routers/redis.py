import json
from fastapi import APIRouter, HTTPException
from ..database.redis import redis_client
from ..schemas import (
    AppConfigCreate, AppConfigUpdate, AppConfigResponse,
    UserSessionCreate, UserSessionUpdate, UserSessionResponse
)

router = APIRouter()

# AppConfig endpoints
@router.get("/config/{key}", response_model=AppConfigResponse)
def get_config(key: str):
    val = redis_client.get(f"config:{key}")
    if not val:
        raise HTTPException(status_code=404, detail="Config not found")
    data = json.loads(val)
    if not data.get("active", False):
        raise HTTPException(status_code=404, detail="Config is deleted")
    return {"key": key, "data": data["data"], "active": data["active"]}

@router.post("/config", response_model=AppConfigResponse)
def create_config(config: AppConfigCreate):
    key = f"config:{config.key}"
    if redis_client.exists(key):
        raise HTTPException(status_code=400, detail="Config already exists")
    data = {"data": config.data, "active": True}
    redis_client.set(key, json.dumps(data))
    return {"key": config.key, "data": config.data, "active": True}

@router.patch("/config/{key}", response_model=AppConfigResponse)
def update_config(key: str, config_update: AppConfigUpdate):
    redis_key = f"config:{key}"
    val = redis_client.get(redis_key)
    if not val:
        raise HTTPException(status_code=404, detail="Config not found")
    data = json.loads(val)
    if not data.get("active", False):
        raise HTTPException(status_code=404, detail="Config is deleted")
    if config_update.data is not None:
        data["data"].update(config_update.data)
    redis_client.set(redis_key, json.dumps(data))
    return {"key": key, "data": data["data"], "active": data["active"]}

@router.delete("/config/{key}")
def delete_config(key: str):
    redis_key = f"config:{key}"
    val = redis_client.get(redis_key)
    if not val:
        raise HTTPException(status_code=404, detail="Config not found")
    data = json.loads(val)
    data["active"] = False
    redis_client.set(redis_key, json.dumps(data))
    return {"message": "Config deleted"}

# UserSessions endpoints
@router.get("/sessions/{user_id}", response_model=UserSessionResponse)
def get_session(user_id: str):
    val = redis_client.get(f"session:{user_id}")
    if not val:
        raise HTTPException(status_code=404, detail="Session not found")
    data = json.loads(val)
    if not data.get("active", False):
        raise HTTPException(status_code=404, detail="Session is deleted")
    return {"user_id": user_id, "session_data": data["session_data"], "active": data["active"]}

@router.post("/sessions", response_model=UserSessionResponse)
def create_session(session: UserSessionCreate):
    key = f"session:{session.user_id}"
    if redis_client.exists(key):
        raise HTTPException(status_code=400, detail="Session already exists")
    data = {"session_data": session.session_data, "active": True}
    redis_client.set(key, json.dumps(data))
    return {"user_id": session.user_id, "session_data": session.session_data, "active": True}

@router.patch("/sessions/{user_id}", response_model=UserSessionResponse)
def update_session(user_id: str, session_update: UserSessionUpdate):
    redis_key = f"session:{user_id}"
    val = redis_client.get(redis_key)
    if not val:
        raise HTTPException(status_code=404, detail="Session not found")
    data = json.loads(val)
    if not data.get("active", False):
        raise HTTPException(status_code=404, detail="Session is deleted")
    if session_update.session_data is not None:
        data["session_data"].update(session_update.session_data)
    redis_client.set(redis_key, json.dumps(data))
    return {"user_id": user_id, "session_data": data["session_data"], "active": data["active"]}

@router.delete("/sessions/{user_id}")
def delete_session(user_id: str):
    redis_key = f"session:{user_id}"
    val = redis_client.get(redis_key)
    if not val:
        raise HTTPException(status_code=404, detail="Session not found")
    data = json.loads(val)
    data["active"] = False
    redis_client.set(redis_key, json.dumps(data))
    return {"message": "Session deleted"}