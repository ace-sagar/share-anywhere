from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Message(Enum):
    SHARED = "Resource shared successfully"
    ALREADY_SHARED = "Resource already shared"
    PERMISSION_REMOVED="Resource access removed successfully"
    PERMISSION_UPDATED="Resource access updated successfully"
    NOT_FOUND = "Resource not found"
    TOKEN_NOT_FOUND = "Token not found"
    DENIED_ACTION = "You do not have the required permissions to perform this action or your token not found"
    ERROR = "An error occurred"

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