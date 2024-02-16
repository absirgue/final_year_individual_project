import numpy as np

def create_floats_list(start,end,step):
    return np.arange(start, end + step, step).tolist()

def create_ints_list(start,end,step):
    return list(range(start,end+step,step))