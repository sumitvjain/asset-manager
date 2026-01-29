# from qt_lib.qt_compact import *
import sys
from pathlib import Path
from qt_lib import qt_compact #module 
from PySide2.QtGui import QFontDatabase
import qdarkstyle

from view import view
from model import model
from controller import controller
from config import constant, settings




if __name__ == "__main__":
    app = qt_compact.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    qss_file = Path("resources/styles.qss")
    if qss_file.exists():
        app.setStyleSheet(app.styleSheet() + qss_file.read_text())
    else:
        print('no'*10)

    view = view.View(app)
    model = model.Model()  

    settings.setup_config()

    controller = controller.Controller(model, view)
    
    view.show()
    sys.exit(app.exec_())


#######################

