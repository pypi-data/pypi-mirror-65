'''Efficiently find all unique n-dimensional binary sampling patterns.
'''

import numpy as np

def unique_patterns(data, kernel_size):
    '''Find all unique sampling patterns,

    Parameters
    ----------
    data : array_like
        Complex n-dimensional k-space data.
    kernel_size : tuple
        Size of n-dimensional kernel.
    '''

    kernel_els = 2^0 2^1 2^2 ... 2^{prod(kernel_size)-1}
    indices = ii
    

    
    # There are prod(dims) number of patch locations. We will assign
    # each location a number in C order
    orig_flag = data.flags.writable
    data.flags.writable = False


    # Set the flags back to the way they were when data came in
    data.flags.writable = orig_flag

if __name__ == '__main__':
    pass
