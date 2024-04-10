import unittest
from analysis.hyperparameters_optimisation.iterators.dbscan_iterator import DBSCANIterator
from tests.unit_tests.analysis.conclusion_1.iterators.helper import get_random_2d_array
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score,silhouette_score

class TestDBSCANIterator(unittest.TestCase):

    def test_get_optimal_gives_expected_result(self):
        iterator = DBSCANIterator(None)
        performance_data = []
        for i in range(1,10):
            performance_data.append({"cluster counts":0,"eps":0,"min pts":0,"Calinski Harabasz Index":i,"Silhouette Score":i,"time":0})
        calinski_best ={"cluster counts":1,"eps":1,"min pts":1,"Calinski Harabasz Index":100,"Silhouette Score":50,"time":1}
        performance_data.append(calinski_best)
        for i in range(90,10,-1):
            performance_data.append({"cluster counts":0,"eps":0,"min pts":0,"Calinski Harabasz Index":i,"Silhouette Score":i,"time":0})
        silhouette_best = {"cluster counts":1,"eps":1,"min pts":1,"Calinski Harabasz Index":50,"Silhouette Score":100,"time":1}
        performance_data.append(silhouette_best)
        iterator.performance_data = performance_data
        iterator_optimal = iterator.get_optimal()
        self.assertEqual(iterator_optimal["Calinski Harabasz Index Optimum"]["MinPts"],calinski_best["min pts"])
        self.assertEqual(iterator_optimal["Silhouette Score Optimum"]["Eps"],silhouette_best["eps"])
        self.assertEqual(iterator_optimal["Calinski Harabasz Index Optimum"]["Calinski Harabasz Index"],calinski_best["Calinski Harabasz Index"])
        self.assertEqual(iterator_optimal["Silhouette Score Optimum"]["Silhouette Score"],silhouette_best["Silhouette Score"])

    def test_get_optimal_fails_graciously_when_called_before_iterate(self):
        iterator = DBSCANIterator(None)
        self.assertEqual(iterator.get_optimal(),None)

    def test_iterate_saves_results_as_expected(self):
        data = get_random_2d_array()
        iterator = DBSCANIterator(data)
        iterator.MIN_EPS = 0.5
        iterator.MAX_EPS = 0.5
        iterator.MIN_MIN_PTS = 3
        iterator.MAX_MIN_PTS = 3
        iterator.iterate()
        clustering_alg = DBSCAN(eps=0.5,min_samples=3).fit(data)
        labels = clustering_alg.labels_
        expected_calinski_harabasz= calinski_harabasz_score(data, labels) 
        expected_silhouette = silhouette_score(data, labels) 
        self.assertEqual(len(iterator.performance_data),1)
        self.assertEqual(iterator.performance_data[0]["min pts"],3)
        self.assertEqual(iterator.performance_data[0]["eps"],0.5)
        self.assertAlmostEqual(iterator.performance_data[0]["Calinski Harabasz Index"],round(expected_calinski_harabasz,3))
        self.assertAlmostEqual(iterator.performance_data[0]["Silhouette Score"],round(expected_silhouette,3))
       