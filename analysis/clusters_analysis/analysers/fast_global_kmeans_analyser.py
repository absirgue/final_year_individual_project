from analysis.clusters_analysis.clusters_analyzer import ClustersAnalyzer
from analysis.json_helper import JSONHelper
from clustering_algorithms.fast_global_k_means import FastGlobalKMeans

class FastGlobalKMeansAnalyser:
    """
    Runs Fast Global K-Means with specified hyperparameters and on a specified data set 
    before coordianting the analysis of its result.
    """

    def __init__(self,data_source,entity_ids,col_names,encoding_first_junk,folder_name, data, credit_ratings,credit_rating_analyzers):
        self.data_source =data_source
        self.col_names = col_names 
        self.entity_ids = entity_ids
        self.encoding_first_junk = encoding_first_junk
        self.folder_name = folder_name
        self.data = data
        self.credit_ratings = credit_ratings
        self.credit_rating_analyzers = credit_rating_analyzers
        self.alg_name = "K-Means"
        
    def analyse(self,performance_metrics):
        fast = FastGlobalKMeans(performance_metrics["K"])
        labels = fast.cluster(self.data)
        self.produce_analysis(labels, performance_metrics)
    
    def analyse_from_alg_hyperparameters(self,K,file_name_appendix=None):
        fast = FastGlobalKMeans(K)
        labels = fast.cluster(self.data)
        analysis = {}
        analysis["Algorithm Parameters"] = {"K":K}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids, self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name+file_name_appendix,analysis)
    
    def get_name_and_significant_cluster_count(self):
        return self.alg_name, self.significant_clusters_count

    def produce_analysis(self,labels,performance_metrics):
        analysis = {}
        analysis["Algorithm Parameters"] = {"K":performance_metrics["K"]}
        analysis["Algorithm Performance"] = {"WCSS":performance_metrics["WCSS"],"Silhouette Score":performance_metrics["Silhouette Score"],"Calinski Harabasz Index":performance_metrics["Calinski Harabasz Index"]}
        cluster_analyzer = ClustersAnalyzer(self.entity_ids, self.data_source,self.encoding_first_junk,labels,self.credit_ratings,self.credit_rating_analyzers,self.data,self.col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze(self.folder_name,self.alg_name)
        self.significant_clusters_count = analysis["Clusters Content Analysis"]["Significant Clusters (count)"]
        JSONHelper().save(self.folder_name,self.alg_name,analysis)