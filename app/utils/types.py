from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Request(BaseModel):
    owner_email: str
    recipient_email: str
    file_name: str
    container: Optional[str]
    bucket_name: str 
    provider: str
    permission: str

class StatusDetail(BaseModel):
    status_code: int
    detail: str
    headers: Optional[dict]

class Response(BaseModel):
    status: StatusDetail
    message: str
class Message(Enum):
    PERMISSION_DENIED = "Permission Denied: You are not the owner of the file"
    SHARED_SUCCESS = "File Shared Successfully"
    NOT_FOUND = "File not found"
    DENIED_ACTION = "Permission Denied: You do not have the required permissions to perform this action"
    ERROR = "An error occurred"
    FILE_ALREADY_SHARED = "File already shared"