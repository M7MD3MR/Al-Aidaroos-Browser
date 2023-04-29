import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Al-Aidaroos Browser')
        self.setWindowIcon(
            QIcon('AlAidaroos_Browser\2a453a21169448b7a466e5a4baf24b50.png'))
        self.setGeometry(100, 100, 800, 600)

        # Create and set up the main web view
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl('https://www.google.com'))
        self.setCentralWidget(self.web_view)

        # create the address bar
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)

        # Create the navigation bar and add buttons
        navigation_bar = QToolBar('Navigation')
        self.addToolBar(navigation_bar)

        back_button = QAction(
            QIcon('AlAidaroos_Browser\back.png'), 'Back', self)
        back_button.triggered.connect(self.web_view.back)
        navigation_bar.addAction(back_button)

        forward_button = QAction(
            QIcon('AlAidaroos_Browser\forward.png'), 'Forward', self)
        forward_button.triggered.connect(self.web_view.forward)
        navigation_bar.addAction(forward_button)

        reload_button = QAction(
            QIcon('AlAidaroos_Browser\reload.png'), 'Reload', self)
        reload_button.triggered.connect(self.web_view.reload)
        navigation_bar.addAction(reload_button)

        # Add a button to toggle dark mode
        dark_mode_button = QToolButton()
        dark_mode_button.setText('Dark Mode')
        dark_mode_button.setCheckable(True)
        dark_mode_button.toggled.connect(self.toggle_dark_mode)
        navigation_bar.addWidget(dark_mode_button)

        # Add a button to close the current tab
        close_tab_button = QToolButton()
        close_tab_button.setText('Close Tab')
        close_tab_button.clicked.connect(self.close_current_tab)
        navigation_bar.addWidget(close_tab_button)

        # Create a new tab button
        new_tab_button = QPushButton("+")
        new_tab_button.clicked.connect(self.create_new_tab)
        navigation_bar.addWidget(new_tab_button)


        # Add the menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        # Add a button to open a new tab
        new_tab_action = QAction(QIcon('new_tab.png'), 'New Tab', self)
        new_tab_action.triggered.connect(self.create_new_tab)
        file_menu.addAction(new_tab_action)

        # Add a button to close the current tab
        close_tab_action = QAction(QIcon('close_tab.png'), 'Close Tab', self)
        close_tab_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action)

        # Add a button to exit the browser
        exit_action = QAction(QIcon('exit.png'), 'Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # add the address bar and tabs to the main window
        self.setCentralWidget(self.tabs)
        self.statusBar()

        # Add a button to toggle dark mode
        dark_mode_action = QAction('Dark Mode', self)
        dark_mode_action.setCheckable(True)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        file_menu.addAction(dark_mode_action)

        self.show()


    def toggle_dark_mode(self, state):
        if state:
            style = """
                QTabWidget::pane { 
                    border-top: 1px solid #333; 
                }
                QTabBar::tab {
                    background-color: #222;
                    color: #fff;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QTabBar::tab:selected {
                    background-color: #444;
                    border-color: #666;
                }
                QWidget {
                    color: #bbb;
                    background-color: #222;
                }
            """
        else:
            style = ""
        self.setStyleSheet(style)
        self.tabs.setStyleSheet(style)


    def create_new_tab(self):
        # create the web view and add it to a new tab
        tab = QWidget()
        web_view = QWebEngineView()
        tab.layout = QVBoxLayout(tab)
        tab.layout.addWidget(web_view)
        web_view.load(QUrl("https://www.google.com"))
        self.tabs.addTab(tab, "New Tab")

    def load_url(self):
        # load the URL in the current tab
        url = self.address_bar.text()
        self.tabs.currentWidget().layout.itemAt(0).widget().load(QUrl(url))


    def add_new_tab(self, qurl=None, label='Blank'):
        # Create the webview
        webview = QWebEngineView()
        webview.setUrl(qurl)

        # Add the webview to a new tab
        i = self.tab_widget.addTab(webview, label)
        self.tab_widget.setCurrentIndex(i)

        # Connect the webview's URL to the window's title bar
        webview.urlChanged.connect(lambda qurl, webview=webview:
                                   self.setTabText(self.tab_widget.indexOf(webview), webview.title()))

        # Connect the webview's title to the window's title bar
        webview.titleChanged.connect(lambda title, webview=webview:
                                     self.setTabText(self.tab_widget.indexOf(webview), title))

        # Connect the webview's load finished signal to apply dark mode if it's enabled
        webview.loadFinished.connect(lambda success, webview=webview:
                                     self.apply_dark_mode(webview) if self.dark_mode_enabled else None)

    def current_webview(self):
        return self.tab_widget.currentWidget()

    def tab_open_doubleclick(self, i):
        if i == -1:  # If no tabs are open
            self.add_new_tab()

    def current_tab_changed(self, i):
        webview = self.tab_widget.widget(i)
        self.setWindowIcon(webview.icon())


    def apply_dark_mode(self, webview, enabled=True):
        if enabled:
            # Use JavaScript to modify the CSS of the current page
            css = """
            body {
                background-color: #1A1A1D;
                color: #F2F2F2;
            }
            a {
                color: #FFFFFF;
            }
            """
            webview.page().runJavaScript(
                "var style = document.createElement('style'); style.innerHTML = '{}'; document.head.appendChild(style);".format(css))
        else:
            # Remove the dark mode CSS if it was previously applied
            webview.page().runJavaScript(
                "var style = document.querySelector('style'); if (style !== null) { style.remove(); }")


    def close_current_tab(window):
        # Get the current tab index
        current_tab_index = window.tabs.index(window.current_tab)

        # Remove the current tab from the tabs array
        window.tabs.splice(current_tab_index, 1)

        # Set the current tab to the previous tab
        window.current_tab = window.tabs[current_tab_index - 1]

    def close_current_tab(self):
        current_tab_index = self.tabs.currentIndex()
        if current_tab_index != 0:
            self.tabs.removeTab(current_tab_index)



    def keyPressEvent(self, e):
        # Open a new tab when the user presses Ctrl+T
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.key() == Qt.Key.Key_T:
            self.add_new_tab()

    def contextMenuEvent(self, event):
        # Create a context menu with the option to open links in new tabs
        menu = QMenu(self)

        new_tab_action = QAction("Open Link in New Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab(
            QUrl.fromUserInput(self.current_webview().selectedText())))

        menu.addAction(new_tab_action)

        menu.exec(event.globalPos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec())
