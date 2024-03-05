import numpy as np
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.conclusion_1.algorithms_performances_evaluation import AlgorithmsPerformancesEvaluation
from analysis.conclusion_2.clustering_results_analyzer import ClusteringResultsAnalyzer
from analysis.conclusion_2.manual_analysis_helper import ManualAnalysisHelper
from analysis.conclusion_3.rating_changes_identifier import RatingChangesIdentifier
from data_preparation.data_preparator import DataPreparator
from analysis.conclusion_1.iterators.kmeans_iterator import KMeansIterator
from analysis.data_configuration import DataConfiguration
from analysis.conclusion_2.analysers.kmeans_analyser import KMeansAnalyser
from analysis.conclusion_2.credit_rating_analyzer import CreditRatingAnalyzer
np.seterr(over='ignore')

class DataConfigurationWrapper:

    def __init__(self):
        self.create_config_packages()

    def get_config_packages(self, pkg_id):
        return self.config_packages[pkg_id]

    def create_config_packages(self):
        self.config_packages = {}
        self.config_packages["ALL"] = self.get_all_configs()
        self.config_packages["RAW NUMBERS AND RATIOS"] = self.get_raw_nb_and_ratios_configs()
        self.config_packages["CREDIT HEALTH AND CREDIT MODEL"] = self.get_credit_health_and_credit_model()
        self.config_packages["ALL - COMPLEX"] = self.get_all_configs(complex=True)
        self.config_packages["CREDIT HEALTH AND CREDIT MODEL - COMPLEX"] = self.get_credit_health_and_credit_model(complex=True)

    def get_all_configs(self,complex=False):
        raw_nb_and_ratios_configs = self.get_raw_nb_and_ratios_configs()
        credit_health_and_credit_model = self.get_credit_health_and_credit_model(complex)
        return credit_health_and_credit_model.update(raw_nb_and_ratios_configs)

    def get_raw_nb_and_ratios_configs(self):
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS")
        both_config_ratios_and_raw_numbers = DataConfiguration()
        both_config_ratios_and_raw_numbers.set_to_default_configuration("BOTH RATIOS AND RAW NUMBERS")
        return {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH RATIOS AND RAW NUMBERS":both_config_ratios_and_raw_numbers,"CREDIT MODEL":credit_model_config,"CREDIT HEALTH":credit_health__config,"BOTH CREDIT HEALTH AND CREDIT MODEL":both_config_credit_health_and_credit_model}
    
    def get_credit_health_and_credit_model(self,complex=False):
        configs = {}
        credit_health_config = DataConfiguration()
        credit_health_config.set_to_default_configuration("CREDIT HEALTH")
        configs["CREDIT HEALTH"] = credit_health_config
        credit_model_config = DataConfiguration()
        credit_model_config.set_to_default_configuration("CREDIT MODEL")
        configs["CREDIT MODEL"] = credit_model_config
        both_config_credit_health_and_credit_model = DataConfiguration()
        both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL")
        configs["BOTH CREDIT HEALTH AND CREDIT MODEL"] = both_config_credit_health_and_credit_model
        if complex:
            for config_nb in range(1,4):
                credit_health_config = DataConfiguration()
                credit_health_config.set_to_default_configuration("CREDIT HEALTH",average_by_category=config_nb)
                configs["CREDIT HEALTH"+credit_health_config.get_appendix_for_averager_modif_of_config()] = credit_health_config
                credit_model_config = DataConfiguration()
                credit_model_config.set_to_default_configuration("CREDIT MODEL",average_by_category=config_nb)
                configs["CREDIT MODEL"+credit_model_config.get_appendix_for_averager_modif_of_config()] = credit_model_config
                both_config_credit_health_and_credit_model = DataConfiguration()
                both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",average_by_category=config_nb)
                configs["BOTH CREDIT HEALTH AND CREDIT MODEL"+both_config_credit_health_and_credit_model.get_appendix_for_averager_modif_of_config()] = both_config_credit_health_and_credit_model
        return configs


d = DataConfiguration()
d.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",average_by_category=3)
prep = DataPreparator(d,d.get_data_source())
data = prep.apply_configuration(0.5)
it = KMeansIterator(data,20)
it.iterate()
print(it.get_optimal())


# AlgorithmsPerformancesEvaluation().run_evaluation()
# AlgorithmsPerformancesEvaluation(run_pca=True).run_evaluation()
# ClusteringResultsAnalyzer("./conclusion_1_graphs/algorithms_comparisons/with_pca/performance_metrics.json", "./conclusion_2_results",True).analyse()


# d = DataConfiguration()
# d.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",average_by_category=True)
# prep = DataPreparator(d,d.get_data_source())
# data = prep.apply_configuration(0.5)
# print(len(data))
# credit_ratings = prep.get_credit_ratings()
# print(len(credit_ratings))
# credit_ratings_analysers = {}
# for cr_idx in range(len(credit_ratings)):
#     if credit_ratings[cr_idx] in credit_ratings_analysers.keys():
#         analyser = credit_ratings_analysers[credit_ratings[cr_idx]]
#         analyser.insert_company(credit_ratings[cr_idx], data[cr_idx])
#     else:
#         analyser = CreditRatingAnalyzer()
#         analyser.insert_company(credit_ratings[cr_idx], data[cr_idx])
#         credit_ratings_analysers[credit_ratings[cr_idx]] = analyser
# print(prep.get_column_names())
# KMeansAnalyser(list(prep.get_column_names()),prep.get_encoding_of_first_junk_rating(),"./test",data,prep.get_credit_ratings(),credit_ratings_analysers).analyse({"K":13,"WCSS":0,"Calinski Harabasz Index":0,"Silhouette Score":0})


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
