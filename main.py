# from PySide2.QtWidgets import QApplication
from qt_lib.qt_compact import *

# from Qt.QtWidgets import *
# from Qt.QtGui import *
# from Qt.QtCore import *
# from Qt.QtMultimedia import *

import sys, os

from config import constant, settings
from view import view
from model import model
from controller import controller

# con = constant.Constant()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(open(STYLE_QSSPATH, "r").read())
    
    view = view.View(app)
    model = model.Model()   
    settings.setup_config()
    controller = controller.Controller(model, view)
    view.show()
    sys.exit(app.exec_())
