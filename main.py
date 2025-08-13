# from PySide2.QtWidgets import (
#     QApplication, 
# )
# import sys

# from view import LayoutManager
# from model import DataModel
# from controller import LogicHandler

from  pprint import pprint
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
    QMenu      
)
from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent, QPixmap, QFont
from PySide2. QtCore import Qt, QUrl, Slot, Signal, QPoint
import sys, os
import random

DRIVE = "E:\\"

class TreeWidgetDragDrop(QTreeWidget):
    itemPathClicked = Signal(str)
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        # self.itemClicked.connect(self.on_item_clicked)

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


    def enterEvent(self, event):
        """When mouse enters widget"""
        self.setStyleSheet("""
            QTreeWidget::item {
                background-color: #F0F8FF;

            }
            QTreeWidget::item:hover {
                background-color: #778899;
            }
            QTreeWidget::item:selected {
                background-color: #5F9EA0;
                color: black;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """When mouse leaves widget"""
        self.setStyleSheet("""
            QTreeWidget::item {
                background-color: #F0F8FF;
            }
        """)
        super().leaveEvent(event)


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


class LayoutManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Manager")
        self.setGeometry(100,50, 1000, 450)

        self.scroll = QScrollArea()
        widget = QWidget()  
        self.mainvlay = QVBoxLayout()
        self.splitter = QSplitter(Qt.Horizontal)
        # self.wid_hlay = QHBoxLayout()
        self.tree_wid = None

        widget.setLayout(self.mainvlay)
        self.setCentralWidget(widget)

        self.add_menu()
        self.add_tree_wid()
        self.add_lst_wid()
        self.add_tab_wid()

        #self.mainvlay.addLayout(self.wid_hlay)
        # self.mainvlay.addLayout(self.splitter)
        self.mainvlay.addWidget(self.splitter)


    def add_ren_wid(self, info_wid_lst):

        for widget in info_wid_lst:
            list_item = QListWidgetItem()
            list_item.setSizeHint(widget.sizeHint())
            self.lst_wid.addItem(list_item)
            self.lst_wid.setItemWidget(list_item, widget)

        self.lst_wid.setSpacing(10)

        # print('self.scroll --- ', self.scroll)
        # print('self.scroll.viewport  --- ', self.scroll.viewport())
        # print('self.scroll.viewport.width --- ', self.scroll.viewport().width())

    def clear_lst_wid(self):
        self.lst_wid.clear()


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
        #self.wid_hlay.addWidget(self.tree_wid)
        self.splitter.addWidget(self.tree_wid)
        

    def add_lst_wid(self):
        self.lst_wid = QListWidget()
        #self.wid_hlay.addWidget(self.lst_wid)
        self.splitter.addWidget(self.lst_wid)

    def add_tab_wid(self):
        right_widget = QWidget()
        right_vlay = QVBoxLayout(right_widget)
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

        # self.wid_hlay.addLayout(right_vlay)
        
   
        self.splitter.addWidget(right_widget)


class LogicHandler():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.signal_slot()
        # self.tree_wid_drag_drop_handler = TreeWidgetDragDropHandler(view)
        # self.view.tree_wid.handler = self.tree_wid_drag_drop_handler

    def signal_slot(self):
        
        self.view.open_file_action.triggered.connect(self.open_file)
        self.view.open_folder_action.triggered.connect(self.open_folder)
        self.view.save_action.triggered.connect(self.save_file)
        self.view.save_as_action.triggered.connect(self.save_as_file)

        self.view.undo_action.triggered.connect(self.undo_last_action)
        self.view.redo_action.triggered.connect(self.redo_last_action)
        self.view.cut_action.triggered.connect(self.cut_selected_item)
        self.view.copy_action.triggered.connect(self.copy_selected_item)
        self.view.paste_action.triggered.connect(self.paste_item)

        self.view.tree_wid.itemClicked.connect(self.on_item_clicked)

        # self.exr_action.triggered.connect(self.load_in_viewer)


        # self.model.ver_wid.exr_action.triggered.connect(self.load_exr_in_viewer)


    def on_item_clicked(self, item, column):
        print("item --- ", item)
        print("column --- ", column)
        info_wid_lst = self.model.get_ren_info_wid(item, column)

        if info_wid_lst:
            self.view.add_ren_wid(info_wid_lst)
            for w in info_wid_lst:
                # w.exr_action.triggered.connect(self.load_exr_in_viewer)
                w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))
                # widget.menuRequested.connect(self.handle_context_menu)
        else:
            self.view.clear_lst_wid()


    def handle_context_menu(self, widget, pos):
        print("widget --- ", widget)
        print("pos --- ", pos)
        widget.populate_menu_actions(pos)
        # if widget.exr_action:
        widget.exr_action.triggered.connect(self.load_exr_in_viewer)
        widget.jpg_action.triggered.connect(self.load_jpg_in_viewer)
        widget.mov_action.triggered.connect(self.load_mov_in_viewer)

        widget.menu.exec_(widget.mapToGlobal(pos))
        print("***"*10)


    def load_exr_in_viewer(self):
        print("this is load_exr_in_viewer")

    def load_jpg_in_viewer(self):
        print("this is load_jpg_in_viewer")

    def load_mov_in_viewer(self):
        print("this is load_mov_in_viewer")

    def open_file(self):
        msg = self.model.get_file_data()
        print(msg)

    def open_folder(self):
        msg = self.model.get_folder_data()
        print(msg)

    def save_file(self):
        msg = self.model.save_execute()
        print(msg)

    def save_as_file(self):
        msg = self.model.save_as_execute()
        print(msg)

    def undo_last_action(self):
        msg = self.model.undo_operation()
        print(msg)

    def redo_last_action(self):
        msg = self.model.redo_operation()
        print(msg)

    def cut_selected_item(self):
        msg = self.model.cut_operation()
        print(msg)

    def copy_selected_item(self):
        msg = self.model.copy_operation()
        print(msg)

    def paste_item(self):
        msg = self.model.paste_operation()
        print(msg)


class RenderVersionWidget(QWidget):
    contextMenuRequested = Signal(QPoint)

    def __init__(self, ver_path):
        super().__init__()
        # self.exr_action = None

        # self.fixed_width = 400
        # self.setFixedWidth(self.fixed_width)


        self.set_style_sheet()   
        self.ver_path = ver_path

        self.mainhlay = QHBoxLayout(self)
        self.mainhlay.setContentsMargins(0,0,0,0)
        self.mainhlay.setSpacing(0)
        self.add_widgets()
        self.setLayout(self.mainhlay)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.populate_menu_actions)
        self.customContextMenuRequested.connect(self.contextMenuRequested)


        # self.context_menu_callback()

        


    def populate_menu_actions(self, pos):
        print('pos --- ', pos)
        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #f9f9f9;  /* Light background */
                border: 1px solid #ccc;     /* Light gray border */
                padding: 4px;
            }

            QMenu::item {
                background-color: transparent;
                padding: 4px 20px;
            }

            QMenu::item:selected {
                background-color: #e0e0e0;  /* Light gray when hovered */
                color: black;
            }

            QMenu::separator {
                height: 1px;
                background: #dcdcdc;
                margin: 4px 0;
            }
        """)

        self.play_menu = self.menu.addMenu("Load in Viewer")
        self.exr_action = self.play_menu.addAction("exr")
        # self.exr_action.triggered.connect(self.load_in_viewer)

        self.jpg_action = self.play_menu.addAction("jpg")
        self.mov_action = self.play_menu.addAction("mov")

        self.compare_action = self.menu.addAction("Compare")

        self.remove_menu = self.menu.addMenu("Remove")
        self.rm_single_action = self.remove_menu.addAction("Single")
        self.rm_multi_action = self.remove_menu.addAction("Multiple")

        # self.menu.exec_(self.mapToGlobal(pos))

        # if self.selected:
        #     print("self.selected --- ", self.selected.text())


    # def context_menu_callback(self):
    #     self.exr_action.triggered.connect(self.add_exr_in_player)


    def load_in_viewer(self):
        print("EXR clicked")


    def set_style_sheet(self):
        self.setStyleSheet("""
                border: 3px grey;
                background-color: #f5f5f5;
        """)


    def add_widgets(self):
        hlay = QHBoxLayout()

        image_full_path = os.path.join(self.ver_path, os.listdir(self.ver_path)[0])
        pixmap = QPixmap(image_full_path)
        scaled = pixmap.scaled(60, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
        lbl_thumbnil = QLabel()
        lbl_thumbnil.setPixmap(scaled)
        lbl_thumbnil.setAlignment(Qt.AlignCenter)
        lbl_thumbnil.setFixedWidth(50)

        hlay.addWidget(lbl_thumbnil)
  
        

        vlay = QVBoxLayout()
        vlay.setContentsMargins(2,0,0,0)

        image_nm = os.listdir(self.ver_path)[0]
        lbl_title = QLabel(f"  {image_nm.split('.')[0]}  ")
        font = QFont()
        font.setPointSize(10)
        lbl_title.setFont(font)

        first_frame = random.randint(1001, 1009)
        last_frame = random.randint(1100, 1200)
        lbl_info = QLabel(
            f"""  
            Project - {self.ver_path.split(os.sep)[2]}
            Shot - {self.ver_path.split(os.sep)[2]}
            Frame range - {first_frame} - {last_frame}  
        """
        )

        print("***"*10)
        pprint(lbl_info.text())
        print("***"*10)

        font.setPointSize(8)
        lbl_info.setFont(font)

        vlay.addWidget(lbl_title)
        vlay.addWidget(lbl_info)

        hlay.addLayout(vlay)

        self.mainhlay.addLayout(hlay)

    
    def enterEvent(self, event):
        self.setStyleSheet("background-color: #dcdcdc; border: 1px solid #ccc; padding: 1px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)



class DataModel():
    def __init__(self):
        self.ver_wid = None

    # @Slot(QTreeWidgetItem, int) 
    def get_ren_info_wid(self, item: QTreeWidgetItem, column: int):

        parts = []
        it = item
  
        while it is not None:
            parts.append(it.text(0))
            it = it.parent()
 
        parts.reverse()
        
        if parts[-1] == 'render':
            self.ren_dir_path = os.path.join(DRIVE, *parts)

            ver_widget_lst = []
            for ver in os.listdir(self.ren_dir_path):
                self.ver_wid = RenderVersionWidget(os.path.join(self.ren_dir_path, ver))
                # ver_wid.setStyleSheet("border: 3px double gray;")
                ver_widget_lst.append(self.ver_wid)

            if ver_widget_lst:
                return ver_widget_lst
            

    def get_file_data(self):
        return "file has been opened"

    def get_folder_data(self):
        return "Folder has been opened"
    
    def save_execute(self):
        return "file has been saved"
    
    def save_as_execute(self):
        return "file has been save as"


    def undo_operation(self):
        return "Undo last operation"

    def redo_operation(self):
        return "Redo last operation"
    
    def cut_operation(self):
        return "Cut operation"
    
    def copy_operation(self):
        return "Copy operation"

    def paste_operation(self):
        return "Paste Operation"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = DataModel()
    view = LayoutManager()
    controller = LogicHandler(model, view)
    view.show()
    sys.exit(app.exec_())



# des_path = r"E:\demo_projects\aawara\seq\aaw_000\aaw_000_0000\render"
# image_path = r"E:\demo_projects\aawara\seq\aaw_000\aaw_000_0000\scan\Capture001.png"
# import os
# import shutil
# for i in range(1,10):
#     destination_path = os.path.join(des_path, f"v00{i}")
#     os.makedirs(destination_path)
#     shutil.copy2(image_path, destination_path)


