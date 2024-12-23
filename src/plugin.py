from aqt import QAction, mw
from aqt.qt import qconnect
from aqt.utils import showInfo, showWarning

from .config import Config

from .satori_reader_login import LoginSuccess, display_login_dialog


def sync_satori() -> None:
    token = Config.get("token")
    if token is None:
        result = display_login_dialog(mw)
        if not isinstance(result, LoginSuccess):
            mw.taskman.run_on_main(lambda: showWarning(result.message))

    if token is not None:
        print(f"Login success {token}")
    else:
        print("Login failed")


action = QAction("Pull from Satori Reader", mw)
qconnect(action.triggered, sync_satori)
mw.form.menuTools.addAction(action)
