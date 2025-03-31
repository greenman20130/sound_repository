import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from starlette.responses import RedirectResponse

from database import get_database_session, engine
app = FastAPI(
    title="Audio Repository Platform",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

os.makedirs(settings.AUDIO_FILES_DIR, exist_ok=True)

@app.on_event("startup")
async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def zeropoint():
    return {"message": "Hello, how are you?"}