from app.core.config import settings

from .media import LocalMediaStorage, MediaStorage

media_storage: MediaStorage = LocalMediaStorage(
    root_path=settings.MEDIA_STORAGE_PATH,
    base_url=settings.MEDIA_BASE_URL,
)
