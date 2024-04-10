import unittest
from clustering_algorithms.vector_calculations import VectorCalculations

class TestVectorCalculations(unittest.TestCase):

    def test_magnitude_of_2d_vector_is_as_expected(self):
        self.assertEqual(VectorCalculations().get_magnitude([3,4]),5)
    
    def test_magnitude_of_5d_vector_is_as_expected(self):
        self.assertEqual(VectorCalculations().get_magnitude([3,4,-1,10,-5]),12.288205727444508)
    
    def test_square_of_2d_vector_is_as_expected(self):
        self.assertEqual(VectorCalculations().get_square([3,4]),25)

    def test_square_of_5d_vector_is_as_expected(self):
        self.assertEqual(VectorCalculations().get_square([3,4,-1,10,-5]),151)
    
    def test_squared_euclidian_dist_of_2d_vectors_is_as_expected(self):
        self.assertEqual(VectorCalculations().get_squared_euclidian_distance([3,4],[10,4]),49)

    def test_squared_euclidian_dist_of_5d_vectors_is_as_expected(self):
        self.assertEqual(VectorCalculations().get_squared_euclidian_distance([3,4,-1,2,4],[10,4,1,3,0]),70)