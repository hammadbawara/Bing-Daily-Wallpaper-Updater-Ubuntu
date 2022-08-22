import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

import WallpaperManager

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

        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{WallpaperManager.CURRENT_WALLPAPER}'))

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
        self.updateBtn.clicked.connect(self.update_wallpaper_btn_action)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_wallpaper_btn_action(self):
        #show progress dialog
        self.progress_dialog = QtWidgets.QProgressDialog(self.centralwidget)
        self.progress_dialog.setWindowTitle("Updating Wallpaper")
        self.progress_dialog.setLabelText("Checking for new wallpaper...")
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()
        self.progress_dialog.autoClose()

        #start thread to update wallpaper
        self.thread = QThread()
        self.worker = UpdateWallpaper()
        self.worker.start()


    def next_wallpaper(self):
        WallpaperManager.set_next_wallpaper()
        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{WallpaperManager.CURRENT_WALLPAPER}'))

    def prev_wallpaper(self):
        WallpaperManager.set_next_wallpaper(True)
        self.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{WallpaperManager.CURRENT_WALLPAPER}'))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nextBtn.setText(_translate("MainWindow", "Next"))
        self.prevBtn.setText(_translate("MainWindow", "Previous"))
        self.updateBtn.setText(_translate("MainWindow", "Update Wallpaper"))

class UpdateWallpaper(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        NEW_WALLPAPERS_LIST = []
        for i in range(0, 8):
            wallpaper = WallpaperManager.download(i)
            NEW_WALLPAPERS_LIST.append(wallpaper)
            ui.progress_dialog.setValue(int(((i+1)/7)*100))
        # Delete older wallpapers
        WallpaperManager.delete_older_wallpapers(NEW_WALLPAPERS_LIST)
        # Setting wallpaper
        WallpaperManager.set_wallpaper(NEW_WALLPAPERS_LIST[0])
        ui.image_view.setPixmap(QtGui.QPixmap(f'{WALLPAPER_FOLDER_PATH}/{WallpaperManager.CURRENT_WALLPAPER}'))
        ui.progress_dialog.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
