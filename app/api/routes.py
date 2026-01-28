from typing import Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import get_store

router = APIRouter()

class PutRequest(BaseModel):
    key: str
    value: Any
    ttl: Optional[float] = None

@router.put("/kv/insert")
def put_key(request: PutRequest):
    store = get_store()
    store.put(request.key, request.value, request.ttl)
    return {"status": "success"}

@router.get("/kv/{key}")
def get_key(key: str):
    store = get_store()
    value = store.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

@router.delete("/kv/{key}")
def delete_key(key: str):
    store = get_store()
    store.delete(key)
    return {"status": "success"}