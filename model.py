

class DataModel():
    def __init__(self):
        pass

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
