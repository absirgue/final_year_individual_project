from clustering.vector_calculations import VectorCalculations
import math 

class Cluster:
    """
    Element of our reference implementation of OCIL for experimentation purposes.
    We will not study this algorithm further.
    """
    
    def __init__(self,categorical_attributes_count):
        self.categorical_attributes_frequency = {}
        self.intialize_categorical_attributes_frequency(categorical_attributes_count)
        self.numerical_values_centroid = []
        self.points_count = 0
    
    def add_point(self,categorical_attributes,numerical_attributes):
        for attribute_idx,value in enumerate(categorical_attributes):
            self.add_categorical_attributes_frequency(attribute_idx,value)
        self.add_numerical_values_to_centroid(numerical_attributes)
        self.points_count += 1
    
    def remove_point(self,categorical_attributes, numerical_attributes):
        for attribute_idx,value in enumerate(categorical_attributes):
            self.remove_categorical_attributes_frequency(attribute_idx,value)
        self.remove_numerical_values_to_centroid(numerical_attributes)
        self.points_count -= 1
    
    def remove_categorical_attributes_frequency(self,attribute, value):
        if attribute in self.categorical_attributes_frequency and value in self.categorical_attributes_frequency[attribute]:
                self.categorical_attributes_frequency[attribute][value] -= 1
        else:
            raise ValueError()
    
    def add_categorical_attributes_frequency(self,attribute, value):
        if attribute in self.categorical_attributes_frequency:
            if value in self.categorical_attributes_frequency[attribute]:
                self.categorical_attributes_frequency[attribute][value] += 1
            else:
                self.categorical_attributes_frequency[attribute][value] = 1
        else:
            raise ValueError()
    
    def add_numerical_values_to_centroid(self, numerical_values):
        if len(self.numerical_values_centroid) > 0:
            for i in range(len(self.numerical_values_centroid)):
                sum = self.numerical_values_centroid[i] * self.points_count
                sum += numerical_values[i]
                self.numerical_values_centroid[i] = sum/(self.points_count+1)
        else:
             self.numerical_values_centroid = numerical_values
    
    def remove_numerical_values_to_centroid(self, numerical_values):
        for i in range(len(self.numerical_values_centroid)):
            sum = self.numerical_values_centroid[i] * self.points_count
            sum -= numerical_values[i]
            if self.points_count>1:
                self.numerical_values_centroid[i] = sum/(self.points_count-1)
            else:
                self.numerical_values_centroid[i] = 0

    
    def intialize_categorical_attributes_frequency(self,categorical_attributes_count):
        for attribute_idx in range(categorical_attributes_count):
            self.categorical_attributes_frequency[attribute_idx] = {}

    def get_exp_difference_for_numerical_attributes(self,attributes):
        return math.exp(-0.5* VectorCalculations().get_squared_euclidian_distance(attributes,self.numerical_values_centroid))
        
    def get_similarity_for_categorical_attribute(self,attribute,value):
        count_non_null_values = self.get_count_non_null_categorical_values(attribute)
        if count_non_null_values > 0:
            return self.get_count_of_given_value_for_attribute(attribute,value)/self.get_count_non_null_categorical_values(attribute)
        else:
            return 0
        
    def get_count_non_null_categorical_values(self,attribute):
        total = 0
        if attribute in self.categorical_attributes_frequency:
            for value in self.categorical_attributes_frequency[attribute]:
                if self.is_not_null(value):
                    total += self.categorical_attributes_frequency[attribute][value]
        return total

    def get_count_of_given_value_for_attribute(self,attribute, value):
        if (attribute in self.categorical_attributes_frequency) and (value in self.categorical_attributes_frequency[attribute]):
            return self.categorical_attributes_frequency[attribute][value]
        return 0

    def is_not_null(self, value):
        return value and value != "" and value != "na" and value != "None" and value != "null"