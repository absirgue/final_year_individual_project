import unittest
import numpy as np
from analysis.clusters_analysis.credit_rating_analyzer import CreditRatingAnalyzer
from analysis.clusters_analysis.credit_rating_cluster import CreditRatingCluster
from analysis.clusters_analysis.clusters_analyzer import ClustersAnalyzer

class TestCreditRatingCluster(unittest.TestCase):

    def test_get_credit_ratings_shares_gives_expected_result(self):
        cr_cluster = CreditRatingCluster(0,0)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        result = cr_cluster.get_credit_ratings_shares()
        self.assertEqual(len(result.keys()),4)
        self.assertEqual(result["1"],4/10)
        self.assertEqual(result["2"],2/10)
        self.assertEqual(result["4"],3/10)
        self.assertEqual(result["10"],1/10)

    def test_get_credit_ratings_shares_gives_expected_result_when_no_data(self):
        cr_cluster = CreditRatingCluster(0,0)
        result = cr_cluster.get_credit_ratings_shares()
        self.assertEqual(len(result.keys()),0)
    
    def test_get_is_significant_cluster_with_significant_cluster(self):
        cr_cluster = CreditRatingCluster(3,0.1)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        self.assertTrue(cr_cluster.get_is_significant_cluster())
    
    def test_get_is_significant_cluster_not_significant_cluster_bcs_signficance_split(self):
        cr_cluster = CreditRatingCluster(3,0.5)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        self.assertFalse(cr_cluster.get_is_significant_cluster())
                        
    def test_get_is_significant_cluster_not_significant_cluster_bcs_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        self.assertFalse(cr_cluster.get_is_significant_cluster())
    
    def test_get_credit_ratings_held_in_significant_proportions_proportion_1(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        self.assertEqual(cr_cluster.get_credit_ratings_held_in_significant_proportions(0.39),["1"])

    def test_get_credit_ratings_held_in_significant_proportions_proportion_2(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        self.assertEqual(cr_cluster.get_credit_ratings_held_in_significant_proportions(0.1),["1","2","4"])
    
    def test_get_credit_ratings_held_in_significant_proportions_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        self.assertEqual(cr_cluster.get_credit_ratings_held_in_significant_proportions(0.1),[])

    def test_get_credit_ratings_shares_gives_expected_result(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        result = cr_cluster.get_credit_ratings_shares()
        self.assertEqual(len(result.keys()),4)
        self.assertEqual(result["AAA"],0.4)
        self.assertEqual(result["AA+"],0.2)
        self.assertEqual(result["AA-"],0.3)
        self.assertEqual(result["BBB-"],0.1)
    
    def test_get_credit_ratings_shares_gives_expected_result_when_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        result = cr_cluster.get_credit_ratings_shares()
        self.assertEqual(len(result.keys()),0)
    
    def test_get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances_gives_expected_results_cr_1(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.data = {"1":[[1,2,3],[-1,-2,-3],[4,5,6]],"2":[[-4,-5,-6],[10,11,12],[4,4,4]]}
        result = cr_cluster.get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(0,"1")
        self.assertEqual(result["Mean"],4/3)
        self.assertEqual(result["Median"],1)
        self.assertEqual(result["1st Quartile"],0)
        self.assertEqual(result["3rd Quartile"],2.5)
        self.assertAlmostEqual(result["Standard Deviation"],2.0548046676)

    def test_get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances_gives_expected_results_cr_2(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.data = {"1":[[1,2,3],[-1,-2,-3],[4,5,6]],"2":[[-4,-5,-6],[10,11,12],[4,4,4]]}
        result = cr_cluster.get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(1,"2")
        self.assertEqual(result["Mean"],10/3)
        self.assertEqual(result["Median"],4)
        self.assertEqual(result["1st Quartile"],-0.5)
        self.assertEqual(result["3rd Quartile"],7.5)
        self.assertAlmostEqual(result["Standard Deviation"],6.5489609014)
    
    def test_get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances_when_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        result = cr_cluster.get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(1,"2")
        self.assertEqual(result, None)

    def test_get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances_when_inexisting_col_idx(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.data = {"1":[[1,2,3],[-1,-2,-3],[4,5,6]],"2":[[-4,-5,-6],[10,11,12],[4,4,4]]}
        result = cr_cluster.get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(12,"2")
        self.assertEqual(result, None)
    
    def test_get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances_when_inexisting_credit_rating(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.data = {"1":[[1,2,3],[-1,-2,-3],[4,5,6]],"2":[[-4,-5,-6],[10,11,12],[4,4,4]]}
        result = cr_cluster.get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(1,"12")
        self.assertEqual(result, None)

    def test_get_rating_range_scenar_1(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":1,"2":2}
        self.assertEqual(cr_cluster.get_rating_range(),1)
    
    def test_get_rating_range_scenar_2(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":1,"12":2,"3":3}
        self.assertEqual(cr_cluster.get_rating_range(),11)
    
    def test_get_rating_range_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        self.assertEqual(cr_cluster.get_rating_range(),None)

    def test_get_measures_of_location_and_dispersion_for_credit_ratings_values(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":1,"12":2,"3":3}
        result= cr_cluster.get_measures_of_location_and_dispersion_for_credit_ratings_values()
        self.assertEqual(result["Mean"],34/6)
        self.assertEqual(result["Median"],3)
        self.assertEqual(result["1st Quartile"],3)
        self.assertEqual(result["3rd Quartile"],9.75)
        self.assertAlmostEqual(result["Standard Deviation"],4.533823502)
        self.assertTrue(result["Is Signficant"])
    
    def test_get_measures_of_location_and_dispersion_for_credit_ratings_values_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        result= cr_cluster.get_measures_of_location_and_dispersion_for_credit_ratings_values()
        self.assertEqual(result,None)
    
    def test_get_entropy_gets_expected_result(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.credit_ratings_counts = {"1":5,"12":2,"3":3}
        result= cr_cluster.get_entropy()
        self.assertAlmostEqual(result,1.485475297)
    
    def test_get_entropy_when_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        result= cr_cluster.get_entropy()
        self.assertAlmostEqual(result,None)
    
    def test_get_entropy_when_no_data(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        result= cr_cluster.get_entropy()
        self.assertAlmostEqual(result,None)
     
    def test_add_clustered_credit_rating_first_data_point(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.add_clustered_credit_rating("1",[1,2,3],1)
        self.assertEqual(cr_cluster.get_companies_count(),1)
        self.assertEqual(cr_cluster.get_credit_ratings_counts(),{"1":1})
        self.assertEqual(cr_cluster.data,{"1":[[1,2,3]]})

    def test_add_clustered_credit_rating_data_point_with_same_rating(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.add_clustered_credit_rating("1",[1,2,3],0)
        cr_cluster.add_clustered_credit_rating("1",[3,4,5],0)
        self.assertEqual(cr_cluster.get_companies_count(),2)
        self.assertEqual(cr_cluster.get_credit_ratings_counts(),{"1":2})
        self.assertEqual(cr_cluster.data,{"1":[[1,2,3],[3,4,5]]})
    
    def test_add_clustered_credit_rating_data_point_with_other_rating(self):
        cr_cluster = CreditRatingCluster(9,0.1)
        cr_cluster.add_clustered_credit_rating("1",[1,2,3],0)
        cr_cluster.add_clustered_credit_rating("1",[3,4,5],0)
        cr_cluster.add_clustered_credit_rating("2",[-3,6,-8],0)
        self.assertEqual(cr_cluster.get_companies_count(),3)
        self.assertEqual(cr_cluster.get_credit_ratings_counts(),{"1":2,"2":1})
        self.assertEqual(cr_cluster.data,{"1":[[1,2,3],[3,4,5]],"2":[[-3,6,-8]]})