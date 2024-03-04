import unittest
import math
import numpy as np
from skfuzzy.cluster import cmeans
from analysis.conclusion_1.iterators.fuzzy_cmean_iterator import FuzzyCMeansIterator
from tests.unit_tests.analysis.conclusion_1.iterators.helper import get_random_2d_array
from sklearn.cluster import Birch
from sklearn.metrics import calinski_harabasz_score,silhouette_score

class TestFuzzyCMeansIterator(unittest.TestCase):

    def test_get_optimal_gives_expected_result(self):
        iterator = FuzzyCMeansIterator(np.array([]),2)
        performance_data = [{'C': 2, 'time': 0.021783781051635743, 'Calinski Harabasz Index': 1760.562342962464, 'Silhouette Score': 0.9121173323821766, 'WCSS': 417536337914.2912}, {'C': 3, 'time': 0.015134763717651368, 'Calinski Harabasz Index': 3450.309020004752, 'Silhouette Score': 0.8341674160956891, 'WCSS': 170697492839.6624}, {'C': 4, 'time': 0.012144041061401368, 'Calinski Harabasz Index': 3873.4575041122343, 'Silhouette Score': 0.8227740412009108, 'WCSS': 106721161601.56282}, {'C': 5, 'time': 0.01652984619140625, 'Calinski Harabasz Index': 5480.4782499743715, 'Silhouette Score': 0.7755919091371386, 'WCSS': 60755474640.35763}, {'C': 6, 'time': 0.01188812255859375, 'Calinski Harabasz Index': 9025.517218092355, 'Silhouette Score': 0.7205905177553892, 'WCSS': 30216486447.35827}, {'C': 7, 'time': 0.01130661964416504, 'Calinski Harabasz Index': 10297.093480874555, 'Silhouette Score': 0.7035160374009493, 'WCSS': 22283990427.115685}, {'C': 8, 'time': 0.013953638076782227, 'Calinski Harabasz Index': 12460.950669226397, 'Silhouette Score': 0.6596852024942864, 'WCSS': 15906278800.382183}, {'C': 9, 'time': 0.0199432373046875, 'Calinski Harabasz Index': 14230.883257831967, 'Silhouette Score': 0.646011649762762, 'WCSS': 12394488955.872108}, {'C': 10, 'time': 0.05941023826599121, 'Calinski Harabasz Index': 15273.007544343845, 'Silhouette Score': 0.6299407411622548, 'WCSS': 10148265319.403597}, {'C': 11, 'time': 0.07069616317749024, 'Calinski Harabasz Index': 16764.64402072547, 'Silhouette Score': 0.6106229378430907, 'WCSS': 8335765894.023146}, {'C': 12, 'time': 0.01194934844970703, 'Calinski Harabasz Index': 17479.137397859704, 'Silhouette Score': 0.611386837308306, 'WCSS': 7303745668.531858}, {'C': 13, 'time': 0.0354670524597168, 'Calinski Harabasz Index': 19862.626824758776, 'Silhouette Score': 0.6017919505354284, 'WCSS': 5876021292.7865925}, {'C': 14, 'time': 0.013143157958984375, 'Calinski Harabasz Index': 20915.52293476081, 'Silhouette Score': 0.5725104952168565, 'WCSS': 5163547860.804665}, {'C': 15, 'time': 0.014600133895874024, 'Calinski Harabasz Index': 22978.837963331145, 'Silhouette Score': 0.5802360839502959, 'WCSS': 4365777875.76216}, {'C': 16, 'time': 0.0131134033203125, 'Calinski Harabasz Index': 26030.233064086497, 'Silhouette Score': 0.5842687630885541, 'WCSS': 3585933714.909463}, {'C': 17, 'time': 0.014621210098266602, 'Calinski Harabasz Index': 27484.161560736655, 'Silhouette Score': 0.5753972922638505, 'WCSS': 3182792235.688008}, {'C': 18, 'time': 0.013977670669555664, 'Calinski Harabasz Index': 28685.887388352996, 'Silhouette Score': 0.5605748764447698, 'WCSS': 2871566383.9746184}, {'C': 19, 'time': 0.04431805610656738, 'Calinski Harabasz Index': 29577.342541577666, 'Silhouette Score': 0.5668573140187132, 'WCSS': 2637985849.507469}, {'C': 20, 'time': 0.19248151779174805, 'Calinski Harabasz Index': 31835.964135734237, 'Silhouette Score': 0.5576883753485933, 'WCSS': 2312336591.9990892}]
        iterator.performance_data = performance_data
        iterator_optimal = iterator.get_optimal()
        self.assertEqual(iterator_optimal["C"],6)
        self.assertEqual(iterator_optimal["WCSS"],30216486447.35827)
        self.assertEqual(iterator_optimal["Silhouette Score"],0.7205905177553892)
        self.assertEqual(iterator_optimal["Calinski Harabasz Index"],9025.517218092355)

    def test_get_optimal_fails_graciously_when_called_before_iterate(self):
        iterator = FuzzyCMeansIterator(np.array([]))
        self.assertEqual(iterator.get_optimal(),None)

    def test_iterate_saves_results_as_expected(self):
        data = get_random_2d_array()
        iterator = FuzzyCMeansIterator(data,2,10)
        iterator.iterate()
        expected_calinski_harabasz = 0
        expected_silhouette = 0
        expected_wcss = 0
        nb_iter = 10
        for i in range(nb_iter):
            cntr, u, _, _, _, _, _ = cmeans(data.T, c=2, m=2,error=0.001,maxiter=400)
            fuzzy_cluster_labels = np.argmax(u, axis=0)
            expected_calinski_harabasz+= calinski_harabasz_score(data, fuzzy_cluster_labels)
            expected_silhouette += silhouette_score(data, fuzzy_cluster_labels)
            expected_wcss += np.sum(np.power(np.linalg.norm(data.T - cntr.T[:, fuzzy_cluster_labels], axis=1), 2))
        self.assertEqual(len(iterator.performance_data),1)
        self.assertEqual(iterator.performance_data[0]["C"],2)
        self.assertGreater(iterator.performance_data[0]["Calinski Harabasz Index"],(expected_calinski_harabasz/nb_iter)-3)
        self.assertLess(iterator.performance_data[0]["Calinski Harabasz Index"],(expected_calinski_harabasz/nb_iter)+3)
        self.assertGreater(iterator.performance_data[0]["Silhouette Score"],(expected_silhouette/nb_iter)-3)
        self.assertLess(iterator.performance_data[0]["Silhouette Score"],(expected_silhouette/nb_iter)+3)
        self.assertGreater(iterator.performance_data[0]["WCSS"],(expected_wcss/nb_iter)-3)
        self.assertLess(iterator.performance_data[0]["WCSS"],(expected_wcss/nb_iter)+3)

       