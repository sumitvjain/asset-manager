from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent
from PySide2. QtCore import Qt, QUrl
import sys, os

# class TreeWidgetDragDropHandler():
#     def __init__(self, view):
#        super().__init__()
#        self.view = view

#     #    self.view.setAcceptDrops(True)

#     def dragEnterEvent(self, event:QDragEnterEvent):
#         if event.mimeData().hasUrls():
#             print("dragEnterEvent --------- ")
#             event.acceptProposedAction()
#         else:
#             event.ignore()
    
#     def dragMoveEvent(self, e:QDragMoveEvent):
#         if e.mimeData().hasUrls():
#             print("dragMoveEvent --------- ")
#             e.acceptProposedAction()
#         else:
#             e.ignore()

#     def dropEvent(self, event):
#         if event.mimeData().hasUrls():
#             drop_urls = event.mimeData().urls()
#             print("drop_urls --- ", drop_urls)
#             url = event.mimeData().urls()[0]
#             folder_path = url.toLocalFile()
#             if os.path.isdir(folder_path):
#                 if len(os.listdir(folder_path)) > 0:
#                     dir_path = url.toLocalFile()
#                     print("dir_path path ---- ", dir_path)

#                     dir_lst_itms = os.listdir(dir_path)
                    
#                     proj_len = len(dir_lst_itms)
#                     print("proj_len --- ", proj_len)

#                     for dir_itm in dir_lst_itms:
#                         print(dir_itm)

                    

#                     event.accept()
#                 else:
#                     print("Directory check complete: no content found.")
#             else:
#                 print("This is not directory path")
#                 event.ignore()

#         else:
#             event.ignore()



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
