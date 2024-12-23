from typing import Any, Optional
from aqt import mw

tag = mw.addonManager.addonFromModule(__name__)


class Config:
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get a value from the addon config."""
        config = mw.addonManager.getConfig(tag)
        if config is None:
            return None
        return config.get(key)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set a value in the addon config."""
        config = mw.addonManager.getConfig(tag)
        if config is None:
            config = {}

        config[key] = value
        mw.addonManager.writeConfig(tag, config)
