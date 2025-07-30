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
    QTabWidget
)
from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent
from PySide2. QtCore import Qt, QUrl
import sys, os



class TreeWidgetDragDrop(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event:QDragEnterEvent):
        if event.mimeData().hasUrls():
            print("dragEnterEvent --------- ")
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, e:QDragMoveEvent):
        if e.mimeData().hasUrls():
            print("dragMoveEvent --------- ")
            e.acceptProposedAction()
        else:
            e.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            drop_urls = event.mimeData().urls()
            url = drop_urls[0]
            path = url.toLocalFile()

            if os.path.isdir(path):
                if len(os.listdir(path)) > 0:
                    self.clear()

                    base_nm = os.path.basename(path)
                    tree_item = QTreeWidgetItem([base_nm, "Folder"])
                    self.addTopLevelItem(tree_item)

                    self.build_tree_view(path, tree_item)
                    event.accept()
                else:
                    print("Directory check complete: no content found.")
            else:
                print("This is not directory path")
                event.ignore()
        else:
            event.ignore()


    def build_tree_view(self, path, tree_item):
        dir_contents = os.listdir(path)

        for item in sorted(dir_contents):
            full_path = os.path.join(path, item)

            if os.path.isdir(full_path):
                folder_item = QTreeWidgetItem([item , "Folder"])
                tree_item.addChild(folder_item)
                self.build_tree_view(full_path, folder_item)
            
            elif os.path.isfile(full_path):
                file_item = QTreeWidgetItem([item, "File"])
                tree_item.addChild(file_item)


# class TreeWidgetDragDrop(QTreeWidget):
#     def __init__(self, handler=None):
#         super().__init__()
#         self.setAcceptDrops(True)
#         self.handler = handler

#     def dragEnterEvent(self, event):
#         if self.handler:
#             self.handler.dragEnterEvent(event)
#         else:
#             super().dragEnterEvent(event)

#     def dragMoveEvent(self, event):
#         if self.handler:
#             self.handler.dragMoveEvent(event)
#         else:
#             super().dragMoveEvent(event)

#     def dropEvent(self, event):
#         if self.handler:
#             self.handler.dropEvent(event)
#         else:
#             super().dropEvent(event)


class LayoutManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Manager")
        self.setGeometry(100,50, 1000, 450)

        widget = QWidget()  
        self.mainvlay = QVBoxLayout()
        self.wid_hlay = QHBoxLayout()

        widget.setLayout(self.mainvlay)
        self.setCentralWidget(widget)

        self.add_menu()
        self.add_tree_wid()
        self.add_lst_wid()
        self.add_tab_wid()

        self.mainvlay.addLayout(self.wid_hlay)


    def add_menu(self):
        menu = self.menuBar()

        # File menu
        file_menu = menu.addMenu("File")

        self.open_file_action = QAction("Open File", self)
        self.open_folder_action = QAction("Open Folder", self)
        self.save_action = QAction("Save", self)
        self.save_as_action = QAction("Save As...", self)

        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.open_folder_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)

        # Edit menu
        file_menu = menu.addMenu("Edit")

        self.undo_action = QAction("Undo", self)
        self.redo_action = QAction("Redo", self)
        self.cut_action = QAction("Cut", self)
        self.copy_action = QAction("Copy", self)
        self.paste_action = QAction("Paste", self)

        file_menu.addAction(self.undo_action)
        file_menu.addAction(self.redo_action)
        file_menu.addAction(self.cut_action)
        file_menu.addAction(self.copy_action)
        file_menu.addAction(self.paste_action)


    def add_tree_wid(self):
        # self.tree_wid = QTreeWidget()
        self.tree_wid = TreeWidgetDragDrop()
        self.wid_hlay.addWidget(self.tree_wid)
        

    def add_lst_wid(self):
        self.lst_wid = QListWidget()
        self.wid_hlay.addWidget(self.lst_wid)

    def add_tab_wid(self):
        right_vlay = QVBoxLayout()
        tab_vlay = QVBoxLayout()
        self.tab_wid = QTabWidget()

        self.tab_viewer = QWidget()


        info_hlay = QHBoxLayout()
        self.lbl_width = QLabel("Width: ")
        self.lbl_height = QLabel("Height: ")
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.lbl_frame = QLabel("Frame: ")

        info_hlay.addWidget(self.lbl_width)
        info_hlay.addWidget(self.lbl_height)
        info_hlay.addItem(spacer)
        info_hlay.addWidget(self.lbl_frame)

        btn_hlay = QHBoxLayout()
        self.btn_zoom_int = QPushButton("Zoom In")
        self.btn_zoom_out = QPushButton("Zoom Out")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")

        btn_hlay.addWidget(self.btn_zoom_int)
        btn_hlay.addWidget(self.btn_zoom_out)
        btn_hlay.addWidget(self.btn_play)
        btn_hlay.addWidget(self.btn_pause)
    
        tab_vlay.addWidget(self.tab_wid)
        tab_vlay.addLayout(info_hlay)    

        right_vlay.addLayout(tab_vlay)
        right_vlay.addLayout(btn_hlay)

        self.wid_hlay.addLayout(right_vlay)



