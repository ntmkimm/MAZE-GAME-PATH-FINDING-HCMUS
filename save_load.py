import pickle
import os

class File:
    def __init__(self, player_name=''):
        self.extension = ".save"
        self.root = os.path.join("save_data", player_name)
        self.create_folder_of_player()
    
    def create_folder_of_player(self):
        os.makedirs(self.root, exist_ok=True)

    def save(self, data, file_name):
        file = open(os.path.join(self.root, file_name + self.extension), "wb")
        pickle.dump(data, file)

    def load(self, file_name):
        file = open(os.path.join(self.root, file_name + self.extension), "rb")
        data = pickle.load(file)
        return data

    def is_exist(self, file_name):
        return os.path.exists(os.path.join(self.root, file_name + self.extension))
    
    def delete(self, file_name):
        file = os.path.join(self.root, file_name + self.extension)
        if os.path.exists(file):
            os.remove(file)
            return True
        return False

