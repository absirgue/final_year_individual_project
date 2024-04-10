import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from graph.graphing_helper import GraphingHelper

class PrincipalComponentAnalysis:
    """
    Wrapper class for sklearn.decomposition.PCA enabling easier interfacing with other classes.
    """

    """
    Params:
        - data - the data we want to apply Principal Component Analysis on
        - dimensionality - the number of Pricinpal Components we want to reduce the data to.
    """
    def __init__(self,data,dimensionality):
        if data.shape[1] <2:
            raise ValueError("Data can not be reduced in dimensions.")
        if data.shape[1] < dimensionality:
            raise ValueError("Dimensionality demanded his superior to current dimenstionality.")
        self.data = data
        self.dimensionality = dimensionality
        self.explained_variance_ratio = 0
        self.reduce_dimensionality()
    
    # Returns the reduced data.
    def get_principal_components(self):
        return self.principal_components

    # Orchestrates the actual performance of PCA on the data set with a given number of desired
    # principal components.
    def reduce_dimensionality(self):
        std_scaler = StandardScaler()
        scaled_df = std_scaler.fit_transform(self.data)
        nan_rows = np.isnan(scaled_df).any(axis=1)
        cleaned_scaled_df = scaled_df[~nan_rows]
        pca = PCA(n_components=self.dimensionality)
        self.principal_components = pca.fit_transform(cleaned_scaled_df)
        self.explained_variance_ratio = pca.explained_variance_ratio_
        return self.principal_components

    """
    Returns a list of the explained variance represented by each of the obtained 
    Principal Components.
    """
    def get_explained_variance_ratios(self):
        return self.explained_variance_ratio

    """
    Returns the total explained variance ratio when reducing the given data set 
    to our deisred number of  Principal Components.
    """
    def get_total_explained_variance_ratio(self):
        return np.sum(self.explained_variance_ratio)


class PrincipalComponentAnalysisPerformanceMeasurement:
    """
    Measures and plots the performance (total explained variance ratio) of running PCA
    on a given data set across a given range of numbers of Principal Components.
    """

    def __init__(self,data,extra_title_precision=None):
        self.extra_title_precision =extra_title_precision
        self.data = data
    
    # Orchestrates all actions.
    def compute_and_plot_explained_variance_ratio_to_components_count(self,max_dimensionality_to_test = None):
        nb_features = self.data.shape[1]
        # The default maximum number of Principal Components we will test is the number of rows
        # in the data set.
        if not max_dimensionality_to_test:
            max_dimensionality_to_test = min(nb_features,self.data.shape[0])
        variance_ratios = self.calculate_explained_variance_ratios_across_components_count(max_dimensionality_to_test)
        self.plot(max_dimensionality_to_test,variance_ratios)
        return 1,variance_ratios

    """
    Iterates in performing PCA with each different number of Principal Componets.

    Returns:
        - a list presenting explained variance ratio for each of the number of 
        Principal Components tested.
    """
    def calculate_explained_variance_ratios_across_components_count(self,max_nb_component):
        explained_variance_ratios = []
        for components_count in range(1,max_nb_component+1):
            pca = PrincipalComponentAnalysis(self.data,components_count)
            pca.reduce_dimensionality()
            explained_variance_ratios.append(pca.get_total_explained_variance_ratio())
        return explained_variance_ratios
    
    """
    Coordinates actions to create a plot of the explained variance ratio across various 
    numbers of Principal Components.
    """
    def plot(self,max_nb_component,variance_ratios):
        d2_arr = []
        for i in range(max_nb_component):
            d2_arr.append([i+1,variance_ratios[i]])
        GraphingHelper().plot_2d_array_of_points(d2_arr,"Number of Components","Explained Variance Ratio",self.extra_title_precision+" PCA Number of Components to Explained Variance Ratio",folder_name="dimensionality_evaluation")