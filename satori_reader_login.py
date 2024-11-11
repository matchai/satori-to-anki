from typing import Optional, Union
from dataclasses import dataclass
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


@dataclass
class LoginSuccess:
    token: str


class LoginFailed(str):
    pass


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

        # Add navigation finished signal
        self.webview.loadFinished.connect(self._on_navigation_finished)

    def _on_navigation_finished(self, success: bool) -> None:
        # Prevent user from navigating away from login
        if self.webview.url().toString() != self.SATORI_LOGIN_URL:
            self.reject()

    def _on_cookie_added(self, cookie) -> None:
        # Return as soon as the user's session is found
        if cookie.name() == b"SessionToken":
            self.token = cookie.value()
            self.accept()


def display_login_dialog(mw: AnkiQt) -> Union[LoginSuccess, LoginFailed]:
    try:
        dialog = SatoriLoginDialog(mw)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted and dialog.token:
            return LoginSuccess(token=dialog.token)
        elif result == QDialog.DialogCode.Rejected:
            return LoginFailed("Failed to authenticate Satori Reader.")
    except Exception as e:
        return LoginFailed(f"Unexpected error during login: {str(e)}")
    finally:
        dialog.webview.destroy()
