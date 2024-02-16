import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class PrincipalComponentAnalysis:

    def __init__(self,data,dimensionality):
        if len(data.columns) <2:
            raise ValueError("Data can not be reduced in dimensions.")
        if len(data.columns) < dimensionality:
            raise ValueError("Dimensionality demanded his superior to current dimenstionality.")
        self.data = data
        self.explained_variance_ratio = 0
        self.pca = self.reduce_dimensionality(dimensionality)
    
    def get_principal_components(self):
        return self.principal_components

    def reduce_dimensionality(self,dimensionality):
        std_scaler = StandardScaler()
        scaled_df = std_scaler.fit_transform(self.data)
        # Remove any NaN valuve from data not fitting scaling calculations.
        nan_rows = np.isnan(scaled_df).any(axis=1)
        cleaned_scaled_df = scaled_df[~nan_rows]
        
        df_1 = pd.DataFrame(self.data)
        excel_file_path = 'data.xlsx'
        df_1.to_excel(excel_file_path, index=False)

        df = pd.DataFrame(scaled_df)
        excel_file_path = 'output.xlsx'
# Export DataFrame to Excel
        df.to_excel(excel_file_path, index=False)

        pca = PCA(n_components=dimensionality)
        self.principal_components = pca.fit_transform(cleaned_scaled_df)
        self.explained_variance_ratio = pca.explained_variance_ratio_

    def get_explained_variance_ratios(self):
        return self.explained_variance_ratio

    def get_total_explained_variance_ratio(self):
        return np.sum(self.explained_variance_ratio)


class PrincipalComponentAnalysisPerformanceMeasurement:

    def __init__(self,data,extra_title_precision=None):
        self.extra_title_precision =extra_title_precision
        self.data = data
    
    def compute_and_plot_explained_variance_ratio_to_components_count(self,max_dimensionality_to_test = None):
        nb_features = len(self.data.axes[1])
        if not max_dimensionality_to_test:
            max_dimensionality_to_test = nb_features
        variance_ratios = self.calculate_explained_variance_ratios_across_components_count(max_dimensionality_to_test)
        self.plot(max_dimensionality_to_test,variance_ratios)
        return 1,variance_ratios

    def calculate_explained_variance_ratios_across_components_count(self,max_nb_component):
        explained_variance_ratios = []
        for components_count in range(1,max_nb_component+1):
            pca = PrincipalComponentAnalysis(self.data,components_count)
            explained_variance_ratios.append(pca.get_total_explained_variance_ratio())
        return explained_variance_ratios
    
    def plot(self,max_nb_component,variance_ratios):
        plt.figure()
        plt.grid()
        plt.plot(np.arange(1,max_nb_component+1),variance_ratios,marker='o')
        plt.xlabel('Number of Components')
        plt.ylabel('Explained Variance Ratio')
        graph_title = 'PCA Number of Components to Explained Variance Ratio'
        if self.extra_title_precision:
            graph_title += " " + self.extra_title_precision
        plt.title(graph_title)
        plt.savefig(graph_title+'.png')