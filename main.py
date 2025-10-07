from qt_lib.qt_compact import *
from config import constant, settings
from view import view
from model import model
from controller import controller
import sys, os



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(open(STYLE_QSSPATH, "r").read())
    
    view = view.View(app)
    model = model.Model()   
    settings.setup_config()
    controller = controller.Controller(model, view)
    view.show()
    sys.exit(app.exec_())
