import time
from collections.abc import Callable
from concurrent.futures import Future

from aqt import QAction, mw
from aqt.gui_hooks import sync_did_finish
from aqt.qt import qconnect
from aqt.utils import showWarning, tooltip

from .api.download import download_export_file
from .api.export import request_flashcard_export
from .api.login import display_login_dialog
from .config import Config


def sync_satori() -> None:
    token = Config.get_token()
    if token is None:
        showWarning("Please login before exporting flashcards")
        return

    request_flashcard_export()
    file_path = download_export_file()
    print(f"CSV file downloaded to: {file_path}")


sync = QAction("Sync with Satori Reader", mw)
qconnect(sync.triggered, sync_satori)
mw.form.menuTools.addAction(sync)

login = QAction("Login to Satori Reader", mw)
qconnect(login.triggered, lambda: display_login_dialog(mw))
mw.form.menuTools.addAction(login)

logout = QAction("Logout from Satori Reader", mw)
qconnect(logout.triggered, Config.clear)
mw.form.menuTools.addAction(logout)

if Config.get_token() is not None:
    sync_did_finish.append(lambda: auto_sync_satori())


def auto_sync_satori() -> None:
    start_time = time.time()

    def on_done(_future: Callable[Future, None]) -> None:
        tooltip(f"Synced with Satori Reader in {time.time() - start_time:.2f} seconds")
        mw.reset()

    mw.taskman.run_in_background(lambda: sync_satori(), on_done)
