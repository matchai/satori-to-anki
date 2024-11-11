from aqt import QAction, mw
from aqt.utils import showInfo, qconnect

from .satori_reader_login import display_login_dialog


def testFunction() -> None:
    # Number of cards in the current collection
    cardCount = mw.col.cardCount()
    # Show a message box
    showInfo("Card count: %d" % cardCount)


def sync_satori() -> None:
    display_login_dialog(mw)


action = QAction("test", mw)
# Have it call the function when clicked
qconnect(action.triggered, sync_satori)
# Add it to the tools menu
mw.form.menuTools.addAction(action)
