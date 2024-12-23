from aqt import QAction, mw
from aqt.qt import qconnect
from aqt.utils import showWarning, tooltip
from aqt.gui_hooks import sync_did_finish
import time

from .config import Config
from .api.login import LoginSuccess, display_login_dialog
from .api.export import request_flashcard_export
from .api.download import get_latest_export_url

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
    download_url = get_latest_export_url()
    print(f"Download URL: {download_url}")

action = QAction("Pull from Satori Reader", mw)
qconnect(action.triggered, sync_satori)
mw.form.menuTools.addAction(action)

sync_did_finish.append(lambda: auto_sync_satori())


def auto_sync_satori() -> None:
    start_time = time.time()

    def on_done(future) -> None:
        tooltip(f"Synced with Satori Reader in {time.time() - start_time:.2f} seconds")
        mw.reset()

    mw.taskman.run_in_background(lambda: sync_satori(), on_done)
