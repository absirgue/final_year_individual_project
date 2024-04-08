import numpy as np

# Returns a list of all floats separated by a given step size between a given start and end number.
def create_floats_list(start,end,step):
    return np.arange(start, end + step, step).tolist()

# Returns a list of all ints separated by a given step size between a given start and end number.
def create_ints_list(start,end,step):
    return list(range(start,end+step,step))