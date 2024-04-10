import unittest
from clustering_algorithms.OCIL.ocil import OCIL
from clustering_algorithms.OCIL.cluster import Cluster
import pandas as pd
import numpy as np

class TestOCILCluster(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        self.data = pd.DataFrame({'col 1':['attr_1_val_1','attr_1_val_2','attr_1_val_2','attr_1_val_3'],
                                  "col 2":[1,2,-3,-6.89],
                                  "col 3":['attr_2_val_1','attr_2_val_2','attr_2_val_1','attr_2_val_2'],
                                  "col 4":[-10,-6.78,10,12]})
        super().__init__(methodName)
    
    def test_weight_of_both_col_1_and_2_are_as_expected(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        ocil.compute_categorical_attributes_importance()
        # entropy of col 1 and col 3 should be equal and therefore both attributes should have equal weights
        self.assertAlmostEqual(ocil.categorical_attributes_importance[0],0.5)
        self.assertAlmostEqual(ocil.categorical_attributes_importance[1],0.5)
    
    def test_weight_of_both_col_1_and_2_are_as_expected_with_different_data(self):
        ocil = OCIL(2)
        data = pd.DataFrame({'col 1':['attr_1_val_1','attr_1_val_1','attr_1_val_1','attr_1_val_2'],
                                  "col 2":[1,2,-3,-6.89],
                                  "col 3":['attr_2_val_1','attr_2_val_2','attr_2_val_1','attr_2_val_2'],
                                  "col 4":[-10,-6.78,10,12]})
        ocil.initialization(data)
        ocil.compute_categorical_attributes_importance()
        self.assertAlmostEqual(ocil.categorical_attributes_importance[0],0.4479036728)
        self.assertAlmostEqual(ocil.categorical_attributes_importance[1],0.55209632)
    
    def test_categorical_similarity_calculation_is_as_intended(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        # Cluster 1 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [2,3].
        cluster_1 = Cluster(2)
        cluster_1.add_point(["attr_1_val_1","attr_2_val_1"],[1,2])
        cluster_1.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1]
        # Cluster 2 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [1,0].
        cluster_2 = Cluster(2)
        cluster_2.add_point(["attr_1_val_2","attr_2_val_1"],[-1,-4])
        cluster_2.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1,cluster_2]
        point = ["attr_1_val_1","attr_2_val_1",6,-1]
        expected_value = 1/4+1/4
        self.assertEqual(ocil.get_cluster_point_similarity_on_categorical_attributes(cluster_1,["attr_1_val_1","attr_2_val_1",6,-1]),expected_value)
    
    def test_categorical_similarity_calculation_is_as_intended_under_different_configuration(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        # Cluster 1 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_2 twice, and numerical centroid
        # [2,3].
        cluster_1 = Cluster(2)
        cluster_1.add_point(["attr_1_val_1","attr_2_val_2"],[1,2])
        cluster_1.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1]
        # Cluster 2 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [1,0].
        cluster_2 = Cluster(2)
        cluster_2.add_point(["attr_1_val_2","attr_2_val_1"],[-1,-4])
        cluster_2.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1,cluster_2]
        point = ["attr_1_val_1","attr_2_val_1",6,-1]
        expected_value = 1/4
        self.assertEqual(ocil.get_cluster_point_similarity_on_categorical_attributes(cluster_1,["attr_1_val_1","attr_2_val_1",6,-1]),expected_value)
    
    def test_overall_similarity_score_is_as_expected(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        # Cluster 1 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [2,3].
        cluster_1 = Cluster(2)
        cluster_1.add_point(["attr_1_val_1","attr_2_val_1"],[1,2])
        cluster_1.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1]
        # Cluster 2 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [1,0].
        cluster_2 = Cluster(2)
        cluster_2.add_point(["attr_1_val_2","attr_2_val_1"],[-1,-4])
        cluster_2.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1,cluster_2]
        point = ["attr_1_val_1","attr_2_val_1",6,-1]
        expected_value = 2/3*1/2 + 1/3*0.04742587317756679
        self.assertEqual(ocil.get_cluster_point_similarity(cluster_1,["attr_1_val_1","attr_2_val_1",6,-1]),expected_value)
    
    def test_overall_similarity_score_is_as_expected_for_cluster_2(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        # Cluster 1 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [2,3].
        cluster_1 = Cluster(2)
        cluster_1.add_point(["attr_1_val_1","attr_2_val_1"],[1,2])
        cluster_1.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1]
        # Cluster 2 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [1,0].
        cluster_2 = Cluster(2)
        cluster_2.add_point(["attr_1_val_2","attr_2_val_1"],[-1,-4])
        cluster_2.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1,cluster_2]
        point = ["attr_1_val_1","attr_2_val_1",6,-1]
        expected_value = 2/3*1/4 + 1/3*cluster_2.get_exp_difference_for_numerical_attributes([6,-1])/(cluster_1.get_exp_difference_for_numerical_attributes([6,-1])+cluster_2.get_exp_difference_for_numerical_attributes([6,-1]))
        self.assertAlmostEqual(ocil.get_cluster_point_similarity(cluster_2,["attr_1_val_1","attr_2_val_1",6,-1]),expected_value)

    def test_best_cluster_is_correctly_selected(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        # Cluster 1 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [2,3].
        cluster_1 = Cluster(2)
        cluster_1.add_point(["attr_1_val_1","attr_2_val_1"],[1,2])
        cluster_1.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1]
        # Cluster 2 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [1,0].
        cluster_2 = Cluster(2)
        cluster_2.add_point(["attr_1_val_2","attr_2_val_1"],[-1,-4])
        cluster_2.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1,cluster_2]
        point = ["attr_1_val_1","attr_2_val_1",6,-1]
        expected_value = 2/3*1/4 + 1/3*cluster_2.get_exp_difference_for_numerical_attributes([6,-1])/(cluster_1.get_exp_difference_for_numerical_attributes([6,-1])+cluster_2.get_exp_difference_for_numerical_attributes([6,-1]))
        self.assertAlmostEqual(ocil.get_cluster_point_similarity(cluster_2,["attr_1_val_1","attr_2_val_1",6,-1]),expected_value)
        self.assertEqual(ocil.get_max_similarity_cluster_idx(point),1)
    
    
    def test_numerical_similarity_calculation_is_as_intended(self):
        ocil = OCIL(2)
        ocil.initialization(self.data)
        # Cluster 1 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [2,3].
        cluster_1 = Cluster(2)
        cluster_1.add_point(["attr_1_val_1","attr_2_val_1"],[1,2])
        cluster_1.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1]
        # Cluster 2 has attribute 0 with values attr_1_val_1 and attr_1_val_2 each once,
        # attribute 1 with values attr_2_val_1 and attr_2_val_2 each once, and numerical centroid
        # [1,0].
        cluster_2 = Cluster(2)
        cluster_2.add_point(["attr_1_val_2","attr_2_val_1"],[-1,-4])
        cluster_2.add_point(["attr_1_val_2","attr_2_val_2"],[3,4])
        ocil.clusters = [cluster_1,cluster_2]
        expected_value = cluster_1.get_exp_difference_for_numerical_attributes([6,-1])/(cluster_1.get_exp_difference_for_numerical_attributes([6,-1])+cluster_2.get_exp_difference_for_numerical_attributes([6,-1]))
        self.assertEqual(ocil.get_cluster_point_similarity_on_numerical_attributes(cluster_1,["attr_1_val_1","attr_2_val_1",6,-1]),expected_value)

    def test_organise_data_by_type_only_numerical(self):
        data = {
        'Num1': [1, None, -3, -2],
        'Num2': [1, 2, 3, 4],
        'Num3': [3.14, np.nan, 1, 2]}
        df = pd.DataFrame(data)
        data_frame, categorical_count = OCIL(0).organise_data_by_type(df)
        self.assertEqual(categorical_count,0)
        self.assertTrue(data_frame.equals(df))

    def test_organise_data_by_type_only_categorical(self):
        data = {
        'Color': ['blue', 'red', 'yellow', 'orange'],
        'Animals': ['cat', 'dog', 'parrot', 'fox'],
        'Greetings': ['hi', 'hello', 'good morning', 'good afternoon']}
        df = pd.DataFrame(data)
        data_frame, categorical_count = OCIL(0).organise_data_by_type(df)
        self.assertEqual(categorical_count,3)
        self.assertTrue(data_frame.equals(df))
    
    def test_organise_data_mixed_data(self):
        data = {
        'Num1': [1, None, -3, -2],
        'Color': ['blue', 'red', 'yellow', 'orange'],
        'Num2': [1, 2, 3, 4],
        'Animals': ['cat', 'dog', 'parrot', 'fox'],
        'Greetings': ['hi', 'hello', 'good morning', 'good afternoon'],
        'Num3': [3.14, np.nan, 1, 2]}
        df = pd.DataFrame(data)
        data_frame, categorical_count = OCIL(0).organise_data_by_type(df)
        expected_data = {
        'Color': ['blue', 'red', 'yellow', 'orange'],
        'Animals': ['cat', 'dog', 'parrot', 'fox'],
        'Greetings': ['hi', 'hello', 'good morning', 'good afternoon'],
        'Num1': [1, None, -3, -2],
        'Num2': [1, 2, 3, 4],
        'Num3': [3.14, np.nan, 1, 2]}
        expected_df = pd.DataFrame(expected_data)
        self.assertEqual(categorical_count,3)
        self.assertTrue(data_frame.equals(expected_df))