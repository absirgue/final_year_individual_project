from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.conclusion_2.json_helper import JSONHelper
from clustering.fast_global_k_means import FastGlobalKMeans

class FastGlobalKMeansAnalyser:

    def __init__(self,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.col_names = col_names 
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.alg_name = "K-Means"
        
    def analyse(self,performance_metrics):
        fast = FastGlobalKMeans(performance_metrics["K"])
        labels = fast.cluster(self.data)
        self.produce_analysis(self.col_names,self.encoding_first_junk,labels,self.folder_name, self.data, self.credit_ratings, performance_metrics,self.credit_rating_analyzers)
    
    def produce_analysis(self,col_names,encoding_first_junk,labels,folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers):
        analysis = {}
        analysis["Algorithm Parameters"] = {"K":performance_metrics["K"]}
        analysis["Algorithm Performance"] = {"WCSS":performance_metrics["WCSS"],"Silhouette Score":performance_metrics["Silhouette Score"],"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        cluster_analyzer = ClustersAnalyzer(encoding_first_junk,labels,credit_ratings,credit_rating_analyzers,data,col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze()
        JSONHelper().save(folder_name,self.alg_name,analysis)