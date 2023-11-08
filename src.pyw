import sys
import webbrowser  # Import the webbrowser module
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QUrl

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setAutoFillBackground(True)
        self.setPalette(QPalette(QColor(53, 53, 53)))
        self.setFixedHeight(30)

        title_label = QLabel("Dark Editor", self)
        title_label.setStyleSheet("color: white; font-size: 14px; padding: 5px;")

        close_button = QPushButton("X", self)
        close_button.setStyleSheet("background-color: gray; color: white; border: none; font-size: 18px; padding: 5px; min-width: 30px;")
        close_button.clicked.connect(self.closeApplication)

        self.layout.addWidget(title_label)
        self.layout.addStretch(1)
        self.layout.addWidget(close_button)

        self.drag_position = None

    def closeApplication(self):
        self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.parent.isMaximized():
                self.parent.showNormal()
            else:
                self.parent.showMaximized()
            event.accept()

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dark Editor")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 800, 600)

        icon_path = 'assets/logo.png'
        app_icon = QIcon(icon_path)

        self.setWindowIcon(app_icon)

        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)

        toolbar = self.addToolBar('File')

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.saveText)
        toolbar.addAction(save_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openText)
        toolbar.addAction(open_action)

        website_action = QAction('Website', self)
        website_action.triggered.connect(self.openWebsite)
        toolbar.addAction(website_action)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

    def saveText(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'IMB Files (*.imb);;Text Files (*.txt);;All Files (*)', options=options)

        if filePath:
            if not filePath.endswith('.txt'):
                filePath += '.txt'
            with open(filePath, 'w') as file:
                text = self.text_edit.toPlainText()
                file.write(text)

    def openText(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'IMB Files (*.imb);;Text Files (*.txt);;All Files (*)', options=options)

        if filePath:
            with open(filePath, 'r') as file:
                text = file.read()
                self.text_edit.setPlainText(text)

    def openWebsite(self):
        website_url = 'https://imbadwithnamestoo.github.io/Dark-Editor-Website/'
        webbrowser.open(website_url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(dark_palette)

    editor = TextEditor()
    editor.show()

    sys.exit(app.exec_())
