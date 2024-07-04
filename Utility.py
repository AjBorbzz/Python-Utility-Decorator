import os
import hashlib
import json
from datetime import datetime
import re
import math


class Utility:
    @staticmethod
    def generate_hash(data, algorithm='sha256'):
        hash_function = getattr(hashlib, algorithm)()
        hash_function.update(data.encode('utf-8'))
        return hash_function.hexdigest()
    
    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
        
    @staticmethod
    def write_json_file(data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)


    @staticmethod
    def get_current_time_format(format='%Y-%m-%d %H:%M:%S'):
        return datetime.now().strftime(format)
    

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def file_exists(file_path):
        return os.path.isfile(file_path)
    

    @staticmethod
    def directory_exists(dir_path):
        return os.path.isdir(dir_path)
    
    @staticmethod
    def create_directory(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        print("Created Directory...")

    @staticmethod
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    

    @staticmethod
    def list_files_in_directory(dir_path, extension=None):
        if extension:
            return [f for f in os.listdir(dir_path) if f.endswith(extension)]
        else:
            return os.listdir(dir_path)
        
        
        
