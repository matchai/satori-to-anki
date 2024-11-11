from aqt import AnkiQt
from aqt.qt import *

def display_login_dialog(mw: AnkiQt):
  d = QDialog()
  d.setWindowTitle("Satori to Anki")
  d.setWindowModality(Qt.WindowModality.WindowModal)
  d.resize(600, 650)

  url = "https://www.satorireader.com/signin"

  token = None

  def on_cookie_added(cookie) -> None:
    nonlocal token

    if cookie.name() != b"SessionToken":
      return

    token = cookie.value()

  webview = QWebEngineView()
  profile = QWebEngineProfile("storage", webview)
  cookie_store = profile.cookieStore()
  cookie_store.cookieAdded.connect(on_cookie_added)

  webpage = QWebEnginePage(profile, webview)
  webview.setPage(webpage)
  webview.load(QUrl(url))

  layout = QVBoxLayout()
  layout.addWidget(webview)
  d.setLayout(layout)

  d.show()
  d.exec()

  webview.destroy()

  return token
