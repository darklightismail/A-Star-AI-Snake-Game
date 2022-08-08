from menuGeneral import *
from PyQt5.QtCore import QSize, QDir, QUrl
from PyQt5.QtGui import QMovie, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel


class monGIF(QWidget):
    def __init__(self, px, py, h, w, parent=None):
        super(monGIF, self).__init__(parent)

        self.resize(QSize(h, w))

        self.move(py, px)

        self.movie = QMovie("loadingx.gif")
        self.movie.setScaledSize(QSize(self.height(), self.width()))
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        self.frameRect = currentFrame.rect()

        self.frameRect.moveCenter(self.rect().center())
        if self.frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(self.frameRect.left(), self.frameRect.top(), currentFrame)


class UIWindow(QWidget):
    def __init__(self, parent=None):
        font = QFont()
        font.setBold(True)
        font.setFamily("TheSans")
        font.setPointSize(15)

        super(UIWindow, self).__init__(parent)

        self.resize(QSize(500, 500))
        self.dc = 5
        self.decompteur = QPushButton("5", self)
        self.decompteur.resize(100, 40)
        self.decompteur.move(200,460)
        self.decompteur.setStyleSheet("background-color: white; color: black; ")

        self.labelImage = QLabel(self)
        pixmap = QPixmap("man.png")
        self.labelImage.setPixmap(pixmap)

        self.labelImage.setGeometry(120,120, 250, 290)
        self.labelImage.setScaledContents(True)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.resize(500, 500)
        self.startUIWindow()

        self.filename = 'gamesong.mp3'


        self.fullpath = QDir.current().absoluteFilePath(self.filename)
        self.media = QUrl.fromLocalFile(self.fullpath) # charger le fichier de son
        self.content = QtMultimedia.QMediaContent(self.media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(self.content)
        self.player.play()



    def startUIWindow(self):
        monGIF(-120, 115, 260, 410, self)
        self.Window = UIWindow(self)
        ##print(sys.argv)
        self.setWindowTitle("Mon Snake")
        self.setStyleSheet("background-color: black")

        QtCore.QTimer.singleShot(1000, self.decompter)
        QtCore.QTimer.singleShot(2000, self.decompter)
        QtCore.QTimer.singleShot(3000, self.decompter)
        QtCore.QTimer.singleShot(4000, self.decompter)
        QtCore.QTimer.singleShot(5000, self.decompter)

        QtCore.QTimer.singleShot(6000, self.openMG)

        self.show()

    def openMG(self):
        self.close()
        self.newf = fenetreMG()

    def decompter(self):
        self.Window.dc -= 1
        self.Window.decompteur.setText("{0}".format(self.Window.dc))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())