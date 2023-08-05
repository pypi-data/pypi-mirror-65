import numpy as np
from scipy.sparse import csc_matrix

from pyHiGHS import highs_wrapper
from pyHiGHS import (
    HIGHS_CONST_INF,
    HIGHS_CONST_TINY,
)

if __name__ == '__main__':

    #c = np.array([-3, -2]).astype('double')
    #A = csc_matrix(np.array([[2, 1], [1, 1], [1, 0]])).astype('double')
    #rhs = np.array([10, 8, 4]).astype('double')
    #lhs= np.array([-HIGHS_CONST_INF]*3).astype('double')
    #lb= np.array([0, 0]).astype('double')
    #ub= np.array([HIGHS_CONST_INF]*2).astype('double')

    #c = np.array([-1, 1]).astype('double')
    #A = csc_matrix(np.array([[1, 0], [0, 1]])).astype('double')
    #lhs = np.array([-np.inf, 2]).astype('double')
    #rhs = np.array([1, 2]).astype('double')
    #lb = np.array([1, 2]).astype('double')
    #ub = np.array([1, 2]).astype('double')

    #c = np.array([-1, -2]).astype('double')
    #A = csc_matrix(np.empty((0, c.size))).astype('double')
    #lhs = np.array([]).astype('double')
    #rhs = np.array([]).astype('double')
    #lb = np.array([0, 0]).astype('double')
    #ub = np.array([np.inf, np.inf]).astype('double')

    #c = np.array([-4, 1]).astype('double')
    #A = csc_matrix(np.array([[7, -2], [0, 1], [2, -2]])).astype('double')
    #lhs = np.array([-np.inf, -np.inf, -np.inf]).astype('double')
    #rhs = np.array([14, 0, 3]).astype('double')
    #lb = np.array([2, 0]).astype('double')
    #ub = np.array([2, np.inf]).astype('double')

    #c = np.array([-1.,  1., -1.,  1.])
    #lb = np.array([  0., -np.inf,  -1.,  -1.])
    #lhs = np.array([], dtype='double')
    #rhs = np.array([], dtype='double')
    #ub = np.array([np.inf,  0.,  1.,  1.])
    #A = csc_matrix(np.empty((0, 4), dtype='double'))

    data = np.load('/home/nicholas/Documents/scipy-highs/testcase.npz')
    c = data['c']
    A = csc_matrix(data['A'])
    lb = data['lb']
    ub = data['ub']
    lhs = data['lhs']
    rhs = data['rhs']

    res = highs_wrapper(c, A, rhs, lhs, lb, ub, {'sense':1, 'presolve':True, 'solver':'simplex', 'message_level':1})
    print(res)
