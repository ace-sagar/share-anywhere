from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
# from fastapi.responses import JSONResponse

from app.services.EmailManager import EmailManager
from app.services.PresignedURLManager import PresignedURLManager
from app.services.ResourceManager import ResourceManager
from app.utils.types import Message, ResourceRequest, ResourceResponse

router = APIRouter()

@router.get("/access-file/{email}/{user_token}")
async def access_file(email: str, user_token: str):
    if not user_token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    db_name = "file_sharing.db"
    
    ########## Get User Details ##########
    resourceManager = ResourceManager(db_name)
    isValidToken = resourceManager.is_token_already_exists(email, user_token)

    ########## Presigned URL Operations ##########
    presignedURLManager = PresignedURLManager()
    
    if not isValidToken:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    presigned_url = presignedURLManager.generate_presigned_url()
    return RedirectResponse(url=presigned_url)

@router.post("/share/", response_model=ResourceResponse)
async def share(resource: ResourceRequest):
    db_name = "file_sharing.db"

    ########## Request Payload ##########
    owner_id = resource.owner_id
    recipient_id = resource.recipient_id
    file_id = resource.file_id
    permission = resource.permission
    email = resource.email

    ########## Share Resource Operations ##########
    resourceManager = ResourceManager(db_name)
    resourceManager.connect()

    file_id = resourceManager.get_file_id(file_id, owner_id, remote_path = "", generated_path = "") # Check if file info is already present in the database

    result = resourceManager.share_file(file_id, owner_id, recipient_id, permission) # Share file with another user

    url = None
    if not result == Message.FILE_ALREADY_SHARED.value:
        host = 'http://127.0.0.1:8000/'
        token = resourceManager.generate_token()
        resourceManager.store_token(email, token)
        url = f"{host}access-file/{email}/{token}"
    
    resourceManager.close()

    ########## Email Operations ##########
    # emailManager = EmailManager()
    # email_body = f"Hello User,\n\nYou can access your file using the following link:\n\n{url}\n\nBest regards,\nUser"
    # emailManager.send_email(email, "File Shared", email_body)

    return {
        "status": HTTPException(status_code=200),
        "message": result,
        "url": url
    }