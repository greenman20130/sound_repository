import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from starlette.responses import RedirectResponse

from config import settings
from database import get_database_session, engine
from models import Base, User, AudioFile
from auth import get_authenticated_user, create_jwt_token
from oauth import yandex_oauth_service, retrieve_yandex_user_info

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

@app.get("/auth/yandex")
async def initiate_yandex_auth() -> RedirectResponse:
    async with yandex_oauth_service:
        auth_url = await yandex_oauth_service.get_authorization_url()
        return RedirectResponse(url=auth_url)

@app.get("/auth/yandex/callback")
async def handle_yandex_callback(
    user_info = Depends(retrieve_yandex_user_info),
    db: AsyncSession = Depends(get_database_session)
):
    try:
        query_result = await db.execute(
            select(User).where(User.yandex_id == str(user_info.id))
        )
        user = query_result.scalar_one_or_none()
        
        if not user:
            user = User(
                yandex_id=str(user_info.id),
                email=user_info.email,
                username=user_info.display_name or "",
                is_superuser=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        token = create_jwt_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.get("/users/me", response_model=dict)
async def get_current_user_info(auth_user: User = Depends(get_authenticated_user)):
    return {
        "id": auth_user.id,
        "email": auth_user.email,
        "username": auth_user.username,
        "is_active": auth_user.is_active,
        "is_superuser": auth_user.is_superuser
    }

@app.get("/users/{user_id}", response_model=dict)
async def get_user_details(
    user_id: int,
    auth_user: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_database_session)
):
    if not auth_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions"
        )
    
    query_result = await db.execute(select(User).where(User.id == user_id))
    user = query_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser
    }

@app.patch("/users/me", response_model=dict)
async def modify_user_info(
    new_username: str,
    auth_user: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_database_session)
):
    auth_user.username = new_username
    await db.commit()
    await db.refresh(auth_user)
    return {
        "id": auth_user.id,
        "email": auth_user.email,
        "username": auth_user.username,
        "is_active": auth_user.is_active,
        "is_superuser": auth_user.is_superuser
    }

@app.delete("/users/{user_id}")
async def remove_user(
    user_id: int,
    auth_user: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_database_session)
):
    if not auth_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions"
        )
    
    query_result = await db.execute(select(User).where(User.id == user_id))
    user = query_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    await db.delete(user)
    await db.commit()
    return {"message": "User successfully removed"}
