import os
import json
import numpy as np

class JSONHelper:

    def save(self,folder_name, file_name,content, encoding='utf-8'):
        print(content)
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        file_name+=".json"
        file_path = os.path.join(folder_name, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w+', encoding=encoding) as json_file:
            json.dump(content, json_file,default=convert_to_serializable)
    
    def read(self, source_file_path):
        with open(source_file_path) as f:
            content = json.load(f)
            return content