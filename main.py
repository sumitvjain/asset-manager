# from qt_lib.qt_compact import *
from qt_lib import qt_compact #module 
from config import constant, settings
from view import view
from model import model, nuke_operation
from controller import controller
import sys, os



if __name__ == "__main__":
    app = qt_compact.QApplication(sys.argv)
    # app.setStyleSheet(open(STYLE_QSSPATH, "r").read())
    
    view = view.View(app)
    model = model.Model()   
    settings.setup_config()
    controller = controller.Controller(model, view, nuke_operation)
    view.show()
    sys.exit(app.exec_())
