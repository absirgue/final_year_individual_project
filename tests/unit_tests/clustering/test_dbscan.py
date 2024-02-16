import unittest
import pandas as pd
from clustering.dbscan import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import  DBSCAN as SKLearnDBSCAN

class TestDBScan(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        centers = [[1, 1], [-1, -1], [1, -1],[0.5,0.2],[-0.1,1]]
        self.data, labels_true = make_blobs(
            n_samples=1000, centers=centers, cluster_std=0.4, random_state=0
        )
        self.data = StandardScaler().fit_transform(self.data)
        super().__init__(methodName)
    
    def test_dbscan_gives_as_expected_result_in_config_1(self):
        db = SKLearnDBSCAN(eps=0.3, min_samples=10).fit(self.data)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        db = DBSCAN(self.data,eps=0.3, Minpts=10)
        self.assertEqual(db.cluster(), n_clusters_)
    
    def test_dbscan_gives_as_expected_result_in_config_2(self):
        db = SKLearnDBSCAN(eps=0.6, min_samples=15).fit(self.data)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        db = DBSCAN(self.data,eps=0.6, Minpts=15)
        self.assertEqual(db.cluster(), n_clusters_)
    
    def test_dbscan_gives_as_expected_result_in_default_config(self):
        db = SKLearnDBSCAN(eps=0.5, min_samples=5).fit(self.data)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        db = DBSCAN(self.data)
        self.assertEqual(db.cluster(), n_clusters_)