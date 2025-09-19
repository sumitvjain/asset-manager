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
    QStyle,
    QDialog,
    QComboBox
)
from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent, QPixmap, QFont, QWheelEvent, QIcon
from PySide2.QtCore import Qt, QUrl, Slot, Signal, QPoint, QEvent, QObject, QSize, QThread, QThreadPool, QRunnable
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
import sys, os
import random
import json

from platformdirs import user_documents_dir
from pathlib import Path
import re



DOCUMENTS_DIRPATH = user_documents_dir()

APP_DIRNAME = ".app"
CONFIG_FILENAME = "config.json"
AVAILABLE_EXTENSIONS = ["exr", "jpeg", "jpg", "png", "mov"]
DEFAULT_ENABLED_EXTS = {"jpeg", "jpg"}
CONFIG_FILEPATH = Path(DOCUMENTS_DIRPATH) / APP_DIRNAME / CONFIG_FILENAME



class PreferencesDialog(QDialog):
    def __init__(self, existing_prefs_data, parent=None, ):
        super().__init__(parent)
        self.existing_prefs_data = existing_prefs_data
        # self.ext_lst = ["exr", "jpeg", "jpg", "png", "mov"]
        self.config_file_path = CONFIG_FILEPATH
        self.setWindowTitle("Application Preferences")
        icon_path = Path.cwd() / "icon" / "gear_cog_wheel.jpg"
        self.setWindowIcon(QIcon(str(icon_path)))
        self.dialog_vlay = QVBoxLayout()
        self.add_widgets()
        self.setLayout(self.dialog_vlay)


    def add_widgets(self):
        hbox_lay_01 = QHBoxLayout()     
        proj_lbl = QLabel("Project:")
        self.proj_combo = QComboBox()      
        existing_prefs_proj_lst = list(self.existing_prefs_data.keys())
        self.proj_combo.addItems(['-- Select Project --'] + existing_prefs_proj_lst)
        

        hbox_lay_01.addWidget(proj_lbl)
        hbox_lay_01.addWidget(self.proj_combo)
        self.dialog_vlay.addLayout(hbox_lay_01)

        self.lst_wid = QListWidget()
        self.dialog_vlay.addWidget(self.lst_wid)

        self.info_lbl = QLabel()
        self.dialog_vlay.addWidget(self.info_lbl)

        btn_hlay = QHBoxLayout()
        self.close_btn = QPushButton("Close")
        icon = QApplication.style().standardIcon(QStyle.SP_DialogCloseButton)
        self.close_btn.setIcon(icon)


        self.update_btn = QPushButton("Update")
        icon = QApplication.style().standardIcon(QStyle.SP_DialogOkButton)
        self.update_btn.setIcon(icon)
        self.toggle_button_state()

        btn_hlay.addWidget(self.close_btn)
        btn_hlay.addWidget(self.update_btn)
        self.dialog_vlay.addLayout(btn_hlay)

    # def fetch_project_extensions(self, selected_proj):
    #     with open(self.config_file_path, "r") as rd:
    #         config_data = json.load(rd)

    #     raw_ext_dict = config_data[selected_proj]['extension']
    #     supported_ext_lst = []

    #     for ext_key in raw_ext_dict.keys():
    #         if raw_ext_dict[ext_key] == True:
    #             supported_ext_lst.append(ext_key)

    #     return supported_ext_lst

    def set_extension_lst(self, supported_ext_lst):
        selected_proj = self.get_current_project_code()
        if selected_proj != '-- Select Project --':
            self.lst_wid.clear()
            # supported_ext_lst = self.fetch_project_extensions(selected_proj)

            # if supported_ext_lst:

            print("AVAILABLE_EXTENSIONS ---- ", AVAILABLE_EXTENSIONS)
            for ext in AVAILABLE_EXTENSIONS:
                item = QListWidgetItem(ext)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                # if ext in proj_ext_lst:
                if ext in supported_ext_lst:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)

                self.lst_wid.addItem(item)
 
        elif selected_proj == '-- Select Project --':
            self.lst_wid.clear()

        self.toggle_button_state()

    def get_checked_extension(self):
        self.checked_item_nm_lst = []
        for item_index in range(self.lst_wid.count()):
            lst_item = self.lst_wid.item(item_index)
            if lst_item.checkState() == Qt.Checked:
                self.checked_item_nm_lst.append(lst_item.text())

        return self.checked_item_nm_lst

    def toggle_button_state(self):
        if self.proj_combo.currentText()  == '-- Select Project --':
            self.update_btn.setEnabled(False)
        else:
            self.update_btn.setEnabled(True)

    def get_current_project_code(self):
        return self.proj_combo.currentText()


class TreeWidgetWorker(QObject):
    # tree_wid_itm_proc = Signal(QTreeWidgetItem)
    # tree_bld_proc = Signal(str, QTreeWidgetItem)
    tree_data_ready = Signal(str, dict)
    finished = Signal()
    print("111")

    def __init__(self, folder_tree_data_lst):
        super().__init__()
        self.folder_tree_data_lst = folder_tree_data_lst
        print("222")

    def run(self):
        print("444")
        for dict_itm in self.folder_tree_data_lst:
            base_nm = list(dict_itm.keys())[0]
            path = dict_itm[base_nm]["path"]
            print("base_nm --- ", base_nm)
            print("path ---- ", path)
            # tree_item = QTreeWidgetItem([base_nm, "Folder"]) 
            # self.tree_wid_itm_proc.emit(tree_item)
            # self.tree_bld_proc.emit(path, tree_item)

            self.tree_data_ready.emit(base_nm, dict_itm[base_nm])

        self.finished.emit()


class TreeWidget(QTreeWidget):  
    # itemPathClicked = Signal(str)
    filesDropped = Signal(list)
    
    def __init__(self):
        super().__init__()
        # self.drive = None
        self.thread_obj_lst = []
        self.path_item_pairs = []
        self.setHeaderHidden(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event:QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, e:QDragMoveEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
        else:
            e.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            drop_urls = event.mimeData().urls()
            self.filesDropped.emit(drop_urls)
            # event.accept() 
        else:
            event.ignore()

    # --------------------------------------------------------------------------------
    # This is fully working code
    # def dropEvent(self, event):
    
    #     if event.mimeData().hasUrls():
    #         drop_urls = event.mimeData().urls()
    #         self.clear()

    #         for url in drop_urls:
    #             path = url.toLocalFile() 
    #             if self.drive == None:
    #                 self.drive = re.split(r"[\\/]", path)[0]

    #             if os.path.isdir(path):
    #                 if len(os.listdir(path)) > 0:
    #                     base_nm = os.path.basename(path)
    #                     tree_item = QTreeWidgetItem([base_nm, "Folder"])   

    #                     # ----------------------------------------------------------
    #                     # This is working code without thread
    #                     self.addTopLevelItem(tree_item)
    #                     self.build_tree_view(path, tree_item)
    #                     event.accept()  
    #                     # ----------------------------------------------------------   


    #                 else:
    #                     print("Directory check complete: no content found.")
    #             else:
    #                 print("This is not directory path")
    #                 event.ignore()
    #         else:
    #             event.ignore()
    #  ---------------------------------------------------------------------------------

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

    # def tree_wid_itm_processed(self, tree_item):
    #     self.addTopLevelItem(tree_item)

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


    def process_tree_data(self, base_nm, data):
        path = data["path"]
        tree_item = QTreeWidgetItem([base_nm, "Folder"]) 
        self.addTopLevelItem(tree_item)
        self.build_tree_view(path, tree_item)



    def load_folder_tree_into_ui(self, folder_tree_data_lst):
        # ---------------------------------------------------------------------
        # This code with qthread

        self.clear()
        self.thread_obj = QThread()

        self.tree_worker = TreeWidgetWorker(folder_tree_data_lst)
        self.tree_worker.moveToThread(self.thread_obj)

        self.thread_obj.started.connect(self.tree_worker.run)

        # self.tree_worker.tree_wid_itm_proc.connect(self.tree_wid_itm_processed)
        # self.tree_worker.tree_bld_proc.connect(self.build_tree_view)

        self.tree_worker.tree_data_ready.connect(self.process_tree_data)

        self.tree_worker.finished.connect(self.thread_obj.quit)
        self.tree_worker.finished.connect(self.tree_worker.deleteLater)

        self.thread_obj.finished.connect(self.thread_obj.deleteLater)
        self.thread_obj.start()
        # ---------------------------------------------------------------------


        # ********************************************************************
        # This code for without qthread

        # self.clear()
        # for dict_itm in folder_tree_data_lst:
        #     base_nm = list(dict_itm.keys())[0]
        #     path = dict_itm[base_nm]["path"]
        #     print("base_nm --- ", base_nm)
        #     print("path ---- ", path)
        #     tree_item = QTreeWidgetItem([base_nm, "Folder"]) 
        #     self.addTopLevelItem(tree_item)
        #     self.build_tree_view(path, tree_item)
        # ********************************************************************


class View(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Asset Manager")
        self.set_geometry(app)

        self.pixmap = None
        self.lbl_thumb_path = None
        self.tree_wid = None

        self.scroll = QScrollArea()
        widget = QWidget()  
        self.mainvlay = QVBoxLayout()
        self.splitter = QSplitter(Qt.Horizontal)
        
        widget.setLayout(self.mainvlay)
        self.setCentralWidget(widget)

        self.add_menu()
        self.add_tree_wid()
        self.add_lst_wid()
        self.add_viewer_wid()

        self.mainvlay.addWidget(self.splitter)

    def set_geometry(self, app):
        screen = app.primaryScreen().geometry()
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

        # Preferences menu
        preferences_menu = menu.addMenu("Preferences")
        self.preferences_action = QAction("Configuration Settings", self)

        preferences_menu.addAction(self.preferences_action)

    def add_tree_wid(self):
        self.tree_wid = TreeWidget()
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
   
        tab_vlay.addWidget(self.tab_wid)
        right_vlay.addLayout(tab_vlay)    
        self.splitter.addWidget(self.viewer_wid)

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
        else:
            self.tab_view_lbl.clear()
            self.tab_view_lbl.setText("Image not found!")
            self.tab_view_lbl.setAlignment(Qt.AlignCenter)       

    def open_pref_dialog(self, existing_prefs_data):
        prefs_window = PreferencesDialog(existing_prefs_data, self)
        if prefs_window:
            prefs_window.show()

        return prefs_window

    def show_notification(self, msg):
        QMessageBox.information(self, "Action", msg)

    def wheelEvent(self, event: QWheelEvent):
        event.ignore()

    def remove_selected(self, widget):
        self.lst_wid.takeItem(widget)

    # def load_folder_tree_into_ui(self, folder_tree_data_lst):
    #     print("len --- ", len(folder_tree_data_lst))


class TreeItemClickSignals(QObject):
    custom_context = Signal(list)
    completed = Signal()

class TreeItemClickWorkerPool(QRunnable):
    def __init__(self, thumbnil_wid_items_lst, thumb_dir_name, msg):
        super().__init__()
        self.thumbnil_wid_items_lst = thumbnil_wid_items_lst
        self.thumb_dir_name = thumb_dir_name
        self.msg = msg

        self.signal_obj = TreeItemClickSignals()

    def run(self):
        if self.thumbnil_wid_items_lst:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(self.thumb_dir_name)
            self.view.add_thumbnil_wid(self.thumbnil_wid_items_lst)

            self.signal_obj.custom_context.emit(self.thumbnil_wid_items_lst)

        else:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(self.thumb_dir_name)
            self.view.show_notification(self.msg)

        self.signal_obj.completed.emit()


class Controller(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.zoom_factor = 1.0
        self.signal_slot()
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
        self.view.preferences_action.triggered.connect(self.preferences_clicked)

        self.view.tree_wid.itemClicked.connect(self.on_item_clicked)
        self.view.tree_wid.filesDropped.connect(self.on_files_dropped)

    def proj_combo_index_changed(self):
        proj_code = self.prefs_window.get_current_project_code()
        # ext_list = self.model.get_project_extension(proj_code)
        ext_list = self.model.fetch_project_extensions(proj_code)
        print("ext_list ---- ", ext_list)
        
        self.prefs_window.set_extension_lst(ext_list)

    def update_btn_clicked(self):
        new_extensions = self.prefs_window.get_checked_extension()
        print("new_extensions --- ", new_extensions)
        selected_proj = self.prefs_window.proj_combo.currentText() 
        self.model.overwrite_config(new_extensions, selected_proj)

    def on_item_clicked(self, item, column):
        # This code is without threadpool
        # thumbnil_wid_items_lst, thumb_dir_name, msg = self.model.get_thumbnil_wid_lst(item, column)

        # if thumbnil_wid_items_lst:
        #     self.view.clear_lst_wid()
        #     self.view.set_lbl_thumbnil_path(thumb_dir_name)
        #     self.view.add_thumbnil_wid(thumbnil_wid_items_lst)

        #     for w in thumbnil_wid_items_lst:
        #         w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))

        # else:
        #     self.view.clear_lst_wid()
        #     self.view.set_lbl_thumbnil_path(thumb_dir_name)
        #     self.view.show_notification(msg)

        # ---------------------------------------------------------------------------------------------
       
        # This is with threadpool

        thumbnil_wid_items_lst, thumb_dir_name, msg = self.model.get_thumbnil_wid_lst(item, column)
        thread_pool = QThreadPool.globalInstance()

        tree_item_click_worker_pool = TreeItemClickWorkerPool(thumbnil_wid_items_lst, thumb_dir_name, msg)

        tree_item_click_worker_pool.signal_obj.custom_context.connect(self.thumbnail_contextc_action)
        tree_item_click_worker_pool.signal_obj.completed.connect(self.on_task_completed)

        thread_pool.start(tree_item_click_worker_pool)


    def on_task_completed(self):
        print("*** Thumbnil task completed ***")

    def thumbnail_contextc_action(self, thumbnil_wid_items_lst):
        for w in thumbnil_wid_items_lst:
            w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))

    def on_files_dropped(self, drop_urls):
        folder_tree_data_lst = self.model.get_urls_data(drop_urls)
        self.view.tree_wid.load_folder_tree_into_ui(folder_tree_data_lst)


    def handle_context_menu(self, widget, pos):        
        widget.populate_menu_actions(pos)
        self.action = widget.menu.exec_(widget.mapToGlobal(pos))

        if self.action:
            self.action_clicked(self.action, pos)

    def action_clicked(self, invoked_action, pos):

        print("invoked_action --- ", invoked_action.text())
        # if invoked_action.text() in ["exr", 'jpg', 'mov', 'png']:
        if invoked_action.text() == "Load in Viewer":
            result, path = self.model.get_invoked_action_path(invoked_action)
            if result:
                self.view.load_render_in_viewer(path)
                self.update_image_size()
                self.view.show_notification("Successfully loaded into viewer.")
            else:
                self.view.show_notification(f"No [' {invoked_action.text()}' ] file was found.")

        elif self.action.text() == "Remove":
            selected_items = self.view.lst_wid.selectedItems()
            rows = sorted([self.view.lst_wid.row(it) for it in selected_items], reverse=True)

            for row in rows:
                self.view.remove_selected(row) 

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

    def preferences_clicked(self):
        existing_prefs_data = self.model.get_current_preferences()
        print("existing_prefs_data -- ", existing_prefs_data)
        self.prefs_window = self.view.open_pref_dialog(existing_prefs_data)   
        self.prefs_window.proj_combo.currentIndexChanged.connect(self.proj_combo_index_changed)
        self.prefs_window.update_btn.clicked.connect(self.update_btn_clicked) 
        self.prefs_window.close_btn.clicked.connect(self.prefs_window.close)


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

        # self.play_menu = self.menu.addMenu("Load in Viewer")
        # self.exr_action = self.play_menu.addAction("exr")

        # self.jpg_action = self.play_menu.addAction("jpg")
        # self.mov_action = self.play_menu.addAction("mov")

        self.laod_action = self.menu.addAction("Load in Viewer")

        self.remove_action = self.menu.addAction("Remove")
        self.compare_action = self.menu.addAction("Compare")

    def load_in_viewer(self):
        print("EXR clicked")

    def set_style_sheet(self):
        self.setStyleSheet("""
                border: 3px grey;
                background-color: #f5f5f5;
        """)

    def add_widgets(self):
        hlay = QHBoxLayout()
        image_full_path = self.img_data_dict['image_full_path']
        pixmap = QPixmap(image_full_path)
        # scaled = pixmap.scaled(120, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        self.drive = None
        # self.json_path = CONFIG_FILEPATH

    def get_invoked_action_path(self, invoked_action):
        # child_widgets = invoked_action.parentWidget().parentWidget().parentWidget().findChildren(QWidget)
        
        # if invoked_action.text() == "exr":
        #     for child in child_widgets:
        #         if isinstance(child, QLabel):
        #             if child.text().startswith("Path"):
        #                 path = child.text().split("Path-")[-1]
        #                 return True, path
        # else:
        #     return False, None

        # ---------------------------------------------------------------------------------------------------------

        child_widgets = invoked_action.parentWidget().parentWidget().findChildren(QWidget)
        

        for child in child_widgets:
            if isinstance(child, QLabel):
                if child.text().startswith("Path"):
                    path = child.text().split("Path-")[-1]
                    return True, path


    def fetch_folder_tree_data(self, path):

        folder_tree_data = {
            "dir_name" : os.path.basename(path),
            "path" : path
            }

        if os.path.isdir(path):
            files = []
            folders = []

            for entry in sorted(os.listdir(path)):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    folders.append(self.fetch_folder_tree_data(full_path))
                else:
                    files.append(full_path.replace("\\", "/"))

            if files:
                folder_tree_data["files"] = files
            if folders:
                folder_tree_data["sub_dir"] = folders

        return folder_tree_data

    def get_urls_data(self, drop_urls):

        folder_tree_data_lst = []
        for url in drop_urls:
            url_path = url.toLocalFile() 
            print("path --- ", url_path)
            if self.drive == None:
                self.drive = re.split(r"[\\/]", url_path)[0]
                print("self.drive 0000 ", self.drive)

            tree_name = re.split(r"[\\/]", url_path)[-1]

            if os.path.isdir(url_path):
                if len(os.listdir(url_path)) > 0:

                    folder_tree_data_dict = self.fetch_folder_tree_data(url_path)
                    folder_tree_data_lst.append({tree_name:folder_tree_data_dict})
   

            #         # ----------------------------------------------------------
            #         # This is working code without thread
            #         self.addTopLevelItem(tree_item)
            #         self.build_tree_view(path, tree_item)
            #         # event.accept()  
            #         # ----------------------------------------------------------   

                else:
                    print("Directory check complete: no content found.")
            else:
                print("This is not directory path")
                # event.ignore()

        
        folder_structure_dir = r"E:\temp\folder_structure\folder_structure_data.json"

        with open(folder_structure_dir, "w", encoding="utf-8") as f:
            json.dump(folder_tree_data_lst, f, indent=4)

        print("Folder structure saved to folder_structure.json")


        return folder_tree_data_lst

    # @Slot(QTreeWidgetItem, int) 
    def get_project_extension(self, proj_code):
        try:
            with open(CONFIG_FILEPATH, "r") as f:
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

    def fetch_project_extensions(self, selected_proj):
        with open(CONFIG_FILEPATH, "r") as rd:
            config_data = json.load(rd)

        print("selected_proj --- ", selected_proj)
        raw_ext_dict = config_data[selected_proj]['extension']
        supported_ext_lst = []

        for ext_key in raw_ext_dict.keys():
            if raw_ext_dict[ext_key] == True:
                supported_ext_lst.append(ext_key)

        return supported_ext_lst


    def get_thumbnil_wid_lst(self, item: QTreeWidgetItem, column: int):

        parts = []
        it = item
  
        while it is not None:
            parts.append(it.text(0))
            it = it.parent()
 
        parts.reverse()
        self.thumbnil_dir_path = os.path.join(self.drive + os.sep, *parts)
        proj_code = parts[1]

        if len(parts) >= 2:
            ext_list = self.fetch_project_extensions(proj_code)
            ext_tuple = tuple(ext_list)
        
            thumbnil_data_dict_lst = []
            thumb_dir_name = ''
            is_available_in_dir = False

            if os.path.isdir(self.thumbnil_dir_path):
                thumb_dir_name = self.thumbnil_dir_path
                    
                if not is_available_in_dir:
                    is_available_in_dir = True                

                for file_name in os.listdir(self.thumbnil_dir_path):
                    print("file_name --- ", file_name)
                    if file_name.lower().endswith(ext_tuple):
                        thumbnil_data_dict = self.get_thumb_data_dict(file_name, is_thumb_dir=True)
                        thumbnil_data_dict_lst.append(thumbnil_data_dict)
                        
            elif os.path.isfile(self.thumbnil_dir_path):
                thumb_dir_name = os.path.dirname(self.thumbnil_dir_path)
                file_name = re.split(r"[\\/]", self.thumbnil_dir_path)[-1]
                if file_name.lower().endswith(ext_tuple):
                    thumbnil_data_dict = self.get_thumb_data_dict(file_name, is_thumb_dir=False)
                    thumbnil_data_dict_lst.append(thumbnil_data_dict)

            if thumbnil_data_dict_lst:
                thumb_wid_lst = []

                for img_data_dict in thumbnil_data_dict_lst:
                    self.thumbnil_widget = ThumbnilWidget(img_data_dict)
                    thumb_wid_lst.append(self.thumbnil_widget)
                        
                if thumb_wid_lst:
                    msg = "Images found."
                    return thumb_wid_lst, thumb_dir_name, msg
            else:
                if is_available_in_dir:
                    msg = "No images found in the directory." 
                    return [], self.thumbnil_dir_path, msg
                else:
                    msg = f"Invalid or unsupported image format - [{file_name.split('.')[-1]}]"
                    return [], self.thumbnil_dir_path, msg        
        else: 
            msg = "Please select a project or a post-prefix directory."
            return [], self.thumbnil_dir_path, msg
         
    def get_thumb_data_dict(self, file_name, is_thumb_dir=None):
        thumbnil_data_dict = {}
        
        if is_thumb_dir:
            image_full_path = os.path.join(self.thumbnil_dir_path, file_name)
        else:
            image_full_path = self.thumbnil_dir_path

        thumbnil_data_dict['lbl_title'] = file_name.split('.')[0]
        thumbnil_data_dict['image_full_path'] = image_full_path
        thumbnil_data_dict['first_frame'] = random.randint(1001, 1009)
        thumbnil_data_dict['last_frame'] = random.randint(1100, 1200)
        
        thumbnil_data_dict['prj_code'] = re.split(r"[\\/]", image_full_path)[2]
        thumbnil_data_dict['shot_code'] =re.split(r"[\\/]", image_full_path)[5]

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

    def get_current_preferences(self):
        try:
            with open(CONFIG_FILEPATH, "r") as f:
                data = json.load(f)
                print(f"Successful read JSON file")
                return data

        except Exception as e:
            print(f"Error reading JSON: {e}")
            return []        

    def overwrite_config(self, new_extensions, selected_proj):
        with open(CONFIG_FILEPATH, 'r') as f:
            data = json.load(f)

        # data[selected_proj]["extension"] = new_extensions
        for ext_item in data[selected_proj]["extension"].keys():
            if ext_item in new_extensions:
                data[selected_proj]["extension"][ext_item] = True
            else:
                data[selected_proj]["extension"][ext_item] = False


        with open(CONFIG_FILEPATH, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Updated extensions for {selected_proj}: {new_extensions}")


def create_json_file(app_dir_path):
    jsn_fle_pth = os.path.join(app_dir_path, CONFIG_FILENAME)
    project = {}

    for num in range(1, 11):
        extension_dict = {ext: (ext in DEFAULT_ENABLED_EXTS) for ext in AVAILABLE_EXTENSIONS}

        project[f"proj_{num:02}"] = {
            "name" : f"Project_{num:02}",
            "extension": extension_dict
        }

        with open(jsn_fle_pth, "w") as json_file:
            json.dump(project, json_file, indent=4)
    print("config file created ----------- ", jsn_fle_pth)
        

def setup_config():
    # app_dir_path = Path(DOCUMENTS_DIRPATH) / "/app"
    # print("app_dir_path --- ", app_dir_path)
    config_dir_path = os.path.dirname(CONFIG_FILEPATH)

    if not os.path.exists(config_dir_path):
        # config_dir_path.mkdir(exist_ok=True)
        os.makedirs(config_dir_path)
        create_json_file(config_dir_path)

    elif not CONFIG_FILENAME in os.listdir(config_dir_path):
        create_json_file(config_dir_path)
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = View(app)
    setup_config()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())

