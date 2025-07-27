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




class LayoutManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Manager")
        self.setGeometry(400,200, 1000, 450)

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
        self.tree_wid = QTreeWidget()
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



