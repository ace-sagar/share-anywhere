# # from typing import Union
# from fastapi import FastAPI

# # from share.ShareResource import ShareResource
# from .routers import router

# # Fast API instance
# app = FastAPI()

# # Include the router
# app.include_router(router)

# # Model
# # class ShareResourceCreate():
# #     owner_id: int
# #     recipient_id: int
# #     file_id: int

# # @app.get("/")
# # def index():
# #     return {"message": "Hello World!!"}

# # @app.post("/share/")
# # def share():
# #     owner_id = 1
# #     recipient_id = 2
# #     file_id = 1
# #     bucket = 'myshareanywhere'
# #     object_name = 'container/Paper+--+DRUMGAN+-+SYNTHESIS+OF+DRUM+SOUNDS+WITH+TIMBRAL+FEATURE+CONDITIONING+USING+GENERATIVE+ADVERSARIAL+NETWORKS.pdf'

# #     shareResource = ShareResource()

# #     # Share file with another user
# #     print(shareResource.share_file(file_id, owner_id, recipient_id, 'view'))

# #     # Access file for viewing
# #     print(shareResource.access_file(recipient_id, file_id, 'view'))
# #     return {
# #         "data": ""
# #     }


from fastapi import FastAPI
from app.routers.router import router as item_router

app = FastAPI()

# Include the router
app.include_router(item_router)
