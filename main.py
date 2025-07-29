from PySide2.QtWidgets import (
    QApplication, 
)
import sys

from view import LayoutManager
from model import DataModel
from controller import LogicHandler


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = DataModel()
    view = LayoutManager()
    controller = LogicHandler(model, view)
    view.show()
    sys.exit(app.exec_())





