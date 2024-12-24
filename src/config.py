from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from aqt import mw

tag = mw.addonManager.addonFromModule(__name__)


def _load_config() -> dict[str, Any]:
    config = mw.addonManager.getConfig(tag)
    if config is None:
        config = {}
    return config


def _save_config(config: dict[str, Any]) -> None:
    mw.addonManager.writeConfig(tag, config)


class Config:
    _data: dict[str, Any] = _load_config()

    @classmethod
    def _load(cls) -> None:
        cls._data = _load_config()

    @classmethod
    def _save(cls) -> None:
        _save_config(cls._data)

    @classmethod
    def clear(cls) -> None:
        cls._data = {}
        cls._save()

    @classmethod
    def get_token(cls) -> Optional[str]:
        return cls._data.get("token")

    @classmethod
    def set_token(cls, value: str) -> None:
        cls._data["token"] = value
        cls._save()

    @classmethod
    def get_last_export_time(cls) -> Optional[datetime]:
        timestamp = cls._data.get("last_export_time")
        return datetime.fromisoformat(timestamp) if timestamp else None

    @classmethod
    def set_last_export_time(cls, value: datetime) -> None:
        cls._data["last_export_time"] = value.isoformat()
        cls._save()
