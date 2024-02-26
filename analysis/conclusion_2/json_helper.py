import os
import json
import numpy as np

class JSONHelper:

    def save(self,folder_name, file_name,content):
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        file_name+=".json"
        file_path = os.path.join(folder_name, file_name)
        # Write the dictionary to a JSON file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w+') as json_file:
            json.dump(content, json_file,default=convert_to_serializable)
        # d'abord best performance, on les met dans un folder "conclusion 2/with-without pca/algorithms best performance/the file name is the alg name"
        # keep silhouette, calinski harabasaz, and time metrics in the json 
        # then the analysis 
        # so analyze must buckle 
    
    def read(self, source_file_path):
        with open(source_file_path) as f:
            content = json.load(f)
            return content