import sys,os
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
from leavingFenetre import *
import subprocess
from PyQt5.QtCore import QSize, QDir, QUrl, QPoint, QRect, Qt
from PyQt5.QtGui import QMovie, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
class mgGIF(QWidget):
    def __init__(self, px, py, h, w, parent=None):
        super(mgGIF, self).__init__(parent)
        self.resize(QSize(h, w))
        self.move(py, px)

        movie = QMovie("choix.gif")
        movie.start()
        self.labelImage = QLabel(self)
        self.labelImage.setMovie(movie)
        self.labelImage.setScaledContents(True)


class mnButtons(QWidget):

    def __init__(self, parent=None):
        font = QFont()
        font.setBold(True)
        font.setFamily("TheSansCorrespondence")
        font.setPointSize(18)


        self.www = QWidget()
        super(mnButtons, self).__init__(parent)

        self.resize(QSize(450, 450))
        self.selector = QLabel(self)
        self.selector.resize(290, 160)
        self.selector.move(100, 240)
        self.selector.setStyleSheet("background-color: #91a196; color: red; border: 4px dashed white; border-bottom-right-radius: 10px; border-bottom-left-radius: 10px; border-top: 0px;")

        self.titlechoix = QLabel("CHOIX DE MODE JEU", self)
        self.titlechoix.setAlignment(Qt.AlignCenter)
        self.titlechoix.resize(290, 40)
        self.titlechoix.move(100, 200)
        self.titlechoix.setStyleSheet("background-color: white; color: black; border: 4px dashed white; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        self.titlechoix.setFont(font)

        font.setPointSize(15)

        self.players2 = QPushButton('2-PLAYERS', self)
        self.players2.resize(120, 40)
        self.players2.move(110, 270)
        self.players2.setStyleSheet("background-color: #ffdf7c; color: black; border-top-left-radius: 20px; ")
        self.players2.setFont(font)

        self.players1 = QPushButton('1-PLAYER', self)
        self.players1.resize(120, 40)
        self.players1.move(260,270)
        self.players1.setStyleSheet("background-color: #8fe9df; color: black; border-top-right-radius: 20px;")
        self.players1.setFont(font)

        self.playersai = QPushButton('AI-PLAYER', self)
        self.playersai.resize(270, 40)
        self.playersai.move(110, 330)
        self.playersai.setStyleSheet("background-color: #bfff7f; color: black; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;")
        self.playersai.setFont(font)





class fenetreMG(QMainWindow):
    def __init__(self, parent=None):
        super(fenetreMG, self).__init__(parent)
        self.resize(500, 500)

        self.startUIWindow()

        self.filename = 'snake.mp3'
        self.fullpath = QDir.current().absoluteFilePath(self.filename)
        self.media = QUrl.fromLocalFile(self.fullpath)
        self.content = QtMultimedia.QMediaContent(self.media)
        self.player = QtMultimedia.QMediaPlayer()
       #self.player.setMedia(self.content)
       #self.player.play()

    def startUIWindow(self):
        self.Fenetre = mgGIF(-80, -55, 500, 300, self)
        self.Window = mnButtons(self)

        self.setWindowTitle("Mon Snake")
        self.setStyleSheet("background-color: #4b525d")

        self.show()

        self.Window.playersai.clicked.connect(self.decr3)

        self.Window.players1.clicked.connect(self.decr1)
        self.Window.players2.clicked.connect(self.decr2)

    def decr1(self):

        sleep = subprocess.Popen(['python', 'allcode.py','1'])
        self.hide()
    def decr2(self):

        sleep = subprocess.Popen(['python', 'allcode.py','2'])
        self.hide()

    def decr3(self):

        sleep = subprocess.Popen(['python', 'allcode.py', '3'])
        self.hide()
    def closeEvent(self, event):
        self.closet = leavingFN(self)
        event.ignore()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = fenetreMG()
    sys.exit(app.exec_())