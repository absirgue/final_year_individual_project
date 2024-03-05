from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.json_helper import JSONHelper
from sklearn.cluster import KMeans

class KMeansAnalyser:

    def __init__(self,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.col_names = col_names 
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.alg_name = "Fast Global K-Means"
        
    def analyse(self,performance_metrics):
        k_means = KMeans(n_clusters=performance_metrics["K"],n_init=1).fit(self.data)
        labels = k_means.labels_
        self.produce_analysis(labels, performance_metrics)
    
    def get_name_and_significant_cluster_count(self):
        return self.alg_name, self.significant_clusters_count
    
    def produce_analysis(self,labels, performance_metrics):
        analysis = {}
        analysis["Algorithm Parameters"] = {"K":performance_metrics["K"]}
        analysis["Algorithm Performance"] = {"WCSS":performance_metrics["WCSS"],"Silhouette Score":performance_metrics["Silhouette Score"],"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        cluster_analyzer = ClustersAnalyzer(self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name,analysis)