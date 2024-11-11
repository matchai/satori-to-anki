from aqt import AnkiQt
from dataclasses import dataclass
from .const import ADDON


@dataclass
class AddonConfig:
    token: str

    @staticmethod
    def get(mw: AnkiQt) -> "AddonConfig":
        config_dict = mw.addonManager.getConfig(ADDON)
        return AddonConfig(**config_dict)
