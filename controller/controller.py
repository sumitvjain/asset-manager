from qt_lib.qt_compact import *

# from config import constant

# con = constant.Constant()



class Controller(QObject):
    """
    Controller class acts as a mediator between the Model and View.
    Responsibilities:
    - Connects UI actions to corresponding model/view methods.
    - Handles user interactions like clicks, drag/drop, context menus.
    - Manages zooming, keyboard shortcuts, and updating the view.
    - Controls project preferences and configuration updates.
    """

    def __init__(self, model, view, nuke_operation):

        """
        Initialize Controller.

        Args:
            model: Instance of the Model class (data and logic).
            view: Instance of the View class (UI components).
        """

        super().__init__()
        self.model = model
        self.view = view
        self.nuke_operation = nuke_operation
        self.zoom_factor = 1.0
        self.signal_slot()
        self.view.tab_wid.setFocusPolicy(Qt.StrongFocus)
        self.view.tab_wid.installEventFilter(self)

    def signal_slot(self):   
        """
        Connects UI signals to controller methods.
        """

        # File menu actions
        self.view.open_file_action.triggered.connect(self.open_file)
        self.view.open_folder_action.triggered.connect(self.open_folder)
        self.view.save_action.triggered.connect(self.save_file)
        self.view.save_as_action.triggered.connect(self.save_as_file)

        # Edit menu actions
        self.view.undo_action.triggered.connect(self.undo_last_action)
        self.view.redo_action.triggered.connect(self.redo_last_action)
        self.view.cut_action.triggered.connect(self.cut_selected_item)
        self.view.copy_action.triggered.connect(self.copy_selected_item)
        self.view.paste_action.triggered.connect(self.paste_item)
        self.view.preferences_action.triggered.connect(self.preferences_clicked)

        # Tree widget actions
        self.view.tree_wid.itemClicked.connect(self.on_item_clicked)
        self.view.tree_wid.filesDropped.connect(self.on_files_dropped)

    def proj_combo_index_changed(self):
        """
        Triggered when project combo box index changes in preferences dialog.
        Updates extension list for selected project.
        """
        proj_code = self.prefs_window.get_current_project_code()
        ext_list = self.model.fetch_project_extensions(proj_code)
        print("ext_list ---- ", ext_list)
        
        self.prefs_window.set_extension_lst(ext_list)

    def update_btn_clicked(self):
        """
        Triggered when 'Update' button is clicked in preferences dialog.
        Saves updated extensions for selected project.
        """
        new_extensions = self.prefs_window.get_checked_extension()
        print("new_extensions --- ", new_extensions)
        selected_proj = self.prefs_window.proj_combo.currentText() 
        self.model.overwrite_config(new_extensions, selected_proj)

    def on_item_clicked(self, item, column):
        """
        Triggered when a tree widget item is clicked.
        Fetches thumbnails and updates the UI.

        Args:
            item: QTreeWidgetItem clicked.
            column: Column index clicked.
        """
        # ==========================================================================================
        # ---- Without ThreadPool ---- #
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
        # ---- With ThreadPool (Causing UI crash, commented) ---- # 

        # thumbnil_wid_items_lst, thumb_dir_name, msg = self.model.get_thumbnil_wid_lst(item, column)      

        # tree_item_click_worker_pool = TreeItemClickWorkerPool(thumbnil_wid_items_lst, thumb_dir_name, msg)
        # tree_item_click_worker_pool.signal_obj.custom_context.connect(self.update_ui_frm_workerpool)

        # thread_pool = QThreadPool.globalInstance()
        # thread_pool.start(tree_item_click_worker_pool)
        # --------------------------------------------------------------------------------------------- 

    def thumbnail_context_action(self, thumbnil_wid_items_lst):
        """
        Attach context menu actions for a list of thumbnail widgets.

        Args:
            thumbnil_wid_items_lst (list): List of thumbnail widget instances.
        """
        for w in thumbnil_wid_items_lst:
            w.customContextMenuRequested.connect(lambda pos, widget=w: self.handle_context_menu(widget, pos))

    def update_ui_frm_workerpool(self, thumbnil_wid_items_lst, thumb_dir_name, msg):
        """
        Update UI after worker pool completes (ThreadPool approach).

        Args:
            thumbnil_wid_items_lst (list): Thumbnails loaded by worker.
            thumb_dir_name (str): Directory path of thumbnails.
            msg (str): Status message.
        """
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
        """
        Handle file/folder drop onto tree widget.

        Args:
            drop_urls (list): Dropped file/folder URLs.
        """
        folder_tree_data_lst = self.model.get_urls_data(drop_urls)
        self.view.tree_wid.load_folder_tree_into_ui(folder_tree_data_lst)

    # ---------------- Context Menu Handling ---------------- #
    def handle_context_menu(self, widget, pos):       
        """
        Display context menu for a thumbnail widget.

        Args:
            widget: Thumbnail widget.
            pos: Position where context menu was requested.
        """
        widget.populate_menu_actions(pos)
        self.action = widget.menu.exec_(widget.mapToGlobal(pos)) 

        if self.action:
            self.action_clicked(self.action, pos)

    # def get_meta(self, path):
    #     proc = subprocess.Popen(
    #         [str(con.NUKE_EXE), "-t", str(con.NUKE_OP_PATH), str(path)],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         text=True
    #     )

    #     stdout, stderr = proc.communicate()
        
    #     print("RETURN CODE:", proc.returncode)
    #     print("STDOUT:\n", stdout)
    #     print("STDERR:\n", stderr)


    def action_clicked(self, invoked_action, pos):
        """
        Handle action clicked from thumbnail context menu.

        Args:
            invoked_action: QAction invoked.
            pos: Position of action trigger.
        """
        if invoked_action.text() == "Load in Viewer":
            result, path = self.model.get_invoked_action_path(invoked_action)
            print("result --- ", result)
            print("path --- ", path)
            if result:
                self.view.load_render_in_viewer(path)
                self.update_image_size()
                # self.view.show_notification("Successfully loaded into viewer.")
                # Need to add code here for meta data login(calling from here)
                # meta_data_dict = self.nuke_operation.get_meta_data(path) temporary off
                self.model.get_meta(path)

                print("*************** meta_data_dict ***************")
                # from pprint import pprint
                # pprint(meta_data_dict)


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

     # ---------------- Event Handling ---------------- #
    def eventFilter(self, obj, event):
        """
        Event filter to handle zooming (mouse wheel, +/- keys) and focus on tab widget.

        Args:
            obj: Object receiving the event.
            event: QEvent instance.

        Returns:
            bool: Whether event was handled or passed along.
        """
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
        """
        Scale and update image preview based on current zoom factor.
        """
        if self.view.pixmap:
            scaled_pixmap = self.view.pixmap.scaled(
                self.view.tab_view_lbl.size() * self.zoom_factor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.view.tab_view_lbl.setPixmap(scaled_pixmap)

    # ---------------- Menu Actions (File/Edit) ---------------- #
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
        """
        Handle 'Preferences' action.
        Opens preferences dialog and sets up signal connections.
        """
        existing_prefs_data = self.model.get_current_preferences()
        print("existing_prefs_data -- ", existing_prefs_data)
        self.prefs_window = self.view.open_pref_dialog(existing_prefs_data)   
        self.prefs_window.proj_combo.currentIndexChanged.connect(self.proj_combo_index_changed)
        self.prefs_window.update_btn.clicked.connect(self.update_btn_clicked) 
        self.prefs_window.close_btn.clicked.connect(self.prefs_window.close)
