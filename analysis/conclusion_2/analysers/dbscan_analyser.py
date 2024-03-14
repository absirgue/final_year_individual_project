from sklearn.cluster import DBSCAN
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.json_helper import JSONHelper

class DBSCANAnalyser:

    def __init__(self,data_source,entity_ids,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.data_source = data_source
        self.col_names = col_names 
        self.entity_ids = entity_ids
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.significant_clusters_count = 0
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.alg_name = "DBSCAN"

    def analyse(self,performance_metrics):
        optimum_names = ["Calinski Harabasz Index Optimum","Silhouette Score Optimum"]
        for optimum in optimum_names:
            self.alg_name = self.alg_name+"_"+optimum
            if optimum in performance_metrics.keys():
                self.analyse_alg_optimum_in_format_1(optimum,performance_metrics)
            elif "Threshold Value" in performance_metrics.keys():
                self.analyse_alg_optimum_in_format_2(optimum,performance_metrics)

    def analyse_from_alg_hyperparameters(self,eps, minpts,file_name_appendix=None):
        birch = DBSCAN(eps=eps,min_samples=minpts).fit(self.data)
        labels = birch.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Eps":eps,"MinPts":minpts}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids, self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name+file_name_appendix,analysis)

    def get_name_and_significant_cluster_count(self):
        return self.alg_name, self.significant_clusters_count 
    
    def analyse_alg_optimum_in_format_1(self,optimum,performance_metrics):
        dbscan = DBSCAN(eps=float(performance_metrics[optimum]["Eps"]),min_samples=int(performance_metrics[optimum]["MinPts"])).fit(self.data)
        labels = dbscan.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Eps":performance_metrics[optimum]["Eps"],"MinPts":performance_metrics[optimum]["MinPts"],"K":performance_metrics[optimum]["Number of Clusters"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics[optimum]["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics[optimum]["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids,self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name+"_"+optimum,analysis)
    
    def analyse_alg_optimum_in_format_2(self,optimum,performance_metrics):
        dbscan = DBSCAN(eps=float(performance_metrics["Eps"][optimum]),min_samples=int(performance_metrics["MinPts"][optimum])).fit(self.data)
        labels = dbscan.labels_
        analysis = {}
        analysis["Algorithm Parameters"] = {"Eps":performance_metrics["Eps"][optimum],"MinPts":performance_metrics["MinPts"][optimum],"K":performance_metrics["K"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids,self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name+"_"+optimum,analysis)