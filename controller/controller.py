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

from platformdirs import user_documents_dir
from pathlib import Path
import re






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
        ext_list = self.model.fetch_project_extensions(proj_code)
        print("ext_list ---- ", ext_list)
        
        self.prefs_window.set_extension_lst(ext_list)

    def update_btn_clicked(self):
        new_extensions = self.prefs_window.get_checked_extension()
        print("new_extensions --- ", new_extensions)
        selected_proj = self.prefs_window.proj_combo.currentText() 
        self.model.overwrite_config(new_extensions, selected_proj)

    def on_item_clicked(self, item, column):
        # ==========================================================================================
        # This code is without threadpool
        thumbnil_wid_items_lst, thumb_dir_name, msg = self.model.get_thumbnil_wid_lst(item, column)

        if thumbnil_wid_items_lst:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(thumb_dir_name)
            self.view.add_thumbnil_wid(thumbnil_wid_items_lst)

            for w in thumbnil_wid_items_lst:
                w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))

        else:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(thumb_dir_name)
            self.view.show_notification(msg)
        # ==========================================================================================

        # ---------------------------------------------------------------------------------------------     
        # This is with threadpool (UI is crushing when click on qtreewidgetitem)

        # thumbnil_wid_items_lst, thumb_dir_name, msg = self.model.get_thumbnil_wid_lst(item, column)      

        # tree_item_click_worker_pool = TreeItemClickWorkerPool(thumbnil_wid_items_lst, thumb_dir_name, msg)
        # tree_item_click_worker_pool.signal_obj.custom_context.connect(self.update_ui_frm_workerpool)

        # thread_pool = QThreadPool.globalInstance()
        # thread_pool.start(tree_item_click_worker_pool)
        # --------------------------------------------------------------------------------------------- 

    def thumbnail_context_action(self, thumbnil_wid_items_lst):
        for w in thumbnil_wid_items_lst:
            w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))

    def update_ui_frm_workerpool(self, thumbnil_wid_items_lst, thumb_dir_name, msg):
        if thumbnil_wid_items_lst:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(thumb_dir_name)
            self.view.add_thumbnil_wid(thumbnil_wid_items_lst)
            self.thumbnail_contextc_action(thumbnil_wid_items_lst)
        else:
            self.view.clear_lst_wid()
            self.view.set_lbl_thumbnil_path(thumb_dir_name)
            self.view.show_notification(msg)        

    def on_files_dropped(self, drop_urls):
        folder_tree_data_lst = self.model.get_urls_data(drop_urls)
        self.view.tree_wid.load_folder_tree_into_ui(folder_tree_data_lst)


    def handle_context_menu(self, widget, pos):       
        
        widget.populate_menu_actions(pos)
        self.action = widget.menu.exec_(widget.mapToGlobal(pos)) 

        if self.action:
            self.action_clicked(self.action, pos)

    def action_clicked(self, invoked_action, pos):
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
