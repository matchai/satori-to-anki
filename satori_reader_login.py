from aqt import AnkiQt
from aqt.qt import *

def display_login_dialog(mw: AnkiQt):
  # Create and configure the dialog
  d = QDialog()
  d.setWindowTitle("Satori to Anki")
  d.setWindowModality(Qt.WindowModality.WindowModal)
  d.resize(600, 660)

  url = "https://www.satorireader.com/signin"
  token = None

  def on_cookie_added(cookie) -> None:
    nonlocal token

    if cookie.name() != b"SessionToken":
      return

    # Close the dialog when the token is received
    token = cookie.value()
    d.accept()

  # Setup a profile to capture cookies
  webview = QWebEngineView()
  profile = QWebEngineProfile("storage", webview)
  cookie_store = profile.cookieStore()
  cookie_store.cookieAdded.connect(on_cookie_added)

  # Load the login URL
  webpage = QWebEnginePage(profile, webview)
  webview.setPage(webpage)
  webview.load(QUrl(url))

  # Add the webview to a dialog layout
  layout = QVBoxLayout()
  layout.addWidget(webview)
  d.setLayout(layout)

  # Show the dialog until it completes
  d.exec()
  webview.destroy()

  return token
