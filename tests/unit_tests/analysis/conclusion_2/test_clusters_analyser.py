import unittest
from analysis.clusters_analysis.credit_rating_analyzer import CreditRatingAnalyzer
from analysis.clusters_analysis.credit_rating_cluster import CreditRatingCluster
from analysis.clusters_analysis.clusters_analyzer import ClustersAnalyzer

class TestClustersAnalyser(unittest.TestCase):

    def test_get_cluster_cr_shares_gives_expected_results_many_cr_in_1_cluster(self):
        cr_cluster = CreditRatingCluster(0,0)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        cr_cluster.companies_count = 10
        result = ClustersAnalyzer(None,None,None,None,None,None).get_cluster_cr_shares([cr_cluster])
        result = result[0]
        self.assertEqual(result["AAA"],0.4)
        self.assertEqual(result["AA+"],0.2)
        self.assertEqual(result["AA-"],0.3)
        self.assertEqual(result["BBB-"],0.1)

    def test_get_cluster_cr_shares_gives_expected_results_many_cr_in_2_cluster(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        cr_cluster1.companies_count = 10
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":1,"13":1,"14":3}
        cr_cluster2.companies_count = 5
        result = ClustersAnalyzer(None,None,None,None,None,None).get_cluster_cr_shares([cr_cluster1,cr_cluster2])
        self.assertEqual(result[0]["AAA"],0.4)
        self.assertEqual(result[0]["AA+"],0.2)
        self.assertEqual(result[0]["AA-"],0.3)
        self.assertEqual(result[0]["BBB-"],0.1)
        self.assertEqual(result[1]["BB"],0.2)
        self.assertEqual(result[1]["BB-"],0.2)
        self.assertEqual(result[1]["B+"],0.6)

    def test_get_cluster_cr_shares_gives_expected_results_no_cr(self):
        cr_cluster = CreditRatingCluster(0,0)
        cr_cluster.credit_ratings_counts = {}
        cr_cluster.companies_count = 0
        result = ClustersAnalyzer(None,None,None,None,None,None).get_cluster_cr_shares([cr_cluster])
        result = result[0]
        self.assertEqual(len(result),0)
    
    def test_get_clusters_share_of_overal_credit_ratings_gives_expected_result_1_cr_cluster(self):
        cr_cluster = CreditRatingCluster(0,0)
        cr_cluster.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        cr_cluster.data = ["test"]*10
        cr_analyser = ClustersAnalyzer([],"",None,None,None,None,None,None)
        analyser_1 = CreditRatingAnalyzer()
        analyser_1.data = ["test"]*5
        analyser_2 = CreditRatingAnalyzer()
        analyser_2.data = ["test"]*4
        analyser_4 = CreditRatingAnalyzer()
        analyser_4.data = ["test"]*10
        analyser_10 = CreditRatingAnalyzer()
        analyser_10.data = ["test"]*2
        cr_analyser.credit_ratings_analyzers = {"1":analyser_1,"2":analyser_2,"4":analyser_4,"10":analyser_10}
        result = cr_analyser.get_clusters_share_of_overal_credit_ratings([cr_cluster])
        result = result[0]
        self.assertEqual(result["AAA"],0.8)
        self.assertEqual(result["AA+"],0.5)
        self.assertEqual(result["AA-"],0.3)
        self.assertEqual(result["BBB-"],0.5)
    
    def test_get_share_of_companies_in_each_clusters_gives_expected_result(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":10}
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"1":4,"2":1}
        cr_cluster3 = CreditRatingCluster(0,0)
        cr_cluster3.credit_ratings_counts = {"1":12,"2":8}
        cr_cluster4 = CreditRatingCluster(0,0)
        cr_cluster4.credit_ratings_counts = {"1":3,"2":2}
        cr_analyser = ClustersAnalyzer(None,None,None,None,None,None)
        cr_analyser.cluster_labels = ["test"]*40
        result = cr_analyser.get_share_of_companies_in_each_clusters([cr_cluster1,cr_cluster2,cr_cluster3,cr_cluster4])
        self.assertEqual(result[0],0.25)
        self.assertEqual(result[1],0.125)
        self.assertEqual(result[2],0.5)
        self.assertEqual(result[3],0.125)
    
    def test_get_measures_of_location_and_dispersion_gives_expected_result_no_cr_cluster(self):
        cr_analyser = ClustersAnalyzer(None,None,None,None,None,None)
        cr_analyser.cluster_labels = ["test"]*40
        result = cr_analyser.get_share_of_companies_in_each_clusters([])
        self.assertEqual(result[0]["SUM"],0)

    def test_get_measures_of_location_and_dispersion_gives_expected_results_many_cr_in_2_clusters(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        cr_cluster1.companies_count = 10
        cr_cluster1_expectations = cr_cluster1.get_measures_of_location_and_dispersion_for_credit_ratings_values()
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":1,"13":1,"14":3}
        cr_cluster2.companies_count = 5
        cr_cluster2_expectations = cr_cluster2.get_measures_of_location_and_dispersion_for_credit_ratings_values()
        result = ClustersAnalyzer(None,None,None,None,None,None).get_measures_of_location_and_dispersion([cr_cluster1,cr_cluster2])
        self.assertEqual(cr_cluster1_expectations["Mean"],result[0]["Mean"])
        self.assertEqual(cr_cluster2_expectations["Median"],result[1]["Median"])
    
    def test_get_measures_of_location_and_dispersion_gives_expected_results_no_cr_cluster(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).get_measures_of_location_and_dispersion([])
        self.assertEqual(len(result),0)
    
    def test_get_cluster_ranges_gives_expected_results_no_cr_cluster(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).get_cluster_ranges([])
        self.assertEqual(len(result),0)
    
    def test_get_cluster_ranges_gives_expected_results_many_cr_in_2_clusters(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":4,"2":2,"4":3,"10":1}
        cr_cluster1.companies_count = 10
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":1,"13":1,"14":3}
        cr_cluster2.companies_count = 5
        result = ClustersAnalyzer(None,None,None,None,None,None).get_cluster_ranges([cr_cluster1,cr_cluster2])
        self.assertEqual(result[0],9)
        self.assertEqual(result[1],2)

    def test_compare_cluster_and_credit_rating_values_gives_expected_result_scenar_1(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).compare_cluster_and_credit_rating_values({"3rd Quartile":10,"Median":8,"1st Quartile":6},{"Mean":10})
        self.assertTrue("highest 75%" in result)

    def test_compare_cluster_and_credit_rating_values_gives_expected_result_scenar_2(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).compare_cluster_and_credit_rating_values({"3rd Quartile":10,"Median":8,"1st Quartile":6},{"Mean":5})
        self.assertTrue("lowest 25%" in result)

    def test_compare_cluster_and_credit_rating_values_gives_expected_result_scenar_3(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).compare_cluster_and_credit_rating_values({"3rd Quartile":10,"Median":8,"1st Quartile":6},{"Mean":8})
        self.assertTrue("median" in result)

    def test_compare_cluster_and_credit_rating_values_gives_expected_result_scenar_4(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).compare_cluster_and_credit_rating_values({"3rd Quartile":10,"Median":8,"1st Quartile":6},{"Mean":9})
        self.assertTrue("upper half" in result)

    def test_compare_cluster_and_credit_rating_values_gives_expected_result_scenar_5(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).compare_cluster_and_credit_rating_values({"3rd Quartile":10,"Median":8,"1st Quartile":6},{"Mean":7})
        self.assertTrue("lower half" in result)

    def test_get_col_name_no_col_name_fails_graciously(self):
        result = ClustersAnalyzer(None,None,None,None,None,None).get_col_name(0)
        self.assertEqual(result, "")

    def test_get_col_name_gives_expected_result(self):
        result = ClustersAnalyzer([],"",None,None,None,None,None,["Col 1","Col 2"]).get_col_name(1)
        self.assertEqual(result,"Col 2")

    def test_get_col_name_gives_index_out_of_bounds(self):
        try:
            res = ClustersAnalyzer([],"",None,None,None,None,None,["Col 1","Col 2"]).get_col_name(2)
            self.assertTrue(False)
        except IndexError:
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

    def test_compute_weigthed_avg_entropy_gives_expected_results_many_cr_in_2_clusters(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":1,"2":1,"4":1,"10":1}
        cr_cluster1.companies_count = 4
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":2,"13":1,"14":3}
        cr_cluster2.companies_count = 6
        expected_result = cr_cluster1.get_entropy()*0.4+cr_cluster2.get_entropy()*0.6
        result = ClustersAnalyzer([],"",data=["test"]*10).compute_weigthed_avg_entropy([cr_cluster1,cr_cluster2])
        self.assertEqual(result,expected_result)
    
    def test_get_clusters_entropies_gives_expected_results_many_cr_in_2_clusters(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":1,"2":1,"4":1,"10":1}
        cr_cluster1.companies_count = 4
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":2,"13":1,"14":3}
        cr_cluster2.companies_count = 6
        expected_result = [cr_cluster1.get_entropy(),cr_cluster2.get_entropy()]
        result = ClustersAnalyzer([],"",data=["test"]*10).get_clusters_entropies([cr_cluster1,cr_cluster2])
        self.assertEqual(result,expected_result)

    def test_get_clusters_with_various_cr_ranges_gives_expected_results_many_cr_in_2_clusters_scenar_1(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":1,"2":1,"4":1,"10":1}
        cr_cluster1.companies_count = 4
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":2,"13":1,"14":3}
        cr_cluster2.companies_count = 6
        result = ClustersAnalyzer([],"").get_clusters_with_various_cr_ranges([cr_cluster1,cr_cluster2])
        self.assertEqual(len(result),1)
    
    def test_get_clusters_with_various_cr_ranges_gives_expected_results_many_cr_in_2_clusters_scenar_2(self):
        cr_cluster1 = CreditRatingCluster(0,0)
        cr_cluster1.credit_ratings_counts = {"1":1,"2":1,"4":1,"10":1}
        cr_cluster1.companies_count = 4
        cr_cluster2 = CreditRatingCluster(0,0)
        cr_cluster2.credit_ratings_counts = {"12":2,"13":1,"18":3}
        cr_cluster2.companies_count = 6
        result = ClustersAnalyzer([],"").get_clusters_with_various_cr_ranges([cr_cluster1,cr_cluster2])
        self.assertEqual(len(result),2)
    
    def test_create_credit_rating_clusters_scenario_1(self):
        cr_analyser = ClustersAnalyzer([],"")
        cr_analyser.data = [["data "+str(i)] for i in range(10)]
        cr_analyser.row_credit_ratings = ["1","2","4","1","2","3","2","4","3","2"]
        cr_analyser.cluster_labels = [0,0,1,0,1,2,2,2,1,0]
        result = cr_analyser.create_credit_rating_clusters()
        self.assertEqual(result[0].get_companies_count(),4)
        self.assertEqual(result[1].get_companies_count(),3)
        self.assertEqual(result[2].get_companies_count(),3)
        # CR correctly stored
        self.assertEqual(result[0].credit_ratings_counts["1"],2)
        self.assertEqual(result[0].credit_ratings_counts["2"],2)
        self.assertTrue("3" not in result[0].credit_ratings_counts.keys())
        self.assertTrue("4" not in result[0].credit_ratings_counts.keys())
        self.assertTrue("1" not in result[1].credit_ratings_counts.keys())
        self.assertEqual(result[1].credit_ratings_counts["2"],1)
        self.assertEqual(result[1].credit_ratings_counts["3"],1)
        self.assertEqual(result[1].credit_ratings_counts["4"],1)
        self.assertTrue("1" not in result[2].credit_ratings_counts.keys())
        self.assertEqual(result[2].credit_ratings_counts["2"],1)
        self.assertEqual(result[2].credit_ratings_counts["3"],1)
        self.assertEqual(result[2].credit_ratings_counts["4"],1)
        # Data correctly stored
        self.assertEqual(result[0].data["1"],[["data 0"],["data 3"]])
        self.assertEqual(result[0].data["2"],[["data 1"],["data 9"]])
        self.assertTrue("3" not in result[0].credit_ratings_counts.keys())
        self.assertTrue("4" not in result[0].credit_ratings_counts.keys())
        self.assertEqual(result[1].data["2"],[["data 4"]])
        self.assertEqual(result[1].data["3"],[["data 8"]])
        self.assertEqual(result[1].data["4"],[["data 2"]])
        self.assertTrue("1" not in result[1].credit_ratings_counts.keys())
        self.assertEqual(result[2].data["2"],[["data 6"]])
        self.assertEqual(result[2].data["3"],[["data 5"]])
        self.assertEqual(result[2].data["4"],[["data 7"]])
        self.assertTrue("1" not in result[2].credit_ratings_counts.keys())


    #  TO DO - Clean
    # def explain_incoherences(self, credit_rating_clusters):
    #     clusters_with_notable_ranges = set(self.get_clusters_with_various_cr_ranges(credit_rating_clusters))
    #     significant_clusters = set(self.get_singificant_clusters(credit_rating_clusters))
    #     clusters_requiring_explanations = clusters_with_notable_ranges.union(significant_clusters)
    #     unique_clusters_requiring_explanations = list(set(clusters_requiring_explanations))
    #     explanations = {}
    #     for cluster_idx in range(len(unique_clusters_requiring_explanations)):
    #         credit_ratings_held_in_significant_proportion = unique_clusters_requiring_explanations[cluster_idx].get_credit_ratings_held_in_significant_proportions(self.PROPORTION_OF_RATING_IN_CLUSTER_CONSIDERED_SIGNIFICANT)
    #         cluster_explanations = {}
    #         for rating in credit_ratings_held_in_significant_proportion:
    #             analyzer = self.credit_ratings_analyzers[rating] if rating in self.credit_ratings_analyzers.keys() else None
    #             if analyzer:
    #                 important_columns = analyzer.get_top_X_most_important_columns(self.NUMBER_OF_COLUMNS_WE_WANT_EXPLAINED,self.data)
    #                 for col_idx in important_columns:
    #                     cr_col_values = analyzer.get_measures_of_location_and_dispersion(col_idx)
    #                     cluster_members_col_values = unique_clusters_requiring_explanations[cluster_idx].get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(col_idx, rating)
    #                     comparison = self.compare_cluster_and_credit_rating_values(cr_col_values,cluster_members_col_values)
    #                     if not (("RATING " +rating) in cluster_explanations.keys()):
    #                         cluster_explanations[("RATING " +rating)] = [{self.get_col_name(col_idx) if self.col_names else col_idx:{"Comparison":comparison,"Credit Rating Statistics":cr_col_values,"Cluster Statistics":cluster_members_col_values}}]
    #                     else:
    #                         initial_value = cluster_explanations[("RATING " +rating)]
    #                         initial_value.append({self.get_col_name(col_idx) if self.col_names else col_idx:{"Comparison":comparison,"Credit Rating Statistics":cr_col_values,"Cluster Statistics":cluster_members_col_values}})
    #                         cluster_explanations[("RATING " +rating)] = initial_value
    #         explanations["CLUSTER "+str(cluster_idx)] =  cluster_explanations
    #     return explanations 
           

