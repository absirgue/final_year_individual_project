import unittest
from clustering.fast_global_k_means import FastGlobalKMeans
import pandas as pd
import numpy as np

class TestKMeans(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        self.data = pd.DataFrame({'col 1':[1,2,-9,-5.12],
                                  "col 2":[34,10,-8,-6.89],
                                  "col 3":[-12,-20,11.14,15],
                                  "col 4":[-10,-6.78,10,12]})
        self.data = self.data.values
        super().__init__(methodName)

    def test_fast_global_k_means_is_as_expected_for_4_clusters(self):
        k = FastGlobalKMeans(4,0.001)
        expected_clusters = [[[1,34,-12,-10]],[[2,10,-20,-6.78]],[[-9,-8,11.14,10]],[[-5.12,-6.89,15,12]]]
        correct_clusterings_count = 0
        repeats = 10
        for i in range(repeats):
            clusters = k.cluster(self.data)
            for cluster in clusters:
                true_clustering = len(clusters) == len(expected_clusters) and self.check_2D_arrays_contain_same_rows(cluster, expected_clusters[0]) or self.check_2D_arrays_contain_same_rows(cluster, expected_clusters[1]) or self.check_2D_arrays_contain_same_rows(cluster, expected_clusters[2]) or self.check_2D_arrays_contain_same_rows(cluster, expected_clusters[3])
            if true_clustering:
                correct_clusterings_count += 1
        self.assertEqual(correct_clusterings_count,repeats)

    def test_fast_global_k_means_is_as_expected_for_2_clusters(self):
        k = FastGlobalKMeans(2,0.001)
        expected_clusters = [[[1,34,-12,-10],[2,10,-20,-6.78]],[[-9,-8,11.14,10],[-5.12,-6.89,15,12]]]
        correct_clusterings_count = 0
        repeats = 100
        for i in range(repeats):
            clusters = k.cluster(self.data)
            true_clustering = False
            if len(clusters) == len(expected_clusters):
                true_clustering = True
            for cluster in clusters:
                true_clustering = true_clustering and self.check_2D_arrays_contain_same_rows(cluster, expected_clusters[0]) or self.check_2D_arrays_contain_same_rows(cluster, expected_clusters[1]) 
            if true_clustering:
                correct_clusterings_count += 1
        # we expect at least 50% success.
        self.assertGreater(correct_clusterings_count,repeats/2)

    def test_fast_global_k_can_not_be_greater_than_nb_of_data_points(self):
        with self.assertRaises(ValueError):
            k = FastGlobalKMeans(5,0.001)
            k.cluster(self.data)
    
    def check_2D_arrays_contain_same_rows(self,arr1, arr2):
        for row in arr1:
            if not self.is_array_in_2d_array(row, arr2):
                return False
        return True
    
    def is_array_in_2d_array(self,target_array, array_2d):
        for row in array_2d:
            if self.is_array_equal(target_array, row):
                return True
        return False
    
    def is_array_equal(self,arr1, arr2):
        if not len(arr1) == len(arr2):
            return False
        for i in range(len(arr1)):
            if not arr1[i] == arr2[i]:
                return False
        return True

       
