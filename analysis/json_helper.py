import os
import json
import numpy as np
import codecs

class JSONHelper:
    """
    Interfaces with JSON documents to enable other classes to both read and write such files.
    """

    # Saves data to a json file given a specified name and placed in a specified folder.
    def save(self,folder_name, file_name,content, encoding='utf-8'):
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        file_name+=".json"
        file_path = os.path.join(folder_name, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w+', encoding=encoding) as json_file:
            json.dump(content, json_file,default=convert_to_serializable)
    
    # Reads the content of a json file located at a spcific path.
    def read(self, source_file_path):
        with codecs.open(source_file_path, 'r', encoding='utf-8',
                 errors='ignore') as f:
            # open(source_file_path, 'r')
            content = json.load(f,strict=False)
            return content