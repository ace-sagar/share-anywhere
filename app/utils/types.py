from enum import Enum
from pydantic import BaseModel
from typing import Optional

class ResourceRequest(BaseModel):
    owner_id: int
    recipient_id: int
    file_path: str
    storage_provider: str
    permission: str

class StatusDetail(BaseModel):
    status_code: int
    detail: str
    headers: Optional[dict]

class ResourceResponse(BaseModel):
    status: StatusDetail
    message: str

class Message(Enum):
    PERMISSION_DENIED = "Permission Denied: You are not the owner of the file"
    SHARED_SUCCESS = "File Shared Successfully"
    NOT_FOUND = "File not found"
    DENIED_ACTION = "Permission Denied: You do not have the required permissions to perform this action"
    ERROR = "An error occurred"