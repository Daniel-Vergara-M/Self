"Apps Menu Module"
from datetime import datetime
import os
from typing import Any
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess
from PyQt5 import uic

from utils import cwd, SubWindow
from utils.config import setConfig
from utils.setters import setText, connect
from utils.others import getText

from logic import database


class AppsMenu(SubWindow):
    "Subclass of `SubWindow`"

    def __init__(self, parent: Any, icon: QIcon, db: database.Database, thread: QProcess):
        '''

        Args:
            parent (Self): Different of of `self` but to implement inside other class with `self`
            icon (QIcon): Icon to be setted up in the GUI
            db (database.Database): Db where is going to look for items
            thread (QProcess): Thread where the programs will run from db
        '''
        super().__init__(size=(760, 680))
        self.icon = icon
        self.mp = parent
        self.db = db
        self.othread = thread
        self.connection = self.db.connection
        uic.loadUi(fr"{cwd}logic\apps\apps_menu.ui", self)
        setConfig(self, "Apps Menu", self.icon, (760, 680))

        self.actual: str = self.db.get_current_apps_path_apps()[0]

    def loadShow(self):
        "Loads, connects, sets and show GUI"
        setText(self, {
            "path_line": fr'"{self.actual}"'
        })
        connect(self, {
            "exit_button": self.close,
            "right_button": self.avanzar,
            "left_button": self.retroceder,
            "run_button": self.run
        })
        self.show()

    def avanzar(self):
        "Loops front through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.db.right_path()
            self.actual: Any = self.db.get_current_apps_path_apps()[0]
            setText(self, {"path_line": fr'"{self.actual}"'})

    def retroceder(self):
        "Loops back through the paths in database and sets it up in QLineEdit"
        with self.connection:
            self.db.left_path()
            self.actual: Any = self.db.get_current_apps_path_apps()[0]
            setText(self, {"path_line": fr'"{self.actual}"'})

    def run(self):
        "Runs the program displayed in QLineEdit"
        text = getText(self, "path_line")
        path = fr"{text}"
        date = datetime.now()
        cwd_log = os.getcwd()
        format_date = f"{date.day}-{date.month}-{date.year}_"
        format_hour = f"{date.hour}-{date.minute}-{date.second}"
        path_split = path.split("\\")
        name_with_exe = path_split[-1]
        name_without_exe = name_with_exe.removesuffix('.exe"')
        name = name_without_exe.title().lstrip().rstrip().strip()
        self.othread.setProgram(path)
        if name == "Code":
            self.othread.start(self.othread.program())
        else:
            self.othread.start(self.othread.program(), [
                               fr"> {cwd_log}\logs\log-{format_date+format_hour}.log"])
        format_date = format_date.replace("_", " ")
        print(
            f"[{format_date+format_hour}] - {name} (run)")