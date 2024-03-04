import unittest
from analysis.conclusion_1.iterators.birch_iterator import BIRCHIterator
from tests.unit_tests.analysis.conclusion_1.iterators.helper import get_random_2d_array
from sklearn.cluster import Birch
from sklearn.metrics import calinski_harabasz_score,silhouette_score

class TestBIRCHIterator(unittest.TestCase):

    def test_get_optimal_gives_expected_result(self):
        iterator = BIRCHIterator(None,3)
        performance_data = []
        for i in range(1,10):
            performance_data.append({"threshold":0,"branching factor":0,"Calinski Harabasz Index":i,"Silhouette Score":i,"time":0})
        calinski_best ={"threshold":1,"branching factor":1,"Calinski Harabasz Index":100,"Silhouette Score":50,"time":1}
        performance_data.append(calinski_best)
        for i in range(90,10,-1):
            performance_data.append({"threshold":0,"branching factor":0,"Calinski Harabasz Index":i,"Silhouette Score":i,"time":0})
        silhouette_best = {"threshold":1,"branching factor":1,"Calinski Harabasz Index":50,"Silhouette Score":100,"time":1}
        performance_data.append(silhouette_best)
        iterator.performance_data = performance_data
        iterator_optimal = iterator.get_optimal()
        self.assertEqual(iterator_optimal["Calinski Harabasz Index Optimum"]["Threshold Value"],calinski_best["threshold"])
        self.assertEqual(iterator_optimal["Silhouette Score Optimum"]["Branching Factor"],silhouette_best["branching factor"])
        self.assertEqual(iterator_optimal["Calinski Harabasz Index Optimum"]["Calinski Harabasz Index"],calinski_best["Calinski Harabasz Index"])
        self.assertEqual(iterator_optimal["Silhouette Score Optimum"]["Silhouette Score"],silhouette_best["Silhouette Score"])

    def test_get_optimal_fails_graciously_when_called_before_iterate(self):
        iterator = BIRCHIterator(None,3)
        self.assertEqual(iterator.get_optimal(),None)

    def test_iterate_saves_results_as_expected(self):
        data = get_random_2d_array()
        iterator = BIRCHIterator(data,3)
        iterator.MIN_BRANCHING_FACTOR = 2
        iterator.MAX_BRANCHING_FACTOR = 2
        iterator.MIN_THRESHOLD = 0.2
        iterator.MAX_THRESHOLD = 0.2
        iterator.iterate()
        clustering_alg = Birch(threshold=0.2,branching_factor=2,n_clusters=3).fit(data)
        labels = clustering_alg.labels_
        expected_calinski_harabasz= calinski_harabasz_score(data, labels) 
        expected_silhouette = silhouette_score(data, labels) 
        self.assertEqual(len(iterator.performance_data),1)
        self.assertEqual(iterator.performance_data[0]["threshold"],0.2)
        self.assertEqual(iterator.performance_data[0]["branching factor"],2)
        self.assertEqual(iterator.performance_data[0]["Calinski Harabasz Index"],expected_calinski_harabasz)
        self.assertEqual(iterator.performance_data[0]["Silhouette Score"],expected_silhouette)
       