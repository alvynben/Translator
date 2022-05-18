import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
import tkinter as tk
# import cv2
from PIL import ImageGrab
from translate import Translator
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = 

def translateChineseToEnglish(text):
    translator = Translator(to_lang="en", from_lang="zh")
    return translator.translate(text)

class MainWindow(QMainWindow):
    background = True
    isSnipping = False

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(widget)
        root = tk.Tk()
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        self.setGeometry(0,0, screenWidth, screenHeight)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    
    def start(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.background = False
        self.isSnipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        print('Capture the Screen...')
        print('Press q if you want to quit')
        self.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if self.isSnipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3   
        else:
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0,0,0,0)
            lw = 0
            opacity = 1
        
        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRect(self.begin, self.end)
        qp.drawRect(rect)
    
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Q:
            print('Quit')
            self.close()
        event.accept()
    
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.begin = event.pos()
        self.end = self.begin
        self.update()
    
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.end = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.isSnipping = False
        self.end = event.pos()
        QtWidgets.QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y() + 50, self.end.y() + 50)
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y() + 50, self.end.y() + 50)

        self.repaint()
        QtWidgets.QApplication.processEvents()
        print((x1,y1,x2,y2))
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        QtWidgets.QApplication.processEvents()
        img.show()
        # rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img,lang="chi_sim")
        text.replace("\n"," ")

        # show the original OCR'd text
        print("ORIGINAL")
        print("========")
        print(text)
        print("")

        # show the translated text
        print("TRANSLATED")
        print("==========")
        print(translateChineseToEnglish(text))

app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.start()
app.exec()