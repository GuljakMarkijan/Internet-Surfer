import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QAction, QToolBar, QLineEdit, QTabWidget, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWebEngineWidgets import QWebEngineView


class BrowserTab(QWebEngineView):
    def __init__(self):
        super(BrowserTab, self).__init__()
        self.setUrl(QUrl("http://newtab.kesug.com/"))

class App_PyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)  # Дозволити закриття вкладок
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        
        

        self.navtb = QToolBar()
        self.addToolBar(self.navtb)

        back_btn = QAction("<", self)
        back_btn.triggered.connect(self.navigate_back)
        self.navtb.addAction(back_btn)

        next_btn = QAction(">", self)
        next_btn.triggered.connect(self.navigate_forward)
        self.navtb.addAction(next_btn)

        reload_btn = QAction("Перезавантажити", self)
        reload_btn.triggered.connect(self.reload_page)
        self.navtb.addAction(reload_btn)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.navtb.addWidget(self.urlbar)

        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(self.addTab)
        self.navtb.addAction(new_tab_btn)

    def navigate_to_bookmark(self, i):
        q = QUrl(self.bookmarks[i])
        if q.scheme() == "":
            q.setScheme("https")
            self.tabs.currentWidget().setUrl(q)
            
    def navigate_back(self):
        self.tabs.currentWidget().back()

    def navigate_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("https")
        self.tabs.currentWidget().setUrl(q)

    def addTab(self):
        tab = BrowserTab()
        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(lambda qurl, tab=tab: self.update_urlbar(qurl, tab))
        tab.loadFinished.connect(lambda _, i=i, tab=tab: self.tabs.setTabText(i, tab.page().title()))
        
        close_tab_btn = QAction("x", self)  # Створіть кнопку закриття
        close_tab_btn.triggered.connect(self.close_current_tab)  # Пов'яжіть з обробником подій
    

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            self.close()
    
        
    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index >= 0:
            self.tabs.removeTab(current_index)

    def update_urlbar(self, q, tab=None):
        if tab is not self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        
    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            self.close()

app = QApplication(sys.argv)
main_window = App_PyQt()
main_window.setWindowTitle("Internet Surfer")  # Встановлення заголовку головного вікна
main_window.resize(800, 700)  # Встановлення розміру головного вікна
main_window.move(300, 500)  # Встановлення позиції головного вікна
main_window.show()  # Відображення головного вікна
sys.exit(app.exec_()) 
