from fastapi import APIRouter, HTTPException
# from fastapi.responses import JSONResponse

from app.services.ResourceManager import ResourceManage
from app.utils.types import ResourceRequest, ResourceResponse

router = APIRouter()

@router.get("/share/{user_id}")
async def get_resource(user_id: int):

    ########## Share Resource Operations ##########
    resourceManager = ResourceManage("file_sharing.db")
    resourceManager.connect()

    # Get all the records from the permission table with user_id
    result = resourceManager.getUserFiles(user_id)

    resourceManager.close()

    return {
        "result": result
    }

@router.post("/share/", response_model=ResourceResponse)
async def post_resource(resource: ResourceRequest):
    owner_id = resource.owner_id
    recipient_id = resource.recipient_id
    file_id = resource.file_id
    permission = resource.permission

    ########## Share Resource Operations ##########
    resourceManager = ResourceManage("file_sharing.db")
    resourceManager.connect()

    # Check if file info is already present in the database
    file_id = resourceManager.get_file_id(file_id, owner_id, remote_path = "", generated_path = "")

    # Share file with another user
    result = resourceManager.share_file(file_id, owner_id, recipient_id, permission)
    resourceManager.close()

    return {
        "status": HTTPException(status_code=200),
        "message": result
    }