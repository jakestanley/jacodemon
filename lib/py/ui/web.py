import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class WebPageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        web_view = QWebEngineView(self)
        layout.addWidget(web_view)

        # Load a web page URL
        url = "https://doomwiki.org"
        web_view.setUrl(QUrl(url))

        self.setWindowTitle("Doom Wiki Viewer")
        self.setGeometry(100, 100, 1280, 768)

def OpenDoomWiki():
    app = QApplication(sys.argv)
    webPageWindow = WebPageWindow()
    webPageWindow.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(OpenDoomWiki())