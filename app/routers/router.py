from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.services.EmailManager import EmailManager
from app.services.PresignedURLManager import PresignedURLManager
from app.services.ResourceManager import ResourceManager
from app.utils.types import Message, ResourceRequest, ResourceResponse

from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

@router.get("/access-file/{email}/{user_token}", tags=["Resource"])
async def access_file(email: str, user_token: str):
    if not user_token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    ########## Get User Details ##########
    resourceManager = ResourceManager(db_name=os.getenv("DATABASE_NAME"))
    isValidToken = resourceManager.is_token_already_exists(email, user_token)

    if not isValidToken:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    ########## Presigned URL Operations ##########
    presignedURLManager = PresignedURLManager()
    

    presigned_url = presignedURLManager.generate_presigned_url()
    return RedirectResponse(url=presigned_url)

@router.post("/share/", response_model=ResourceResponse, tags=["Resource"])
async def share(resource: ResourceRequest):

    ########## Request Payload ##########
    owner_id = resource.owner_id
    recipient_id = resource.recipient_id
    file_id = resource.file_id
    permission = resource.permission
    email = resource.email

    ########## Share Resource Operations ##########
    resourceManager = ResourceManager(db_name=os.getenv("DATABASE_NAME"))
    resourceManager.connect()

    file_id = resourceManager.get_file_id(file_id, owner_id, remote_path = "", generated_path = "") # Check if file info is already present in the database

    result = resourceManager.share_file(file_id, owner_id, recipient_id, permission) # Share file with another user

    return_response = {}

    if result == Message.PERMISSION_DENIED.value or result == Message.FILE_ALREADY_SHARED.value:
        return_response = {
            "status": HTTPException(status_code=200),
            "message": result
        }
    else:
        host = 'http://127.0.0.1:8000/'
        token = resourceManager.generate_token()
        resourceManager.store_token(email, token)
        url = f"{host}access-file/{email}/{token}"

        return_response = {
            "status": HTTPException(status_code=200),
            "message": result,
            "url": url,
        }

    resourceManager.close()

    ########## Email Operations ##########
    # emailManager = EmailManager()
    # email_body = f"Hello User,\n\nYou can access your file using the following link:\n\n{url}\n\nBest regards,\nUser"
    # emailManager.send_email(email, "File Shared", email_body)

    return return_response

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="My API",
        swagger_favicon_url="https://example.com/favicon.ico",
    )