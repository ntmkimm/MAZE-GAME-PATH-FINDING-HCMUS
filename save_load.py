import pickle
import json
import os

class File:
    def __init__(self, player_name=''):
        self.extension = ".json"
        self.root = os.path.join("save_data", player_name)
        self.create_folder_of_player()
    
    def create_folder_of_player(self):
        os.makedirs(self.root, exist_ok=True)

    def save(self, data, file_name):
        if self.is_possible_to_save():
            file = open(os.path.join(self.root, file_name + self.extension), "w")
            json.dump(data, file)

    def load(self, file_name):
        file = open(os.path.join(self.root, file_name + self.extension), "r")
        data = json.load(file)
        return data

    def is_exist(self, file_name):
        return os.path.exists(os.path.join(self.root, file_name + self.extension))
    
    def delete(self, file_name):
        file = os.path.join(self.root, file_name + self.extension)
        if os.path.exists(file):
            os.remove(file)
            return True
        return False
    
    def is_possible_to_save(self):
        files = os.listdir(self.root)
        if len(files) > 6:
            return False
        return True
    
    def get_files(self):
        files = os.listdir(self.root)
        filenames = [f[:-5] for f in files if f.endswith(self.extension)]
        return filenames