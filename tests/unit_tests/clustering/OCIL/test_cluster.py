import unittest
from clustering_algorithms.OCIL.cluster import Cluster
import math 
import pandas as pd
class TestOCILCluster(unittest.TestCase):


    def test_add_point_to_empty_cluster(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        self.assertEqual(cluster.points_count,1)
        self.assertEqual(cluster.numerical_values_centroid,[1,3,4])
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_1"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_1"],1)
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
    
    def test_add_point_to_non_empty_cluster_same_categorical_data(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[2,4,5])
        self.assertEqual(cluster.points_count,2)
        self.assertEqual(cluster.numerical_values_centroid,[1.5,3.5,4.5])
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_1"],2)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_1"],2)
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
    
    def test_add_point_to_non_empty_cluster_different_categorical_data(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_2","attr_2_val_2"],[2,4,5])
        self.assertEqual(cluster.points_count,2)
        self.assertEqual(cluster.numerical_values_centroid,[1.5,3.5,4.5])
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_1"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_1"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_2"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_2"],1)
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
          
    def test_remove_point_cluster_with_1_point(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.remove_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        self.assertEqual(cluster.points_count,0)
        self.assertEqual(cluster.numerical_values_centroid,[0,0,0])
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_1"],0)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_1"],0)
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
    
    def test_remove_point_cluster_2_points(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_2","attr_2_val_2"],[2,4,5])
        cluster.remove_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        self.assertEqual(cluster.points_count,1)
        self.assertEqual(cluster.numerical_values_centroid,[2,4,5])
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_1"],0)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_1"],0)
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_2"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_2"],1)
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
    
    def test_remove_point_cluster_3_points(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_2","attr_2_val_2"],[2,4,5])
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[10,8,7])
        cluster.remove_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        self.assertEqual(cluster.points_count,2)
        self.assertEqual(cluster.numerical_values_centroid,[6,6,6])
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_1"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_1"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[0]["attr_1_val_2"],1)
        self.assertEqual(cluster.categorical_attributes_frequency[1]["attr_2_val_2"],1)
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
    
    def test_cluster_is_initialized_as_expected(self):
        cluster = Cluster(2)
        self.assertEqual(cluster.points_count,0)
        self.assertEqual(cluster.numerical_values_centroid,[])
        self.assertEqual(cluster.categorical_attributes_frequency[0],{})
        self.assertEqual(cluster.categorical_attributes_frequency[1],{})
        self.assertEqual(len(cluster.categorical_attributes_frequency),2)
      
    def test_get_exp_difference_for_numerical_attributes_2_points_cluster(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_2","attr_2_val_2"],[11,3,6])
        self.assertAlmostEqual(math.exp(8.06226**2*-0.5),cluster.get_exp_difference_for_numerical_attributes([-2,3,4]))
    
    def test_get_similarity_for_categorical_attribute_config_1(self):
        cluster = Cluster(2)
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_2","attr_2_val_2"],[2,4,5])
        cluster.add_point(["attr_1_val_1","attr_2_val_1"],[10,8,7])
        cluster.add_point(["","attr_2_val_1"],[10,8,7])
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(0,"attr_1_val_1"),2/3)
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(1,"attr_2_val_1"),3/4)

    def test_get_similarity_for_categorical_attribute_config_2(self):
        cluster = Cluster(3)
        cluster.add_point(["","attr_2_val_1","attr_3_val_1"],[1,3,4])
        cluster.add_point(["","attr_2_val_2","attr_3_val_1"],[2,4,5])
        cluster.add_point(["","attr_2_val_1","attr_3_val_1"],[10,8,7])
        cluster.add_point(["","attr_2_val_1","attr_3_val_1"],[10,8,7])
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(0,"attr_1_val_1"),0)
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(1,"attr_2_val_1"),3/4)
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(2,"attr_3_val_1"),1)

    def test_get_similarity_for_categorical_attribute_config_3(self):
        cluster = Cluster(3)
        cluster.add_point(["attr_1_val_1",None,"attr_3_val_1"],[1,3,4])
        cluster.add_point(["attr_1_val_1","attr_2_val_2","attr_3_val_2"],[2,4,5])
        cluster.add_point(["attr_1_val_1","attr_2_val_1","attr_3_val_2"],[10,8,7])
        cluster.add_point(["attr_1_val_1","attr_2_val_1","attr_3_val_1"],[10,8,7])
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(0,"attr_1_val_2"),0)
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(1,"attr_2_val_1"),2/3)
        self.assertEqual(cluster.get_similarity_for_categorical_attribute(2,"attr_3_val_2"),1/2)
      