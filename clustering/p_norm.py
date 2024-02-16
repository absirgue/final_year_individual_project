import numpy as np

class PNorm:

    def __init__(self,p):
        if p < 1:
            raise ValueError("P has to be at least 1")
        self.p = p 
    
    def calculate_norm(self,x1,x2):
        x1 = np.array(x1)
        x2 = np.array(x2)
        return np.linalg.norm(x1 - x2, ord=self.p)
