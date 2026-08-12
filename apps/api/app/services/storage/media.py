from pathlib import Path
from typing import Protocol


class MediaStorage(Protocol):
    def save(
        self,
        content: bytes,
        storage_key: str,
    ) -> str:
        ...

    def delete(
        self,
        storage_key: str,
    ) -> None:
        ...

    def exists(
        self,
        storage_key: str,
    ) -> bool:
        ...


class LocalMediaStorage:
    def __init__(
        self,
        root_path: str,
        base_url: str,
    ) -> None:
        self.root_path = Path(root_path)
        self.base_url = base_url.rstrip("/")

        self.root_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _resolve_path(
        self,
        storage_key: str,
    ) -> Path:
        path = (self.root_path / storage_key).resolve()

        root = self.root_path.resolve()

        if path != root and root not in path.parents:
            raise ValueError("Invalid media storage key.")

        return path

    def save(
        self,
        content: bytes,
        storage_key: str,
    ) -> str:
        path = self._resolve_path(storage_key)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_bytes(content)

        return f"{self.base_url}/{storage_key.lstrip('/')}"

    def delete(
        self,
        storage_key: str,
    ) -> None:
        path = self._resolve_path(storage_key)

        if path.exists():
            path.unlink()

    def exists(
        self,
        storage_key: str,
    ) -> bool:
        return self._resolve_path(storage_key).exists()
