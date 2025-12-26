from pydantic import BaseModel
from typing import Any, Dict

class TaskResponse(BaseModel):
    task_id: str

class StatusResponse(BaseModel):
    state: str
    meta: Dict[str, Any] | None
