from sklearn.cluster import DBSCAN
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.conclusion_2.json_helper import JSONHelper

class DBSCANAnalyser:

    def __init__(self,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.col_names = col_names 
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.alg_name = "DBSCAN"

    def analyse(self,performance_metrics):
        optimum_names = ["Calinski Harabasz Index Optimum","Silhouette Score Optimum"]
        for optimum in optimum_names:
            if optimum in performance_metrics.keys():
                self.analyse_alg_optimum_in_format_1(self.col_names,self.encoding_first_junk,self.folder_name, self.data, self.credit_ratings, performance_metrics,self.credit_rating_analyzers,optimum)
            elif "Threshold Value" in performance_metrics.keys():
                self.analyse_alg_optimum_in_format_2(self.col_names,self.encoding_first_junk,self.folder_name, self.data, self.credit_ratings, performance_metrics,self.credit_rating_analyzers,optimum)

    def get_name_and_significant_cluster_count(self):
        return self.name, self.significant_clusters_count
    
    def analyse_alg_optimum_in_format_1(self,col_names,encoding_first_junk,folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers,optimum):
        birch = DBSCAN(eps=float(performance_metrics[optimum]["Eps"]),min_samples=int(performance_metrics[optimum]["MinPts"])).fit(self.data)
        labels = birch.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Eps":performance_metrics[optimum]["Eps"],"MinPts":performance_metrics[optimum]["MinPts"],"K":performance_metrics[optimum]["Number of Clusters"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics[optimum]["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics[optimum]["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(encoding_first_junk,labels,credit_ratings,credit_rating_analyzers,data,col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(folder_name,self.alg_name+"_"+optimum)
        self.name = self.alg_name+"_"+optimum
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(folder_name,self.alg_name+"_"+optimum,analysis)
    
    def analyse_alg_optimum_in_format_2(self,col_names,encoding_first_junk,folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers,optimum):
        birch = DBSCAN(eps=float(performance_metrics["Eps"][optimum]),min_samples=int(performance_metrics["MinPts"][optimum])).fit(self.data)
        labels = birch.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Eps":performance_metrics["Eps"][optimum],"MinPts":performance_metrics["MinPts"][optimum],"K":performance_metrics["K"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(encoding_first_junk,labels,credit_ratings,credit_rating_analyzers,data,col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(folder_name,self.alg_name+"_"+optimum)
        self.name = self.alg_name+"_"+optimum
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(folder_name,self.alg_name+"_"+optimum,analysis)