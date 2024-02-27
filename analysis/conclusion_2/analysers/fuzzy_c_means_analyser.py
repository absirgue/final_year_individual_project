import numpy as np
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.conclusion_2.json_helper import JSONHelper
from skfuzzy.cluster import cmeans

class FuzzyCMeansAnalyser:

    def __init__(self,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
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
        self.produce_analysis(self.col_names,self.encoding_first_junk,labels,self.folder_name, self.data, self.credit_ratings, performance_metrics,self.credit_rating_analyzers)
    
    def get_name_and_significant_cluster_count(self):
        return self.alg_name, self.significant_clusters_count
    
    def produce_analysis(self,col_names,encoding_first_junk,labels,folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers):
        analysis = {}
        analysis["Algorithm Parameters"] = {"C":performance_metrics["C"]}
        analysis["Algorithm Performance"] = {"WCSS":performance_metrics["WCSS"],"Silhouette Score":performance_metrics["Silhouette Score"],"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        cluster_analyzer = ClustersAnalyzer(encoding_first_junk,labels,credit_ratings,credit_rating_analyzers,data,col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(folder_name,self.alg_name,analysis)