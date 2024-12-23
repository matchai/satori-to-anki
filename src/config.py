from typing import Any, Optional
from aqt import mw


class Config:
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get a value from the addon config."""
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            return None
        return config.get(key)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set a value in the addon config."""
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            config = {}

        config[key] = value
        mw.addonManager.writeConfig(__name__, config)
