from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.article import router as article_router
from app.api.endpoints.sources import router as sources_router
from app.api.endpoints.tasks import router as tasks_router

app = FastAPI(title="Global Vision API")

# 联调加固：仅允许前端开发源，避免生产被任意域名跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(sources_router, prefix="/api/v1/sources", tags=["sources"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])

