from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.article import router as article_router
from app.api.endpoints.tasks import router as tasks_router

app = FastAPI(title="Global Vision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])

