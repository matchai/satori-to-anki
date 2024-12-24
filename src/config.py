from datetime import datetime
from typing import Any, Optional

from aqt import mw

tag = mw.addonManager.addonFromModule(__name__)


def load_config() -> dict[str, Any]:
    config = mw.addonManager.getConfig(tag)
    if config is None:
        config = {}
    return config


def save_config(config: dict[str, Any]) -> None:
    mw.addonManager.writeConfig(tag, config)


class Config:
    _data: dict[str, Any] = load_config()

    @classmethod
    def load(cls) -> None:
        cls._data = load_config()

    @classmethod
    def save(cls) -> None:
        save_config(cls._data)

    @classmethod
    def clear(cls) -> None:
        cls._data = {}
        cls.save()

    @classmethod
    def get_token(cls) -> Optional[str]:
        return cls._data.get("token")

    @classmethod
    def set_token(cls, value: str) -> None:
        cls._data["token"] = value
        cls.save()

    @classmethod
    def get_last_export_time(cls) -> Optional[datetime]:
        timestamp = cls._data.get("last_export_time")
        return datetime.fromisoformat(timestamp) if timestamp else None

    @classmethod
    def set_last_export_time(cls, value: datetime) -> None:
        cls._data["last_export_time"] = value.isoformat()
        cls.save()
