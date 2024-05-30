from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.services.PresignedURLManager import PresignedURLManager
from app.services.ResourceManager import ResourceManager
from app.utils.types import Message, Request, Response

from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()  # Load environment variables from .env file

@router.get("/access/{user_token}", tags=["Resource"])
async def access_file(user_token: str):
    if not user_token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    resourceManager = ResourceManager()
    resourceManager.connect()
    isValidToken = resourceManager.is_valid_token(user_token)

    if isValidToken:
        file_name = resourceManager.get_resource_details(user_token)
        resourceManager.close()
        
        ########## Presigned URL Operations ##########
        presignedURLManager = PresignedURLManager()
        presigned_url = presignedURLManager.generate_presigned_url(file_name[0])

        return RedirectResponse(url=presigned_url)
    else:
        raise HTTPException(status_code=403, detail=Message.DENIED_ACTION.value)

@router.post("/access/", response_model=Response, tags=["Resource"])
async def share(resource: Request):

    ########## Request Payload ##########
    owner_email = resource.owner_email
    recipient_email = resource.recipient_email
    file_name = resource.file_name
    container = resource.container
    bucket_name = resource.bucket_name
    provider = resource.provider
    permission = resource.permission

    ########## Share Resource Operations ##########
    resourceManager = ResourceManager()
    resourceManager.connect()

    result = resourceManager.grant_access(
        owner_email, recipient_email, file_name, container, bucket_name, provider, permission
    )

    return_response = {}
    if result[0] == Message.ALREADY_SHARED.value or result[0] == Message.ERROR.value or result[0] == Message.PERMISSION_UPDATED.value:
        return_response = {
            "status": HTTPException(status_code=200),
            "message": result[0]
        }
    else:
        host = os.getenv("HOST")
        url = f"{host}access/{result[1]}"

        # Send this to Recipient Email address
        print('URL: ', url)

        return_response = {
            "status": HTTPException(status_code=200),
            "message": result[0]
        }

    resourceManager.close()

    return return_response

@router.patch('/access/', response_model=Response)
async def update_access():
    pass

@router.delete('/access/{user_token}', response_model=Response)
async def remove_access(user_token: str):
    ########## Share Resource Operations ##########
    resourceManager = ResourceManager()
    resourceManager.connect()

    result = resourceManager.remove_access(user_token)

    resourceManager.close()

    return {
        "status": HTTPException(status_code=200),
        "message": result
    }

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="My API",
        swagger_favicon_url="https://example.com/favicon.ico",
    )
