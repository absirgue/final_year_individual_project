import math
class VectorCalculations:

    def get_magnitude(self, vector):
        value = 0
        for dimension_value in vector:
            value += dimension_value ** 2
        return math.sqrt(value)

    def get_square(self, vector):
        return self.get_magnitude(vector) ** 2
    
    def get_squared_euclidian_distance(self, vector1, vector2):
        if not len(vector1) == len(vector2):
            return None
        total = 0
        for i in range(len(vector1)):
            total += (vector1[i]-vector2[i])**2
        return total