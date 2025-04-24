from fastapi import FastAPI
from sqladmin import Admin
import uvicorn

from src.logger import logger
from src.admin_panel.auth import AdminAuth
from src.admin_panel.views import UserAdmin, CommandAdmin, DepartmentAdmin
from src.database import engine
from src.config import ADMIN_SECRET_KEY

from src.command.api.public.routers import command_router, department_router
from src.command.api.protected.routers import command_protected_router

from src.user.api.public.routers import user_router
from src.user.api.protected.routers import user_protected_router

app = FastAPI()

admin = Admin(
    app, 
    engine,
    authentication_backend=AdminAuth(secret_key=ADMIN_SECRET_KEY)
)

admin.add_view(UserAdmin)
admin.add_view(CommandAdmin)
admin.add_view(DepartmentAdmin)

app.include_router(command_router)
app.include_router(user_router)
app.include_router(department_router)
app.include_router(command_protected_router)
app.include_router(user_protected_router)

if __name__ =='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8085)