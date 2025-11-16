from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineFullScreenRequest, QWebEngineProfile, QWebEnginePage, QWebEngineUrlRequestInterceptor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, QLabel,
    QLineEdit, QMessageBox, QWidget, QVBoxLayout
)
from PyQt6.QtGui import QAction, QShortcut, QKeySequence, QIcon, QPixmap
from PyQt6.QtCore import QUrl, QSize, Qt
import os
import sys

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self):
        super().__init__()

        self.block_list = [
            "doubleclick.net",
            "googlesyndication.com",
            "adservice.google.com",
            "adsystem.com",
            "advertising.com",
            "taboola.com",
            "outbrain.com",
            "zedo.com",
            "yahoo.com/ad",
            "banner",
            "/ads?",
            "/ads/",
            "/adserver"
        ]

    def interceptRequest(self, info):
        url = info.requestUrl().toString().lower()
        for pattern in self.block_list:
            if pattern in url:
                info.block(True)
                return

class MyWebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadFinished.connect(self.check_error)

    def check_error(self, ok):
        if not ok:
            offline_path = os.path.abspath("offline.html")
            print("Error loading page >> opening offline page")
            self.setUrl(QUrl.fromLocalFile(offline_path))




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
        qtoolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
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

        reload_btn = QAction(QIcon(os.path.join("img", "reload.png")), "Перезавантажити", self)
        reload_btn.setStatusTip("Перезавантажити")
        reload_btn.triggered.connect(lambda: self.tab_widget.currentWidget().reload())
        qtoolbar.addAction(reload_btn)

        new_tab_btn = QAction(QIcon(os.path.join("img", "plus.png")), "Нова вкладка", self)
        new_tab_btn.setStatusTip("Нова вкладка")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        qtoolbar.addAction(new_tab_btn)

        info_btn = QAction(QIcon(os.path.join("img", "info.png")), "інформація", self)
        info_btn.triggered.connect(self.info)
        qtoolbar.addAction(info_btn)

        new_tab_url = os.path.abspath("NewTab/index.html")
        self.add_new_tab(QUrl.fromLocalFile(new_tab_url), "Домашня сторінка")

        self.shortcut = QShortcut(QKeySequence.StandardKey.Refresh, self)
        self.shortcut.activated.connect(lambda: self.tab_widget.currentWidget().reload())
        self.show()
        self.setWindowIcon(QIcon(os.path.join("icon.ico")))

        qtoolbar.setIconSize(QSize(24, 24))
        profile = QWebEngineProfile.defaultProfile()
        
        self.adblock = AdBlocker()
        profile.setUrlRequestInterceptor(self.adblock)

        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)



        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f2f7fd, stop:1 #e3eefb);
            }
            QToolBar {
                background-color: rgba(126, 169, 232, 0.7);
                border: 1px solid #a3a7ac;
            }
            QTabWidget::pane {
                border: 1px solid #A0A0A0;
            }
            QTabBar::tab {
                background: #ffffff;
                border: 1px solid #a3a7ac;
                padding: 5px;
                border-radius: 5px 5px 0 0;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #c3ddfb, stop:1 #ffffff);
                border-bottom: 1px solid #a3a7ac;
            }
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #ced9eb, stop:1 #cdd9eb);
                border: 1px solid #98a1a6;
                padding: 5px;
            }
            QLabel {
                color: #000000;
            }
            QAction {
                color: #000000;
            }
        """)

    def add_new_tab(self, qurl=QUrl.fromLocalFile(os.path.abspath("NewTab/index.html")), label="blank"):
        browser = QWebEngineView()
        browser.setPage(MyWebPage(browser))

        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

        browser.page().fullScreenRequested.connect(self.handle_fullscreen)

        browser.setUrl(qurl)

        tab = self.tab_widget.addTab(browser, label)
        self.tab_widget.setCurrentIndex(tab)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=tab, browser=browser:
                                    self.tab_widget.setTabText(tab, browser.page().title()))

    def handle_fullscreen(self, request: QWebEngineFullScreenRequest):
        if request.toggleOn():
            for i in range(self.tab_widget.count()):
                self.tab_widget.widget(i).setVisible(True)
            self.tab_widget.tabBar().hide()
            self.findChild(QToolBar).hide()
            self.showFullScreen()
        else:
            self.tab_widget.tabBar().show()
            self.findChild(QToolBar).show()
            self.showNormal()
        request.accept()

        
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
        title = self.tab_widget.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Internet Surfer")

    def info(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Про Internet Surfer")

        content_widget = QWidget()
        layout = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap('icon_info.png')
        logo_label.setPixmap(pixmap)
        layout.addWidget(logo_label)

        text_label = QLabel("Version 1.0.6\nCipher Strength: 128-bit\nProduct ID: 12345-67890\nUpdate Versions: SP1;")
        layout.addWidget(text_label)

        text_label2 = QLabel("Copyright © 2024 Guljak Markijan")
        layout.addWidget(text_label2)

        content_widget.setLayout(layout)
        msgBox.layout().addWidget(content_widget)

        msgBox.setStyleSheet("QMessageBox {background-color: #f0f0f0; font-size: 14px;}"
                             "QLabel {color: #333333;}"
                             "QTextEdit {background-color: #f0f0f0; border: none;}")
        msgBox.exec()

    def nav_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl(os.path.abspath("NewTab/index.html")))

    def nav_to_url(self):
        text = self.url_line.text().strip()

        if " " in text or "." not in text:
            search_url = "https://www.google.com/search?q=" + text.replace(" ", "+")
            self.tab_widget.currentWidget().setUrl(QUrl(search_url))
            return

        qurl = QUrl(text)
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
    app = QApplication(sys.argv)
    app.setOrganizationName("Guljak Markijan")
    QApplication.setApplicationName("Internet Surfer")
    QApplication.setWindowIcon(QIcon('icon.ico'))
    window = Browser()
    window.showMaximized()
    sys.exit(app.exec())
