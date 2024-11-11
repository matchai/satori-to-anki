from typing import Optional
from aqt import (
    AnkiQt,
    QUrl,
    QVBoxLayout,
    QWebEnginePage,
    Qt,
    QDialog,
    QWebEngineView,
    QWebEngineProfile,
)


class SatoriLoginDialog(QDialog):
    SATORI_LOGIN_URL = "https://www.satorireader.com/signin"
    WINDOW_TITLE = "Satori to Anki"
    WINDOW_SIZE = (600, 620)

    def __init__(self, mw: AnkiQt) -> None:
        super().__init__(parent=mw)
        self.token: Optional[str] = None

        # Configure dialog
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)

        # Setup webview
        self.webview = QWebEngineView()
        profile = QWebEngineProfile(self.webview)
        profile.cookieStore().cookieAdded.connect(self._on_cookie_added)

        # Load login webpage
        webpage = QWebEnginePage(profile, self.webview)
        self.webview.setPage(webpage)
        self.webview.load(QUrl(self.SATORI_LOGIN_URL))

        # Set layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a cleaner look
        layout.addWidget(self.webview)

    def _on_cookie_added(self, cookie) -> None:
        if cookie.name() == b"SessionToken":
            self.token = cookie.value()
            # Close the dialog
            self.accept()


def display_login_dialog(mw: AnkiQt) -> Optional[str]:
    try:
        dialog = SatoriLoginDialog(mw)
        dialog.exec()
        token = dialog.token
        dialog.webview.destroy()
        return token
    except Exception as e:
        print(f"Login error: {e}")
        return None
