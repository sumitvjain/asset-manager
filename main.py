# from PySide2.QtWidgets import (
#     QApplication, 
# )
# import sys

# from view import view
# from model import Model
# from controller import Controller

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
    QMenu,
    QMessageBox,  
    QStyle
)
from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent, QPixmap, QFont, QWheelEvent
from PySide2.QtCore import Qt, QUrl, Slot, Signal, QPoint, QEvent, QObject
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
import sys, os
import random
import json
import platform

os_name = platform.system()

if os_name == "Windows":
    DRIVE = "E:\\"
    SPLIT_PATTERN = "\\"
    PLATFORM = "win"
elif os_name == "Linux":
    DRIVE = "/home/bhavana/sumit/python"
    SPLIT_PATTERN = "/"
    PLATFORM = "lin"



class TreeWidget(QTreeWidget):
    itemPathClicked = Signal(str)
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        # self.itemClicked.connect(self.on_item_clicked)

    def dragEnterEvent(self, event:QDragEnterEvent):
        if event.mimeData().hasUrls():
            # print("dragEnterEvent --------- ")
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, e:QDragMoveEvent):
        if e.mimeData().hasUrls():
            # print("dragMoveEvent --------- ")
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
                background-color: #B0C4DE;
            }
            QTreeWidget::item:selected {
                background-color: #20B2AA;
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
            QTreeWidget::item:selected {
                background-color: #F0F8FF;
                color: black;
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


class View(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Asset Manager")
        # self.set_style_sheet()
        # self.setGeometry(10,30, 1580, 800)
        # self.setFixedHeight(750)
        # self.setFixedWidth(1600)
        self.set_geometry(app)
        self.pixmap = None
        self.lbl_thumb_path = None
        # self.zoom_factor = 1.0
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
        self.add_viewer_wid()

        #self.mainvlay.addLayout(self.wid_hlay)
        # self.mainvlay.addLayout(self.splitter)
        self.mainvlay.addWidget(self.splitter)

    def set_geometry(self, app):
        screen = app.desktop().screenGeometry()
        width = screen.width()
        height = screen.height()
        self.setGeometry(0, 0, width, height)
        self.setMaximumWidth(width)
        self.setMaximumHeight(height)


    def set_style_sheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b; /* Dark VFX-style background */
            }

            QTabWidget::pane {
                border: 1px solid #444;
                background: #3c3c3c;
            }

            QTabBar::tab {
                background: #3c3c3c;
                color: #ddd;
                padding: 6px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }

            QTabBar::tab:selected {
                background: #5a5a5a;
                color: white;
            }

            QTreeWidget {
                background-color: #333;
                alternate-background-color: #3c3c3c;
                color: #ddd;
                border: 1px solid #555;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #5a87f7;
                color: white;
            }

            QListWidget {
                background-color: #333;
                alternate-background-color: #3c3c3c;
                color: #ddd;
                border: 1px solid #555;
            }
            QListWidget::item {
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #5a87f7;
                color: white;
            }
        """)

    def add_thumbnil_wid(self, thumbnil_wid_items_lst):

        for widget in thumbnil_wid_items_lst:
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
        self.tree_wid = TreeWidget()
        #self.wid_hlay.addWidget(self.tree_wid)
        self.splitter.addWidget(self.tree_wid)
        
    def add_lst_wid(self):
        lst_widget = QWidget()
        lst_vlay = QVBoxLayout(lst_widget)

        self.lbl_thumb_path = QLabel('')
        self.lbl_thumb_path.setStyleSheet("""
            QLabel {
                color: white;                
                background-color: #444444;    
                padding: 5px;               
                border-radius: 3px;    
            }       
        """)

        self.lst_wid = QListWidget()
        self.lst_wid.setSelectionMode(QListWidget.ExtendedSelection)
        #self.wid_hlay.addWidget(self.lst_wid)

        lst_vlay.addWidget(self.lbl_thumb_path)
        lst_vlay.addWidget(self.lst_wid)

        # self.splitter.addWidget(self.lst_wid)
        self.splitter.addWidget(lst_widget)
        
    def set_lbl_thumbnil_path(self, text):
        self.lbl_thumb_path.setText(f"Thumbnil Directory Path:\n{text}")
        font = QFont()
        font.setBold(True)
        font.setFamilies("Arial")
        self.lbl_thumb_path.setFont(font)


    def add_viewer_wid(self):
        self.viewer_wid = QWidget()
        right_vlay = QVBoxLayout(self.viewer_wid)
        tab_vlay = QVBoxLayout()
        self.tab_wid = QTabWidget()
        self.tab_wid.addTab(self.create_viewer_tab(), "Viewer")
        self.tab_wid.addTab(self.create_viewer_tab("metatab"), "Meta Data")

        # info_hlay = QHBoxLayout()
        # self.lbl_width = QLabel("Width: ")
        # self.lbl_height = QLabel("Height: ")
        # spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.lbl_frame = QLabel("Frame: ")

        # info_hlay.addWidget(self.lbl_width)
        # info_hlay.addWidget(self.lbl_height)
        # info_hlay.addItem(spacer)
        # info_hlay.addWidget(self.lbl_frame)

        # btn_hlay = QHBoxLayout()
        # self.btn_zoom_int = QPushButton("Zoom In")
        # self.btn_zoom_out = QPushButton("Zoom Out")
        # self.btn_play = QPushButton("Play")
        # self.btn_pause = QPushButton("Pause")

        # btn_hlay.addWidget(self.btn_zoom_int)
        # btn_hlay.addWidget(self.btn_zoom_out)
        # btn_hlay.addWidget(self.btn_play)
        # btn_hlay.addWidget(self.btn_pause)
    
        tab_vlay.addWidget(self.tab_wid)
        # tab_vlay.addLayout(info_hlay)    

        right_vlay.addLayout(tab_vlay)
        # right_vlay.addLayout(btn_hlay)
        
   
        self.splitter.addWidget(self.viewer_wid)

        # self.tab_wid.installEventFilter(self)

    def create_viewer_tab(self, meta=None):
        tab_view_wid = QWidget()
        tab_view_vlay_1 = QVBoxLayout()
        if meta is None:
            self.tab_view_lbl = QLabel()
            tab_view_vlay_1.addWidget(self.tab_view_lbl)
        tab_view_wid.setLayout(tab_view_vlay_1)
        return tab_view_wid


    def load_render_in_viewer(self, path):
        current_tab = self.tab_wid.currentWidget()
        label = current_tab.findChild(QLabel)

        self.pixmap = QPixmap(path)
        if not self.pixmap.isNull():
            self.tab_view_lbl.clear()
            self.tab_view_lbl.setAlignment(Qt.AlignCenter)
            # self.update_image_size()
 
        else:
            self.tab_view_lbl.clear()
            self.tab_view_lbl.setText("Image not found!")
            self.tab_view_lbl.setAlignment(Qt.AlignCenter)       


    

    # def update_image_size(self):
    #     if self.pixmap:
    #         scaled_pixmap = self.pixmap.scaled(
    #             self.tab_view_lbl.size() * self.zoom_factor,
    #             Qt.KeepAspectRatio,
    #             Qt.SmoothTransformation
    #         )
    #         self.tab_view_lbl.setPixmap(scaled_pixmap)

    def show_notification(self, msg):
        QMessageBox.information(self, "Action", msg)


    # def eventFilter(self, obj, event):
    #     if obj == self.tab_wid and event.type() == QEvent.Wheel:
    #         if self.tab_wid.underMouse():
    #             zoom_in = event.angleDelta().y() > 0

    #             if zoom_in:
    #                 self.zoom_factor *= 1.1
    #             else:
    #                 self.zoom_factor *= 0.9

    #             self.zoom_factor = max(0.1, min(self.zoom_factor, 10.0))

    #             self.update_image_size()
    #             event.accept()
    #         else:
    #             return True

    #     return super().eventFilter(obj, event)


    def wheelEvent(self, event: QWheelEvent):
        # self.tab_wid
        # zoom_in = event.angleDelta().y() > 0

        # if zoom_in:
        #     self.zoom_factor *= 1.1
        # else:
        #     self.zoom_factor *= 0.9

        # self.zoom_factor = max(0.1, min(self.zoom_factor, 10.0))

        # self.update_image_size()
        # event.accept()
        event.ignore()

    def remove_selected(self, widget):
        self.lst_wid.takeItem(widget)
        # sel_wid = invoked_action.parentWidget().parentWidget().parentWidget()
        # row = self.lst_wid.row(item)
        # self.lst_wid.takeItem(row)
        # row = self.list_widget.row(item)
        # self.list_widget.takeItem(row) 

        # -----------------------------------------------------
        # for i in range(self.lst_wid.count()):
        #     item = self.lst_wid.item(i)
        #     if self.lst_wid.itemWidget(item) == widget:
        #         self.lst_wid.takeItem(i)
        #         break
        # -----------------------------------------------------


class Controller(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.zoom_factor = 1.0
        self.signal_slot()
        # self.tree_wid_drag_drop_handler = TreeWidgetHandler(view)
        # self.view.tree_wid.handler = self.tree_wid_drag_drop_handler
        self.view.tab_wid.setFocusPolicy(Qt.StrongFocus)
        self.view.tab_wid.installEventFilter(self)

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
        # print("item --- ", item)
        # print("column --- ", column)
        thumbnil_wid_items_lst, thumb_dir_name = self.model.get_thumbnil_wid_lst(item, column)

        if thumbnil_wid_items_lst:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(thumb_dir_name)
            self.view.add_thumbnil_wid(thumbnil_wid_items_lst)

            for w in thumbnil_wid_items_lst:
                w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))

        else:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(thumb_dir_name)
            self.view.show_notification("Thumbnil not found.")

    def handle_context_menu(self, widget, pos):
        # print("widget --- ", widget)
        # print("pos --- ", pos)
        
        widget.populate_menu_actions(pos)

        # widget.exr_action.triggered.connect(self.load_exr_in_viewer)
        # widget.jpg_action.triggered.connect(self.load_jpg_in_viewer)
        # widget.mov_action.triggered.connect(self.load_mov_in_viewer)

        
        # widget.compare_action.triggered.connect(self.compare_versions)
        # widget.rm_single_action.triggered.connect(self.remove_version)
        # widget.rm_multi_action.triggered.connect(self.remove_multi_versions)

        self.action = widget.menu.exec_(widget.mapToGlobal(pos))

        if self.action:
            self.action_clicked(self.action, pos)

    def action_clicked(self, invoked_action, pos):

        if invoked_action.text() in ["exr", 'jpg', 'mov', 'png']:
            result, path = self.model.get_invoked_action_path(invoked_action)
            if result:
                print("path ----- ", path)
                self.view.load_render_in_viewer(path)
                self.update_image_size()
                self.view.show_notification("Successfully loaded into viewer.")
            else:
                self.view.show_notification(f"No [' {invoked_action.text()}' ] file was found.")
        elif self.action.text() == "Remove":
            # print("pos --- ", pos)
            # item = self.view.lst_wid.itemAt(pos)
            # print("item ---- ", item)
            selected_items = self.view.lst_wid.selectedItems()
            print("selected_items len -- ", len(selected_items))
            rows = sorted([self.view.lst_wid.row(it) for it in selected_items], reverse=True)

            for row in rows:
                self.view.remove_selected(row) 

            # for item in selected_items:
                
                # widget = self.view.lst_wid.row(item)
                # print("widget --- ", widget)
                # self.view.lst_wid.takeItem(row)   
                # self.view.remove_selected(item)         

            # widget = invoked_action.parent().parent()   
            # print("widget === ", widget)    
            # self.view.remove_selected(widget)

            # -----------------------------------------------------------------------------------------------------
            # child_widgets = invoked_action.parentWidget().parentWidget().parentWidget().findChildren(QWidget)
            # for child in child_widgets:
            #     if isinstance(child, QLabel):
            #         print("child text --- ", child.text())
            #     if child.objectName():
            #         print(f"{child.__class__.__name__} objectName: {child.objectName()}")
            # ------------------------------------------------------------------------------------------------------

            # self.load_exr_in_viewer()
        elif self.action.text() == "Compare":
            selected_items = self.view.lst_wid.selectedItems()
            if len(selected_items) == 2:
                self.view.show_notification("The selected version has been loaded into the viewer")
            else:       
                self.view.show_notification("You must select two items to proceed")




    def eventFilter(self, obj, event):
        if obj == self.view.tab_wid and event.type() == QEvent.Wheel:
            if self.view.tab_wid.underMouse():
                zoom_in = event.angleDelta().y() > 0

                if zoom_in:
                    self.zoom_factor *= 1.1
                else:
                    self.zoom_factor *= 0.9

                self.zoom_factor = max(0.1, min(self.zoom_factor, 10.0))

                self.update_image_size()
                event.accept()
            else:
                return True
            
        elif obj == self.view.tab_wid and event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Plus:
                self.zoom_factor *= 1.1
            elif key == Qt.Key_Minus:
                self.zoom_factor *= 0.9
                
            self.zoom_factor = max(0.1, min(self.zoom_factor, 10.0))
            self.update_image_size()
            event.accept()
            return True

        elif obj == self.view.tab_wid and event.type() == QEvent.MouseButtonPress:
            # when user clicks, give it focus
            self.view.tab_wid.setFocus()


        return super().eventFilter(obj, event)
    
    def update_image_size(self):
        if self.view.pixmap:
            scaled_pixmap = self.view.pixmap.scaled(
                self.view.tab_view_lbl.size() * self.zoom_factor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.view.tab_view_lbl.setPixmap(scaled_pixmap)


    # def load_exr_in_viewer(self):

        # print("self.action ----- ", dir(self.action))
        # print("this is load_exr_in_viewer")
        # self.model.get_exr_data()


    # def load_jpg_in_viewer(self):
    #     print("this is load_jpg_in_viewer")

    # def load_mov_in_viewer(self):
    #     print("this is load_mov_in_viewer")

    # def compare_versions(self):
    #     print("this is compare_versions")

    # def remove_version(self):
    #     print("this is remove_version")

    # def remove_multi_versions(self):
    #     print("this is remove_multi_versions")

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


class ThumbnilWidget(QWidget):
    contextMenuRequested = Signal(QPoint)

    # def __init__(self, ver_path):
    def __init__(self, img_data_dict):
        super().__init__()
        # self.exr_action = None

        # self.fixed_width = 400
        # self.setFixedWidth(self.fixed_width)

        self.set_style_sheet()   
        # self.ver_path = ver_path
        self.img_data_dict = img_data_dict

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
        # print('pos --- ', pos)
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


        self.remove_action = self.menu.addAction("Remove")
        self.compare_action = self.menu.addAction("Compare")

        # self.remove_menu = self.menu.addMenu("Remove")
        # self.rm_single_action = self.remove_menu.addAction("Single")
        # self.rm_multi_action = self.remove_menu.addAction("Multiple")

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
        # self.img_data_dict
        # ******************************
        # {'first_frame': 1004,
        # 'image_full_path': 'E:\\demo_projects_02\\proj_01\\seq\\proj_01_00\\proj_01_00_10\\render\\v002\\pexels-alexquezada-33041453.jpg',
        # 'last_frame': 1192,
        # 'lbl_title': 'pexels-alexquezada-33041453',
        # 'prj_code': 'proj_01',
        # 'shot_code': 'proj_01_00_10'}
        # ******************************

        hlay = QHBoxLayout()

        # image_full_path = os.path.join(self.ver_path, os.listdir(self.ver_path)[0])
        image_full_path = self.img_data_dict['image_full_path']
        pixmap = QPixmap(image_full_path)
        scaled = pixmap.scaled(60, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

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

        # image_nm = os.listdir(self.ver_path)[0]
        # lbl_title = QLabel(f"  {image_nm.split('.')[0]}  ")

        lbl_title = QLabel(f"  {self.img_data_dict['lbl_title']}  ")
        font = QFont()
        font.setPointSize(10)
        lbl_title.setFont(font)

        # first_frame = random.randint(1001, 1009)
        # last_frame = random.randint(1100, 1200)
        first_frame = self.img_data_dict['first_frame']
        last_frame = self.img_data_dict['last_frame']
        # lbl_info = QLabel(
        #     f"""  
        #     Project - {self.ver_path.split(os.sep)[2]}
        #     Shot - {self.ver_path.split(os.sep)[2]}
        #     Frame range - {first_frame} - {last_frame}  
        # """
        # )
        
        lbl_info = QLabel(
            f"""  
            Project - {self.img_data_dict['prj_code']}
            Shot - {self.img_data_dict['shot_code']}
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
        self.setStyleSheet("background-color: #B0C4DE; border: 1px solid #ccc; padding: 1px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)


class Model():
    def __init__(self):
        self.thumbnil_widget = None

    def get_invoked_action_path(self, invoked_action):
        child_widgets = invoked_action.parentWidget().parentWidget().parentWidget().findChildren(QWidget)
        if invoked_action.text() == "exr":
            for child in child_widgets:
                if isinstance(child, QLabel):
                    if child.text().startswith("Path"):
                        path = child.text().split("Path-")[-1]
                        return True, path
        else:
            return False, None

    # @Slot(QTreeWidgetItem, int) 
    def get_project_extension(self, proj_code):
        json_path = os.path.join(os.path.expanduser('~'), "Documents", ".app", "config.json" )
        try:
            with open(json_path, "r") as f:
                data = json.load(f)

            project = data.get(proj_code)
            if project:
                return project.get("extension", [])
            else:
                print(f"Project '{proj_code}' not found.")
                return []
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return []
    
    def get_thumbnil_wid_lst(self, item: QTreeWidgetItem, column: int):

        parts = []
        it = item
  
        while it is not None:
            parts.append(it.text(0))
            it = it.parent()
 
        parts.reverse()

        print("parts ---- ", parts)
        
        # ------------------------------------------------------------------------------------
        # ***** Do not delete, this working code, temporary off *****

        # if parts[-1] == 'render':
        #     self.thumbnil_dir_path = os.path.join(DRIVE, *parts)

        #     thumb_wid_lst = []
        #     for ver in os.listdir(self.thumbnil_dir_path):
        #         self.thumbnil_widget = ThumbnilWidget(os.path.join(self.thumbnil_dir_path, ver))
        #         # ver_wid.setStyleSheet("border: 3px double gray;")
        #         thumb_wid_lst.append(self.thumbnil_widget)

        #     if thumb_wid_lst:
        #         return thumb_wid_lst
        # ------------------------------------------------------------------------------------

        # image_full_path, image_nm, lbl_title,, first_frame, last_frame, prj_code, shot_code

        self.thumbnil_dir_path = os.path.join(DRIVE, *parts)

        print("self.thumbnil_dir_path --- ", self.thumbnil_dir_path)
        if PLATFORM == "lin":
            proj_code = self.thumbnil_dir_path.split(SPLIT_PATTERN)[6]
            
        elif PLATFORM == "win":
            pass

        file_exts = self.get_project_extension(proj_code)
        print("file_exts --- ", file_exts)

        thumbnil_data_dict_lst = []
        thumb_dir_name = ''
        if os.path.isdir(self.thumbnil_dir_path):
            thumb_dir_name = self.thumbnil_dir_path
            print("thumb_dir_name ---- ", thumb_dir_name)
         
            
            # -------------------------------------------------------------------------------------------
            # for file_name in os.listdir(self.thumbnil_dir_path):
            #     file_path = os.path.join(self.thumbnil_dir_path, file_name)


            #     if file_name.lower().endswith((".jpg", ".jpeg")):
            #         thumbnil_data_dict = {}
            #         image_full_path = os.path.join(self.thumbnil_dir_path, file_name)

            #         thumbnil_data_dict['lbl_title'] = file_name.split('.')[0]
            #         thumbnil_data_dict['image_full_path'] = image_full_path
            #         thumbnil_data_dict['first_frame'] = random.randint(1001, 1009)
            #         thumbnil_data_dict['last_frame'] = random.randint(1100, 1200)
            #         thumbnil_data_dict['prj_code'] = image_full_path.split("\\")[2]
            #         thumbnil_data_dict['shot_code'] =image_full_path.split("\\")[5]
            
            #         thumbnil_data_dict_lst.append(thumbnil_data_dict)
        

            # if thumbnil_data_dict_lst:
            #     thumb_wid_lst = []
            #     for img_data_dict in thumbnil_data_dict_lst:
            #         pprint(img_data_dict)
            #         print("***"*10)
            #         self.thumbnil_widget = ThumbnilWidget(img_data_dict)
            #         thumb_wid_lst.append(self.thumbnil_widget)
                        
            #     if thumb_wid_lst:
            #         return thumb_wid_lst
            # ------------------------------------------------------------------------------------------

            for file_name in os.listdir(self.thumbnil_dir_path):
                if file_name.lower().endswith((".jpg", ".jpeg")):
                    thumbnil_data_dict = self.get_thumb_data_dict(file_name, is_thumb_dir=True)
                    thumbnil_data_dict_lst.append(thumbnil_data_dict)


        # ******************************
        # self.thumbnil_dir_path ---  E:\demo_projects_02\proj_01\seq\proj_01_00\proj_01_00_10\render\v008
        # {'first_frame': 1009,
        # 'image_full_path': 'E:\\demo_projects_02\\proj_01\\seq\\proj_01_00\\proj_01_00_10\\render\\v008\\pexels-alana-sousa-1723789-17476693.jpg',
        # 'last_frame': 1106,
        # 'lbl_title': 'pexels-alana-sousa-1723789-17476693',
        # 'prj_code': 'proj_01',
        # 'shot_code': 'proj_01_00_10'}
        # ******************************
        # ******************************
        # ('  \n'
        # '            Project - proj_01\n'
        # '            Shot - proj_01_00_10\n'       
        # '            Frame range - 1009 - 1106  \n'
        # '        ')
        # ******************************

        elif os.path.isfile(self.thumbnil_dir_path):
            thumb_dir_name = os.path.dirname(self.thumbnil_dir_path)
            print("thumb_dir_name === ", thumb_dir_name)
            # file_name = self.thumbnil_dir_path.split("\\")[-1]
            
            file_name = self.thumbnil_dir_path.split(SPLIT_PATTERN)[-1]
            print("file_name ---- ", file_name)
            if file_name.lower().endswith((".jpg", ".jpeg")):
                thumbnil_data_dict = self.get_thumb_data_dict(file_name, is_thumb_dir=False)
                print("thumbnil_data_dict --- ", thumbnil_data_dict)
                thumbnil_data_dict_lst.append(thumbnil_data_dict)

        if thumbnil_data_dict_lst:
            thumb_wid_lst = []
            for img_data_dict in thumbnil_data_dict_lst:
                pprint(img_data_dict)
                print("***"*10)
                self.thumbnil_widget = ThumbnilWidget(img_data_dict)
                thumb_wid_lst.append(self.thumbnil_widget)
                    
            if thumb_wid_lst:
                return thumb_wid_lst, thumb_dir_name
        else:
            print("empty thumb list")
            return [], self.thumbnil_dir_path
         
    def get_thumb_data_dict(self, file_name, is_thumb_dir=None):
        # if file_name.lower().endswith((".jpg", ".jpeg")):
        thumbnil_data_dict = {}
        if is_thumb_dir:
            image_full_path = os.path.join(self.thumbnil_dir_path, file_name)
        else:
            image_full_path = self.thumbnil_dir_path

        thumbnil_data_dict['lbl_title'] = file_name.split('.')[0]
        thumbnil_data_dict['image_full_path'] = image_full_path
        thumbnil_data_dict['first_frame'] = random.randint(1001, 1009)
        thumbnil_data_dict['last_frame'] = random.randint(1100, 1200)

        # thumbnil_data_dict['prj_code'] = image_full_path.split("\\")[2]
        # thumbnil_data_dict['shot_code'] =image_full_path.split("\\")[5]
        thumbnil_data_dict['prj_code'] = image_full_path.split(SPLIT_PATTERN)[2]
        thumbnil_data_dict['shot_code'] =image_full_path.split(SPLIT_PATTERN)[5]
        
        return thumbnil_data_dict
            
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



def create_json_file(app_dir_path):
    jsn_fle_pth = os.path.join(app_dir_path, 'config.json')
    # json_data = get_default_data()

    project = {}
    for num in range(1, 11):
        project[f"proj_{num:02}"] = {
            "name": f"Project_{num:02}", 
            "extension": ["jpeg"]
            }

    with open(jsn_fle_pth, "w") as json_file:
        json.dump(project, json_file, indent=4)
    print(f"[config.json] created successfully! \n {jsn_fle_pth}")


def setup_config():
    home_dir = os.path.expanduser('~')
    documents_path = os.path.join(home_dir, "Documents")
    documents_dir_lst = os.listdir(documents_path)
    app_dir_path = os.path.join(documents_path, ".app")

    if not ".app" in documents_dir_lst:       
        os.makedirs(app_dir_path)
        create_json_file(app_dir_path)

    elif not "config.json" in os.listdir(app_dir_path):
        create_json_file(app_dir_path)
 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = View(app)
    setup_config()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())





# def update_json_file(documents_path):
#     jsn_fle_pth = os.path.join(documents_path, ".app", 'config.json')

#     with open(jsn_fle_pth, "r") as f:
#         json_data = json.load(f)

#     json_data["proj_1"]["extension"] = ["jpeg", "jpg"]
#     json_data["proj_2"]["extension"] = ["jpeg", "jpg", "exr"]

#     with open(jsn_fle_pth, "w") as f:
#         json.dump(json_data, f, indent=4)

#     print("JSON file updated successfully!")