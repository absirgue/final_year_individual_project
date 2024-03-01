from sklearn.cluster import Birch
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.conclusion_2.json_helper import JSONHelper

class BIRCHAnalyser:

    def __init__(self,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.col_names = col_names 
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.significant_clusters_count = 0
        self.alg_name = "BIRCH"
        
    def analyse(self,performance_metrics):
        optimum_names = ["Calinski Harabasz Index Optimum","Silhouette Score Optimum"]
        for optimum in optimum_names:
            if optimum in performance_metrics.keys():
                self.analyse_alg_optimum_in_format_1(optimum,performance_metrics)
            elif "Threshold Value" in performance_metrics.keys():
                self.analyse_alg_optimum_in_format_2(optimum,performance_metrics)

    def get_name_and_significant_cluster_count(self):
        return self.name, self.significant_clusters_count

    def analyse_alg_optimum_in_format_1(self,optimum,performance_metrics):
        birch = Birch(threshold=float(performance_metrics[optimum]["Threshold Value"]), branching_factor=int(performance_metrics[optimum]["Branching Factor"]), n_clusters=int(performance_metrics[optimum]["K"])).fit(self.data)
        labels = birch.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Threshold Value":performance_metrics[optimum]["Threshold Value"],"Braching Factor":performance_metrics[optimum]["Branching Factor"],"K":performance_metrics[optimum]["K"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics[optimum]["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics[optimum]["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name+"_"+optimum)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        self.name = self.alg_name+"_"+optimum
        JSONHelper().save(self.folder_name,self.alg_name+"_"+optimum,analysis)
    
    def analyse_alg_optimum_in_format_2(self,optimum,performance_metrics):
        birch = Birch(threshold=float(performance_metrics["Threshold Value"][optimum]), branching_factor=int(performance_metrics["Branching Factor"][optimum]), n_clusters=int(performance_metrics["K"])).fit(self.data)
        labels = birch.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Threshold Value":performance_metrics["Threshold Value"][optimum],"Braching Factor":performance_metrics["Branching Factor"][optimum],"K":performance_metrics["K"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name+"_"+optimum)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        self.name = self.alg_name+"_"+optimum
        JSONHelper().save(self.folder_name,self.alg_name+"_"+optimum,analysis)