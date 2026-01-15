# from qt_lib.qt_compact import *
import sys
from qt_lib import qt_compact #module 
from PySide2.QtGui import QFontDatabase
import qdarkstyle

from view import view
from model import model, nuke_operation
from controller import controller
from config import constant, settings




if __name__ == "__main__":
    app = qt_compact.QApplication(sys.argv)
    # app.setStyleSheet(open(STYLE_QSSPATH, "r").read())
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    # import qt_material AFTER QApplication exists
    # from qt_material import apply_stylesheet

    view = view.View(app)
    model = model.Model()   
    settings.setup_config()
    controller = controller.Controller(model, view, nuke_operation)
    view.show()
    sys.exit(app.exec_())




