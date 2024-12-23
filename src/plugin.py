from aqt import QAction, mw
from aqt.qt import qconnect
from aqt.utils import showWarning

from .config import Config
from .api.login import LoginSuccess, display_login_dialog
from .api.flashcards import request_flashcard_export


def sync_satori() -> None:
    token = Config.get("token")
    if token is None:
        result = display_login_dialog(mw)
        if isinstance(result, LoginSuccess):
            token = result.token
        else:
            showWarning(result.message)

    if token is None:
        showWarning("Login unexpectedly failed")
        return None

    request_flashcard_export()


action = QAction("Pull from Satori Reader", mw)
qconnect(action.triggered, sync_satori)
mw.form.menuTools.addAction(action)
