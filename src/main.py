import psutil
import time
import sys
import os

from threading import Thread

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Signal, Slot, QObject
from PySide6.QtGui import QPixmap

from ui.main_form import Ui_MainWindow

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class Process_kill_signal(QObject):
    Kill = Signal(bool)

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.proc_kill = Process_kill_signal()

        self.ico_file_path =resource_path("src/ico\warning.ico")
        self.ico = QPixmap( self.ico_file_path)
        self.label_pixmap.setPixmap(self.ico)

        self.target_process_names = ["target_process_name1", "target_process_name2"]
        self.pushButton_ok.clicked.connect(self.btn_ok_clicked_handler)

        self.proc_kill.Kill.connect(self.kill_process)

        self.work_thread = Thread(target=self.work, args=(self.target_process_names, self.proc_kill))
        self.work_thread.start()
    
    def btn_ok_clicked_handler(self):
        self.hide()

    def work(self, target_process_names, proc_kill : Process_kill_signal):
        while True:
            time.sleep(10)
            for proc in psutil.process_iter():
                process_name = proc.name()
                if process_name in target_process_names:
                    proc.kill()
                    proc_kill.Kill.emit(True)
    
    @Slot(bool)
    def kill_process(self, is_kill):
        if is_kill:
            self.show()
        
app = QApplication(sys.argv)
main_window = Mainwindow()
main_window.show()
app.setStyle('Fusion')
app.exec()