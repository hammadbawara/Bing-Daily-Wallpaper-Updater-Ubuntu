from PyQt5 import QtCore, QtGui, QtWidgets
import os

CURRENT_WALLPAPER_PATH = f"/home/{os.getlogin()}/.wallpapers/current_wallpaper.txt"
WALLPAPER_FOLDER_PATH = f"/home/{os.getlogin()}/.wallpapers/"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image_view = QtWidgets.QLabel(self.centralwidget)
        self.image_view.setGeometry(QtCore.QRect(11, 11, 778, 478))
        self.image_view.setText("")
        self.image_view.setScaledContents(True)
        self.image_view.setObjectName("image_view")

        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{self.current_wallpaper}'))

        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(610, 510, 150, 50))
        self.nextBtn.setObjectName("nextBtn")
        self.prevBtn = QtWidgets.QPushButton(self.centralwidget)
        self.prevBtn.setGeometry(QtCore.QRect(20, 510, 150, 50))
        self.prevBtn.setObjectName("prevBtn")
        self.updateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.updateBtn.setGeometry(QtCore.QRect(300, 509, 161, 51))
        self.updateBtn.setObjectName("updateBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # click listeners
        self.nextBtn.clicked.connect(self.next_wallpaper)
        self.prevBtn.clicked.connect(self.prev_wallpaper)
        self.updateBtn.clicked.connect(self.update_and_set_wallpaper)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_and_set_wallpaper(self):
        os.system("python3 main.py -ds ")
        with open(CURRENT_WALLPAPER_PATH) as f:
            self.current_wallpaper = f.readline()
        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{self.current_wallpaper}'))

    def next_wallpaper(self):
        os.system("python3 main.py -next")
        with open(CURRENT_WALLPAPER_PATH) as f:
            self.current_wallpaper = f.readline()
        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{self.current_wallpaper}'))

    def prev_wallpaper(self):
        os.system("python3 main.py -prev")
        with open(CURRENT_WALLPAPER_PATH) as f:
            self.current_wallpaper = f.readline()
        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{self.current_wallpaper}'))


    def __init__(self):
        if not os.path.isfile(CURRENT_WALLPAPER_PATH):
            with open(CURRENT_WALLPAPER_PATH, "w") as f:
                f.write("default.jpg")
        with open(CURRENT_WALLPAPER_PATH) as f:
            self.current_wallpaper = f.readline()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nextBtn.setText(_translate("MainWindow", "Next"))
        self.prevBtn.setText(_translate("MainWindow", "Previous"))
        self.updateBtn.setText(_translate("MainWindow", "Update Wallpaper"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
