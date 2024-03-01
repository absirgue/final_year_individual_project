import numpy as np
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.conclusion_1.algorithms_best_performance import AlgorithmsBestPerformanceEvaluation
from analysis.conclusion_2.clustering_results_analyzer import ClusteringResultsAnalyzer
from analysis.conclusion_2.manual_analysis_helper import ManualAnalysisHelper
from analysis.conclusion_3.rating_changes_identifier import RatingChangesIdentifier
from data_preparation.data_preparator import DataPreparator
from analysis.data_configuration import DataConfiguration
np.seterr(over='ignore')

# AlgorithmsBestPerformanceEvaluation().run_evaluation()
# AlgorithmsBestPerformanceEvaluation(run_pca=True).run_evaluation()
# ClusteringResultsAnalyzer("./conclusion_1_graphs/algorithms_comparisons/with_pca/performance_metrics.json", "./conclusion_2_results",True).analyse()
d = DataConfiguration()
d.set_to_default_configuration("CREDIT HEALTH")
DataPreparator(d,d.get_data_source()).apply_configuration(0.5)
# def pca_and_plot(data_array):
#     std_scaler = StandardScaler()
#     scaled_df = std_scaler.fit_transform(data_array)
#     nan_rows = np.isnan(scaled_df).any(axis=1)
#     cleaned_scaled_df = scaled_df[~nan_rows]
    
#     # Perform PCA with 3 components
#     pca = PCA(n_components=2)
#     reduced_data = pca.fit_transform(cleaned_scaled_df)
    
#     kmeans = KMeans(n_clusters=13)
#     kmeans.fit(reduced_data)
#     labels = kmeans.labels_
#     centroids = kmeans.cluster_centers_
#     print(reduced_data)
#     print(len(labels))
#     sum = 0
#     for i in labels:
#         if i <0:
#             sum+=1
#     print(sum)
#     # Plot the data points in 3D with cluster colors
#     plt.figure()
#     plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels, cmap='viridis', edgecolors='k', s=20, alpha=0.4)
#     plt.title('K-Means Clustering in 3D')
#     plt.xlabel('Feature 1')
#     plt.ylabel('Feature 2')
#     plt.show()

# data_configuration = DataConfiguration()
# data_configuration.set_to_default_configuration("RATIOS")
# data_preparator = DataPreparator(data_source=data_source,configuration=data_configuration)
# data = data_preparator.apply_configuration(0.8)
# print(data.shape)
# print(data[0])
# # pca_and_plot(data)
# non_noisy_data = OutlierRemover("CREDIT HEALTH").clean_of_outliers(data)
# print(sum)
# non_noisy_data = np.array(non_noisy_data)    
# print(non_noisy_data.shape)
# pca_and_plot(non_noisy_data)
