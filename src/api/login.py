from typing import Union
from dataclasses import dataclass
from aqt import (
    QUrl,
    QVBoxLayout,
    QWebEnginePage,
    Qt,
    QDialog,
    QWebEngineView,
    QWebEngineProfile,
)
from aqt.main import AnkiQt
from PyQt6.QtNetwork import QNetworkCookie

from ..config import Config


@dataclass
class LoginSuccess:
    token: str


@dataclass
class LoginFailed:
    message: str


LoginResult = Union[LoginSuccess, LoginFailed]


class SatoriLoginDialog(QDialog):
    SATORI_LOGIN_URL = "https://www.satorireader.com/signin"
    WINDOW_SIZE = (600, 620)
    login_result: LoginResult

    def __init__(self, mw: AnkiQt) -> None:
        super().__init__(parent=mw)
        self.login_result = LoginFailed(message="Failed to authenticate Satori Reader.")
        self._setup_dialog()

    def __enter__(self) -> "SatoriLoginDialog":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.webview.destroy()

    def _setup_dialog(self) -> None:
        # Configure dialog
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(*self.WINDOW_SIZE)

        # Setup webview
        self.webview = QWebEngineView()
        profile = QWebEngineProfile(self.webview)
        cookie_store = profile.cookieStore()
        if cookie_store is None:
            raise RuntimeError("Failed to get cookie store")

        # Listen for cookie added event
        cookie_store.cookieAdded.connect(self._on_cookie_added)

        # Load login webpage
        webpage = QWebEnginePage(profile, self.webview)
        self.webview.setPage(webpage)
        self.webview.load(QUrl(self.SATORI_LOGIN_URL))

        # Set layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a cleaner look
        layout.addWidget(self.webview)

        # Listen for navigation finished signal
        self.webview.loadFinished.connect(self._on_navigation_finished)

    def _on_navigation_finished(self, success: bool) -> None:
        # Prevent user from navigating away from login
        if self.webview.url().toString() != self.SATORI_LOGIN_URL:
            self.login_result = LoginFailed(message="Navigated away from login page")
            self.reject()

    def _on_cookie_added(self, cookie: QNetworkCookie) -> None:
        # Return as soon as the user's session is found
        if cookie.name() == b"SessionToken":
            self.login_result = LoginSuccess(token=cookie.value().data().decode())
            self.accept()


def display_login_dialog(mw: AnkiQt) -> LoginResult:
    try:
        with SatoriLoginDialog(mw) as dialog:
            dialog.exec()

            if isinstance(dialog.login_result, LoginSuccess):
                Config.set("token", dialog.login_result.token)

            return dialog.login_result
    except Exception as e:
        return LoginFailed(message=f"Unexpected error during login: {str(e)}")