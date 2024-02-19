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
from analysis.conclusion_1.kmeans_iterator import KMeansIterator
from analysis.conclusion_1.birch_iterator import BIRCHIterator
from analysis.conclusion_1.fuzzy_cmean_iterator import FuzzyCMeansIterator
from analysis.conclusion_1.dbscan_iterator import DBSCANIterator
from analysis.conclusion_1.fast_global_kmeans_iterator import FastGlobalKMeansIterator
from analysis.conclusion_1.birch_super_iterator import BIRCHSuperIterator

np.seterr(over='ignore')

class DataSource:
    def __init__(self,path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name

data_source = DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")


optimal_col_emptiness_ratios_for_default_config = {'RATIOS': 0.8, 'RAW NUMBERS': 0.45, 'BOTH': 0.8}
optimal_dimensionalities_for_default_configs = {'RATIOS': 37, 'RAW NUMBERS': 37, 'BOTH': 46}

config = DataConfiguration()
config.set_to_default_configuration("RATIOS")
data = DataPreparator(data_source=data_source,configuration=config).apply_configuration(0.8)
# it = BIRCHSuperIterator(data,4)
# it.iterate()
# it.graph()
# print(it.get_optimal())

# EmptyRowsDeletionEvaluation().run_evaluation(data_source)
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