from PySide2.QtWidgets import QApplication

# from Qt.QtWidgets import *
# from Qt.QtGui import *
# from Qt.QtCore import *
# from Qt.QtMultimedia import *

import sys, os

from config import constant, settings
from view import view
from model import model
from controller import controller

con = constant.Constant()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(open(STYLE_QSSPATH, "r").read())
    model = model.Model()
    view = view.View(app)
    settings.setup_config()
    controller = controller.Controller(model, view)
    view.show()
    sys.exit(app.exec_())
