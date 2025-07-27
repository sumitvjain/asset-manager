


class LogicHandler():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.signal_slot()

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
