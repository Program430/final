from fastapi import FastAPI
from sqladmin import Admin
import asyncio
import uvicorn

from src.logger import logger
from src.admin_panel.auth import AdminAuth
from src.admin_panel.views import TaskAdmin, CommentAdmin, MarkAdmin, MeetingAdmin
from src.database import engine
from src.config import ADMIN_SECRET_KEY

from src.task.api.public.routers import task_router
from src.comment.api.public.routers import task_comment_router
from src.mark.api.public.routers import mark_router
from src.calendar.api.public.routers import meeting_router


app = FastAPI()

admin = Admin(
    app, 
    engine,
    authentication_backend=AdminAuth(secret_key=ADMIN_SECRET_KEY)
)

admin.add_view(TaskAdmin)
admin.add_view(CommentAdmin)
admin.add_view(MarkAdmin)
admin.add_view(MeetingAdmin)

app.include_router(task_router)
app.include_router(task_comment_router)
app.include_router(mark_router)
app.include_router(meeting_router)

if __name__ =='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8085)