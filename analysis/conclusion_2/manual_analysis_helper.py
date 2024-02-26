import os
from analysis.conclusion_2.json_helper import JSONHelper

class ManualAnalysisHelper:

    def __init__(self):
        self.files = self.iterate_files_in_folder("./conclusion_2_results")
        self.print_name_of_significant_files()

    def iterate_files_in_folder(self,folder_path):
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        return file_paths

    def print_name_of_significant_files(self):
        important_files = []
        for file_path in self.files:
            content = JSONHelper().read(file_path)
            number_of_significant_clusters = content["Clusters Content Analysis"]["Clusters with significant ranges (count)"]
            if "K" in content["Algorithm Parameters"].keys():
                number_of_clusters = content["Algorithm Parameters"]["K"]
            else:
                number_of_clusters = content["Algorithm Parameters"]["C"]
            if  number_of_significant_clusters/number_of_clusters>= 0.1:
                important_files.append(file_path)
        print(important_files)
        print("NUMBER OF FILES IDENTIFIED AS IMPORTANT: "+str(len(important_files)))
        print("TOTAL NUMBER OF FILES: "+str(len(self.files)))