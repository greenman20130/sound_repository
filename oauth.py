from fastapi import HTTPException
from auth365 import YandexOAuth
from config import settings

class CustomYandexOAuthService(YandexOAuth):
    default_scope = ["login:email", "login:info"]

yandex_oauth_service = CustomYandexOAuthService(
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    redirect_uri=settings.YANDEX_REDIRECT_URI
)

async def retrieve_yandex_user_info():
    try:
        async with yandex_oauth_service:
            user_info = await yandex_oauth_service.get_user_info()
            if not user_info.email:
                raise HTTPException(
                    status_code=400,
                    detail="Email not received from Yandex"
                )
            return user_info
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 