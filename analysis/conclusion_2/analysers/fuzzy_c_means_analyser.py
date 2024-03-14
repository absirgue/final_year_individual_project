import numpy as np
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.json_helper import JSONHelper
from skfuzzy.cluster import cmeans

class FuzzyCMeansAnalyser:

    def __init__(self,data_source,entity_ids,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.data_source =data_source
        self.entity_ids = entity_ids
        self.col_names = col_names 
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.alg_name = "Fuzzy C-Means"
        
    def analyse(self,performance_metrics):
        cntr, u, _, _, _, _, _ = cmeans(self.data.T, c=performance_metrics["C"], m=2,error=0.001,maxiter=400)
        labels = np.argmax(u, axis=0)
        self.produce_analysis(labels,performance_metrics)
    
    def analyse_from_alg_hyperparameters(self,C,file_name_appendix=None):
        cntr, u, _, _, _, _, _ = cmeans(self.data.T, c=C, m=2,error=0.001,maxiter=400)
        labels = np.argmax(u, axis=0)
        analysis = {}
        analysis["Algorithm Parameters"] = {"C":C}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids,self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name+file_name_appendix,analysis)

    def get_name_and_significant_cluster_count(self):
        return self.alg_name, self.significant_clusters_count
    
    def produce_analysis(self,labels, performance_metrics):
        analysis = {}
        analysis["Algorithm Parameters"] = {"C":performance_metrics["C"]}
        analysis["Algorithm Performance"] = {"WCSS":performance_metrics["WCSS"],"Silhouette Score":performance_metrics["Silhouette Score"],"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids,self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name,analysis)