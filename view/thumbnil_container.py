from PySide2.QtWidgets import (
    QMainWindow, QSizePolicy, QSpacerItem, QAbstractItemView,
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QApplication, 
    QAction,
    QListWidget,
    QListWidgetItem,
    QTreeWidgetItem,
    QTreeWidget,
    QLabel,
    QPushButton,
    QTabWidget,
    QSplitter,
    QScrollArea,
    QGridLayout,
    QSizePolicy,
    QMenu,
    QMessageBox,  
    QStyle,
    QDialog,
    QComboBox
)
from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent, QPixmap, QFont, QWheelEvent, QIcon
from PySide2.QtCore import Qt, QUrl, Slot, Signal, QPoint, QEvent, QObject, QSize, QThread, QThreadPool, QRunnable
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent

# from Qt.QtWidgets import *
# from Qt.QtGui import *
# from Qt.QtCore import *
# from Qt.QtMultimedia import *


from  pprint import pprint
import sys, os
import random
import json



class ThumbnilWidget(QWidget):
    contextMenuRequested = Signal(QPoint)

    def __init__(self, img_data_dict):
        super().__init__()
        self.set_style_sheet()   
        self.img_data_dict = img_data_dict

        self.mainhlay = QHBoxLayout(self)
        self.mainhlay.setContentsMargins(0,0,0,0)
        self.mainhlay.setSpacing(0)

        self.add_widgets()
        self.setLayout(self.mainhlay)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuRequested)

    def populate_menu_actions(self, pos):   
        self.menu = QMenu(self)

        self.menu.setStyleSheet("""
            /* ---------------- QMenu ---------------- */
            QMenu {
                background-color: #333;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px;
            }

            QMenu::item {
                padding: 6px 24px;
                margin: 2px;
                border-radius: 4px;
                color: #e6e6e6;
                border: 1px solid transparent; /* default no border */
            }

            /* Hover effect */
            QMenu::item:hover {
                background-color: rgba(90, 135, 247, 0.15); /* subtle accent */
                border: 1px solid #5a87f7;
                color: #ffffff;
            }

            /* Selected (clicked/active) */
            QMenu::item:selected {
                background-color: #5a87f7;
                border: 1px solid #3f73ff;
                color: #ffffff;
            }

            /* Disabled item */
            QMenu::item:disabled {
                color: #666;
                border: 1px solid transparent;
                background: transparent;
            }

            /* Separator line */
            QMenu::separator {
                height: 1px;
                background: #444;
                margin: 4px 8px;
            }

            /* Submenu indicator (arrow) */
            QMenu::indicator {
                width: 14px;
                height: 14px;
            }
        """)
 
        self.laod_action = self.menu.addAction("Load in Viewer")

        self.remove_action = self.menu.addAction("Remove")
        self.compare_action = self.menu.addAction("Compare")
        self.set_thumb_background_color()

    def load_in_viewer(self):
        print("EXR clicked")

    def add_widgets(self):
        hlay = QHBoxLayout()
        image_full_path = self.img_data_dict['image_full_path']
        pixmap = QPixmap(image_full_path)
        scaled = pixmap.scaled(120, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        lbl_full_path = QLabel()
        lbl_full_path.setText(f"Path-{image_full_path}")
        lbl_full_path.setHidden(True)

        lbl_thumbnil = QLabel()
        lbl_thumbnil.setPixmap(scaled)
        lbl_thumbnil.setAlignment(Qt.AlignCenter)
        lbl_thumbnil.setFixedWidth(50)

        hlay.addWidget(lbl_full_path)
        hlay.addWidget(lbl_thumbnil)   

        vlay = QVBoxLayout()
        vlay.setContentsMargins(2,0,0,0)

        lbl_title = QLabel(f"  {self.img_data_dict['lbl_title']}  ")
        lbl_title.setStyleSheet("text-transform: uppercase;")
        font = QFont()
        font.setPointSize(10)
        lbl_title.setFont(font)

        first_frame = self.img_data_dict['first_frame']
        last_frame = self.img_data_dict['last_frame']

        lbl_info = QLabel(
            f"""  
            Project - {self.img_data_dict['prj_code']}
            Shot - {self.img_data_dict['shot_code']}
            Frame range - {first_frame} - {last_frame}  
        """
        )

        self.setStyleSheet("""
            QLabel {
                color: white;                
                background-color: #4d4d4d;         
                padding: 5px;               
                border: 1px solid #444;
                border-radius: 3px;
            }       
        """)

        font.setPointSize(8)
        lbl_info.setFont(font)

        vlay.addWidget(lbl_title)
        vlay.addWidget(lbl_info)

        hlay.addLayout(vlay)
        self.mainhlay.addLayout(hlay)

    def set_style_sheet(self):
        # background-color: #006bb3;
        self.setStyleSheet("""
            QLabel {
                color: white;                
                background-color: #4d4d4d;         
                padding: 5px;               
                border: 1px solid #444;
                border-radius: 3px;
            }       
        """)


    def set_thumb_background_color(self):
        self.setStyleSheet("background-color: #B0C4DE; border: 1px solid #ccc; padding: 1px;") # ** this is important line **

    def enterEvent(self, event):
        self.set_thumb_background_color()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.set_style_sheet()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.set_thumb_background_color()
        return super().mousePressEvent(event)
    
    # def mouseReleaseEvent(self, event):
    #     self.set_thumb_background_color()
    #     return super().mouseReleaseEvent(event)
