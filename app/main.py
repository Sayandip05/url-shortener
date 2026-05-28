from fastapi import FastAPI
from app.modules.urls.router import router as urls_router, redirect_router
from app.modules.health.router import router as health_router

app = FastAPI(title="URL Shortener", version="1.0.0")

app.include_router(health_router)
app.include_router(urls_router, prefix="/api/v1")
app.include_router(redirect_router)
