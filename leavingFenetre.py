import sys
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui

from PyQt5.QtCore import QSize, QDir, QUrl, QPoint, QRect, Qt
from PyQt5.QtGui import QMovie, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
class mgGIF(QWidget):
    def __init__(self, px, py, h, w, parent=None):
        super(mgGIF, self).__init__(parent)
        self.resize(QSize(h, w))
        self.move(py, px)

        movie = QMovie("giphy.gif")
        movie.setScaledSize(QSize(self.height(), self.width()))

        movie.start()
        self.labelImage = QLabel(self)
        self.labelImage.setMovie(movie)
        self.labelImage.setScaledContents(True)



class mnButtons(QWidget):

    def __init__(self, parent=None):
        font = QFont()
        font.setBold(True)
        font.setFamily("TheSansCorrespondence")
        font.setPointSize(15)


        super(mnButtons, self).__init__(parent)

        self.resize(QSize(450, 400))
        self.selector = QLabel(self)
        self.selector.resize(290, 65)
        self.selector.move(100, 290)
        self.selector.setStyleSheet("background-color: #91a196; color: red; border: 4px dashed white; border-bottom-right-radius: 10px; border-bottom-left-radius: 10px; border-top: 0px;")

        self.titlechoix = QLabel("Do you really want to leave?", self)
        self.titlechoix.setAlignment(Qt.AlignCenter)
        self.titlechoix.resize(290, 40)
        self.titlechoix.move(100, 250)
        self.titlechoix.setStyleSheet("background-color: white; color: black; border: 4px dashed white; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        self.titlechoix.setFont(font)

        font.setPointSize(15)

        self.playersai = QPushButton('Yes :(', self)
        self.playersai.resize(130, 40)
        self.playersai.move(110, 300)
        self.playersai.setStyleSheet("background-color: #bfff7f; color: black; border-radius: 20px;")
        self.playersai.setFont(font)

        self.training = QPushButton('No :D', self)
        self.training.resize(130, 40)
        self.training.move(250, 300)
        self.training.setStyleSheet("background-color: #edc596; color: black; border-radius: 20px;")
        self.training.setFont(font)



class leavingFN(QMainWindow):
    def __init__(self, parent=None):
        super(leavingFN, self).__init__(parent)
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
        self.Fenetre = mgGIF(50, 140, 200, 200, self)
        self.Window = mnButtons(self)


        self.setWindowTitle("Mon Snake")
        self.setStyleSheet("background-color: #adadad")

        self.show()

        self.Window.playersai.clicked.connect(self.adios)
        self.Window.training.clicked.connect(self.stay)

    def adios(self):
        #self.Window.playersai.setText("justClicked")
        exit(0)

    def stay(self):
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = leavingFN()
    sys.exit(app.exec_())