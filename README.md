# Sound Repository Platform

Это платформа для хранения и управления аудиофайлами, использующая FastAPI и PostgreSQL.

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/greenman20130/sound_repository.git
   cd audiorepo
   ```
2. **Создайте файл `.env` в корне проекта и добавьте необходимые переменные окружения:**

   ```env
   # Настройки базы данных
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@db/audio_db
   POSTGRES_USER=your_postgres_user  # Имя пользователя для PostgreSQL
   POSTGRES_PASSWORD=your_postgres_password  # Пароль для PostgreSQL
   POSTGRES_DB=your_postgres_db  # Имя базы данных

   # Настройки JWT
   SECRET_KEY=your_secret_key  # Секретный ключ для JWT
   ALGORITHM=HS256  # Алгоритм шифрования JWT
   ACCESS_TOKEN_EXPIRE_MINUTES=30  # Время жизни токена в минутах

   # Настройки Яндекс OAuth
   YANDEX_CLIENT_ID=your_yandex_client_id  # ID клиента для Яндекс OAuth
   YANDEX_CLIENT_SECRET=your_yandex_client_secret  # Секрет клиента для Яндекс OAuth
   YANDEX_REDIRECT_URI=http://localhost:8000/auth/yandex/callback  # URI перенаправления для Яндекс OAuth

   # Путь для хранения аудиофайлов
   AUDIO_FILES_DIR=audio_files  # Директория для хранения аудиофайлов

   # Email суперпользователя
   SUPERUSER_EMAIL=your_superuser_email@example.com  # Email суперпользователя
   ```
3. **Запустите Docker Compose:**

   ```bash
   docker-compose up --build
   ```
4. **Доступ к API:**

   API будет доступен по адресу `http://localhost:8000`. Вы можете использовать `/docs` для доступа к документации Swagger.

## Использование

- **Аутентификация через Яндекс:** Перейдите по адресу `/auth/yandex` для начала процесса аутентификации.
- **Управление пользователями:** Используйте эндпоинты `/users/me`, `/users/{user_id}` для получения и изменения информации о пользователях.
- **Загрузка аудиофайлов:** Используйте эндпоинт `/audio/upload` для загрузки аудиофайлов.
- **Просмотр аудиофайлов:** Используйте эндпоинт `/audio/files` для получения списка загруженных аудиофайлов.
