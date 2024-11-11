from aqt import QAction, mw
from aqt.utils import showInfo, qconnect, showWarning

from .satori_reader_login import LoginSuccess, display_login_dialog


def testFunction() -> None:
    # Number of cards in the current collection
    cardCount = mw.col.cardCount()
    # Show a message box
    showInfo("Card count: %d" % cardCount)


def sync_satori() -> None:
    result = display_login_dialog(mw)

    if isinstance(result, LoginSuccess):
        print(f"Login success {result.token}")
    else:
        mw.taskman.run_on_main(lambda: showWarning(str(result)))


action = QAction("Pull from Satori Reader", mw)
qconnect(action.triggered, sync_satori)
mw.form.menuTools.addAction(action)
