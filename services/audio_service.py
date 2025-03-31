import os
from fastapi import HTTPException, UploadFile
from models import AudioFile
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings

class AudioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload_audio_file(self, file: UploadFile, custom_filename: str, owner_id: int):
        if not file.filename.lower().endswith(('.mp3', '.wav', '.ogg')):
            raise HTTPException(status_code=400, detail="Only .mp3, .wav, and .ogg files are supported")

        if not custom_filename:
            custom_filename = file.filename

        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{custom_filename}{file_extension}"
        file_path = os.path.join(settings.AUDIO_FILES_DIR, unique_filename)

        try:
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File saving failed: {str(e)}")

        audio_record = AudioFile(filename=custom_filename, file_path=file_path, owner_id=owner_id)
        self.db.add(audio_record)
        await self.db.commit()
        await self.db.refresh(audio_record)

        return audio_record

    async def list_audio_files(self, owner_id: int):
        query_result = await self.db.execute(select(AudioFile).where(AudioFile.owner_id == owner_id))
        return query_result.scalars().all() 