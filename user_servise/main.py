from fastapi import FastAPI
from sqladmin import Admin
import asyncio
import uvicorn

from src.logger import logger
from src.admin_panel.auth import AdminAuth
from src.admin_panel.views import UserAdmin
from src.database import engine
from src.config import ADMIN_SECRET_KEY

from src.user.api.routers import user_router
from src.authorization.api.routers import token_router
from src.user.utiles import users_delete_loop

app = FastAPI()

admin = Admin(
    app, 
    engine,
    authentication_backend=AdminAuth(secret_key=ADMIN_SECRET_KEY)
)

admin.add_view(UserAdmin)

app.include_router(user_router)
app.include_router(token_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(users_delete_loop())

if __name__ =='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8085)