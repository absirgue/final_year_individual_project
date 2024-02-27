from data_preparation.data_preparator import DataPreparator
from clustering.k_means import KMeans
from sklearn.cluster import  DBSCAN as D
from sklearn.cluster import  Birch as B
import pandas as pd
from analysis.data_configuration import DataConfiguration
# from clustering.BIRCH.birch import BIRCH
from clustering.dbscan import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from clustering.fast_global_k_means import FastGlobalKMeans
import matplotlib.pyplot as plt
import numpy as np
from analysis.dimensionality_evaluation import DimensionalityEvaluation
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.conclusion_1.iterators.kmeans_iterator import KMeansIterator
from data_treatment.principal_component_analysis import PrincipalComponentAnalysis
from analysis.conclusion_1.algorithms_best_performance import AlgorithmsBestPerformanceEvaluation
from analysis.conclusion_1.iterators.birch_iterator import BIRCHIterator
from analysis.conclusion_1.iterators.birch_super_iterator import BIRCHSuperIterator
from analysis.conclusion_2.clustering_results_analyzer import ClusteringResultsAnalyzer
from analysis.conclusion_2.manual_analysis_helper import ManualAnalysisHelper
from analysis.conclusion_3.rating_changes_identifier import RatingChangesIdentifier
np.seterr(over='ignore')

class DataSource:
    def __init__(self,path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name

data_source = DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")

# RatingChangesIdentifier(data_source).identify_changes()

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def pca_and_plot(data_array):
    std_scaler = StandardScaler()
    scaled_df = std_scaler.fit_transform(data_array)
    nan_rows = np.isnan(scaled_df).any(axis=1)
    cleaned_scaled_df = scaled_df[~nan_rows]
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(cleaned_scaled_df)

    # Plot the reduced data
    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], alpha=0.7)
    plt.title('2D PCA Plot')
    plt.xlabel('Principal Component 1 (PC1)')
    plt.ylabel('Principal Component 2 (PC2)')
    plt.grid(True)
    plt.show()

data_configuration = DataConfiguration()
data_configuration.set_to_default_configuration("BOTH")
data_preparator = DataPreparator(data_source=data_source,configuration=data_configuration)
data = data_preparator.apply_configuration(0.8)
# has_nan = np.isnan(data).any()
# print("Contains NaN values:", has_nan)
pca_and_plot(data)

# analyser = ClusteringResultsAnalyzer("./conclusion_1_graphs/algorithms_comparisons/without_pca/performance_metrics.json", "conclusion_2",data_source,False)
# analyser.analyse()
# ManualAnalysisHelper()

# AlgorithmsBestPerformanceEvaluation(data_source,run_pca=True).run_evaluation()
# AlgorithmsBestPerformanceEvaluation(data_source,run_pca=False).run_evaluation()

# optimal_col_emptiness_ratios_for_default_config = {'RATIOS': 0.8, 'RAW NUMBERS': 0.45, 'BOTH': 0.8}
# # {'RATIOS': 29, 'RAW NUMBERS': 29, 'BOTH': 38}
# config = DataConfiguration()
# config.set_to_default_configuration("BOTH")
# dp = DataPreparator(data_source=data_source,configuration=config)
# data= dp.apply_configuration(0.8)
# pca = PrincipalComponentAnalysis(data,38)
# b = BIRCHSuperIterator(pca.reduce_dimensionality(),25)
# b.iterate()
# b.graph()
# print(data.shape)
# pca = PrincipalComponentAnalysis(data,20)
# print(type(pca.reduce_dimensionality()))
# print(pca.reduce_dimensionality().shape)



# data = dp.apply_configuration(0.1)
# dp.get_credit_ratings()
# # it = BIRCHSuperIterator(data,4)
# # it.iterate()
# # it.graph()
# # print(it.get_optimal())

# print(EmptyRowsDeletionEvaluation().run_evaluation(data_source))
# print(DimensionalityEvaluation().run_evaluation(data_source))

# data = pd.DataFrame({'Number of Geographic Segments [Annual]':[1,2,3,4],"Number of Business Segments [Annual]":[-2,3,4,5],"Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]":[-12,7,3.14,2],"Business Segments (Screen by Sum) (Details): % of Revenue [LTM]":[1,5,46,5]})
# data = data.values
# # # # kmeans = K(n_clusters=3).fit(data)
# # # # print(kmeans.cluster_centers_)
# # # # print("HERE")
# # # # k = KMeans(3,0.001)
# # # # k.cluster(data)
# # # # print(k.get_centroids())
        

# fast = FastGlobalKMeans(3, 0.001)
# clusters = fast.cluster(data)
# print(clusters)
# print(fast.get_labels())


# k = KMeans(K=5,error_tolerance=0.001)
# kmeans_clusters = k.cluster(X)


# fig, axes = plt.subplots(1, 3, figsize=(12, 5))



# for i, cluster in enumerate(clusters):
#     cluster_points = np.array(cluster)
#     axes[0].scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i+1}')

# for i, cluster in enumerate(kmeans_clusters):
#     cluster_points = np.array(cluster)
#     axes[2].scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i+1}')

# axes[1].scatter(X[:, 0], X[:, 1], c=labels_true, edgecolors='k', cmap=plt.cm.Paired, s=100)
# plt.tight_layout()
# plt.show()
# # db = B(threshold=1.7, n_clusters=100).fit(X)
# # # labels = db.labels_
# # # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# # print(n_clusters_)