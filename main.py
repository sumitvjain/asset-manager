from PySide2.QtWidgets import (
    QMainWindow, QSizePolicy, QSpacerItem,
    QWidget,
    QVBoxLayout, 
    QHBoxLayout, 
    QApplication, 
    QAction,
    QListWidget,
    QListWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
    QPushButton,
    QTabWidget
)
import sys

from view import LayoutManager
from model import DataModel
from controller import LogicHandler



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # win = AssetManager()

    model = DataModel()
    view = LayoutManager()
    controller = LogicHandler(model, view)
    view.show()
    sys.exit(app.exec_())





