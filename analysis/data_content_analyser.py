from analysis.json_helper import JSONHelper

class DataContentAnalyser:

    def __init__(self,data,config_name,ordered_credit_ratings,col_names):
        self.folder_name = "data_configs_analysis"
        self.data = data
        self.config_name = config_name
        self.ordered_credit_ratings = ordered_credit_ratings
        self.col_names = col_names

    def analyse(self):
        analysis = self.analyse_data()
        self.save_analysis(analysis)
       

    def analyse_data(self):
        ratings_share = self.get_shares_of_each_ratings()
        return {"Number of Companies":self.data.shape[0],"Number of Columns":self.data.shape[1],"Share of each Credit Rating":ratings_share,"List of Columns":list(self.col_names)}
    
    def print_analysis(self, analysis):
        print("\n************ Analysis for Data Configuration",self.config_name," ************\n")
        print(analysis)
        print("\n*****************************************\n")
    
    def save_analysis(self,analysis):
        JSONHelper().save(self.folder_name, self.config_name,analysis)

    def get_shares_of_each_ratings(self):
        counts = {}
        for rating in self.ordered_credit_ratings:
            if rating in counts.keys():
                counts[rating] += 1
            else:
                counts[rating] = 1
        for rating, count in counts.items():
            counts[rating] = count/self.data.shape[0]
        return counts