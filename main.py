from PyQt5.QtWebEngineWidgets import *  # pip install pyqtwebengine
from PyQt5.QtWidgets import QShortcut  # pip install pyqt5
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tab_widget)
        
        qtoolbar = QToolBar("Nav")
        qtoolbar.setIconSize(QSize(30, 30))
        qtoolbar.setAllowedAreas(Qt.TopToolBarArea)
        qtoolbar.setFloatable(False)
        qtoolbar.setMovable(False)
        self.addToolBar(qtoolbar)

        back_btn = QAction(QIcon(os.path.join("img", "back.png")), "Назад", self)
        back_btn.setStatusTip("Назад")
        back_btn.triggered.connect(lambda: self.tab_widget.currentWidget().back())
        qtoolbar.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join("img", "forward.png")), "Вперед", self)
        next_btn.setStatusTip("Вперед")
        next_btn.triggered.connect(lambda: self.tab_widget.currentWidget().forward())
        qtoolbar.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join("img", "reload.png")), "Перезаватнажити", self)
        reload_btn.setStatusTip("Перезавантажити")
        reload_btn.triggered.connect(lambda: self.tab_widget.currentWidget().reload())
        qtoolbar.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join("img", "home.png")), "Додому", self)
        home_btn.setStatusTip("Додому")
        home_btn.triggered.connect(lambda: self.nav_home())
        qtoolbar.addAction(home_btn)

        qtoolbar.addSeparator()

        self.https_icon = QLabel()
        self.https_icon.setPixmap(QPixmap(os.path.join("img", "lock.png")))
        qtoolbar.addWidget(self.https_icon)

        self.url_line = QLineEdit()
        self.url_line.returnPressed.connect(self.nav_to_url)
        qtoolbar.addWidget(self.url_line)

        new_tab_btn = QAction(QIcon(os.path.join("img", "plus.png")), "Нова вкладка", self)
        new_tab_btn.setStatusTip("Нова вкладка")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        qtoolbar.addAction(new_tab_btn)

        info_btn = QAction(QIcon(os.path.join("img", "info.png")), "інформація", self)
        info_btn.triggered.connect(self.info)
        qtoolbar.addAction(info_btn)

        self.add_new_tab(QUrl("http://newtab.kesug.com/"), "Домашня сторінка")

        self.shortcut = QShortcut(QKeySequence("F5"), self)
        self.shortcut.activated.connect(lambda: self.tab_widget.currentWidget().reload())
        self.show()
        self.setWindowIcon(QIcon(os.path.join("icon.ico")))

    def add_new_tab(self, qurl=QUrl("http://newtab.kesug.com/"), label="blank"):
        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        browser.page().fullScreenRequested.connect(lambda request: request.accept())
        browser.setUrl(qurl)

        tab = self.tab_widget.addTab(browser, label)
        self.tab_widget.setCurrentIndex(tab)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=tab, browser=browser:
                                     self.tab_widget.setTabText(tab, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tab_widget.currentWidget().url()
        self.update_urlbar(qurl, self.tab_widget.currentWidget())
        self.update_title(self.tab_widget.currentWidget())

    def close_current_tab(self, i):
        if self.tab_widget.count() < 2:
            return

        self.tab_widget.removeTab(i)

    def update_title(self, browser):
        if browser != self.tab_widget.currentWidget():
            return
        title = self.tab_widget.current().page().title()
        self.setWindowTitle(f"{title} - Internet Surfer")

    def info(self):
        QMessageBox.about(self, "Інформація", "Internet Surfer 1 \nCopyright Huliak Markiian")

    def nav_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("http://newtab.kesug.com/"))

    def nav_to_url(self):
        qurl = QUrl(self.url_line.text())
        if qurl.scheme() == "":
            qurl.setScheme("http")

        self.tab_widget.currentWidget().setUrl(qurl)

    def update_urlbar(self, url, browser=None):
        if browser != self.tab_widget.currentWidget():
            return

        if url.scheme() == "https":
            self.https_icon.setPixmap(QPixmap(os.path.join("img", "lock.png")))
        else:
            self.https_icon.setPixmap(QPixmap(os.path.join("img", "unlock.png")))

        self.url_line.setText(url.toString())
        self.url_line.setCursorPosition(999)
        
if __name__ == '__main__':
    app = QApplication([])
    app.setOrganizationName("Guljak Corporation")
    QApplication.setApplicationName("Internet Surfer")
    QApplication.setWindowIcon(QIcon('icon.ico'))
    window = Browser()
    window.showMaximized()
    app.exec_()
