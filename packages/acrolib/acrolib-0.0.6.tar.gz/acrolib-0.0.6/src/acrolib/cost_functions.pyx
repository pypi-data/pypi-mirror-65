
import numpy as np
from math import sqrt

DTYPE = np.double


def norm_l1(double[:,:] D1, double[:, :] D2):
    
    cdef Py_ssize_t N1 = D1.shape[0]
    cdef Py_ssize_t N2 = D2.shape[0]
    cdef Py_ssize_t K = D2.shape[1]
        
    result = np.zeros((N1, N2), dtype=DTYPE)
    cdef double[:, :] result_view = result
    
    cdef Py_ssize_t i, j, k
    cdef double tmp
    for i in range(N1):
        for j in range(N2):
            tmp = 0
            for k in range(K):
                tmp += abs(D1[i, k] - D2[j, k])
            result_view[i, j] = tmp
    
    return result

def norm_l2(double[:,:] D1, double[:, :] D2):
    
    cdef Py_ssize_t N1 = D1.shape[0]
    cdef Py_ssize_t N2 = D2.shape[0]
    cdef Py_ssize_t K = D2.shape[1]
        
    result = np.zeros((N1, N2), dtype=DTYPE)
    cdef double[:, :] result_view = result
    
    cdef Py_ssize_t i, j, k
    cdef double tmp
    for i in range(N1):
        for j in range(N2):
            tmp = 0
            for k in range(K):
                tmp += (D1[i, k] - D2[j, k]) ** 2
            result_view[i, j] = sqrt(tmp)
    
    return result

def sum_squared(double[:,:] D1, double[:, :] D2):
    
    cdef Py_ssize_t N1 = D1.shape[0]
    cdef Py_ssize_t N2 = D2.shape[0]
    cdef Py_ssize_t K = D2.shape[1]
        
    result = np.zeros((N1, N2), dtype=DTYPE)
    cdef double[:, :] result_view = result
    
    cdef Py_ssize_t i, j, k
    cdef double tmp
    for i in range(N1):
        for j in range(N2):
            tmp = 0
            for k in range(K):
                tmp += (D1[i, k] - D2[j, k]) ** 2
            result_view[i, j] = tmp
    
    return result

def weighted_sum_squared(double[:,:] D1, double[:, :] D2, double[:] weights):
    
    cdef Py_ssize_t N1 = D1.shape[0]
    cdef Py_ssize_t N2 = D2.shape[0]
    cdef Py_ssize_t K = D2.shape[1]
        
    result = np.zeros((N1, N2), dtype=DTYPE)
    cdef double[:, :] result_view = result
    
    cdef Py_ssize_t i, j, k
    cdef double tmp
    for i in range(N1):
        for j in range(N2):
            tmp = 0
            for k in range(K):
                tmp += weights[k] * (D1[i, k] - D2[j, k]) ** 2
            result_view[i, j] = tmp
    
    return result

def norm_infinity(double[:,:] D1, double[:, :] D2):
    
    cdef Py_ssize_t N1 = D1.shape[0]
    cdef Py_ssize_t N2 = D2.shape[0]
    cdef Py_ssize_t K = D2.shape[1]
        
    result = np.zeros((N1, N2), dtype=DTYPE)
    cdef double[:, :] result_view = result
    
    cdef Py_ssize_t i, j, k
    cdef double tmp
    for i in range(N1):
        for j in range(N2):
            tmp = 0
            for k in range(K):
                if abs((D1[i, k] - D2[j, k])) > tmp:
                    tmp = abs(D1[i, k] - D2[j, k])
            result_view[i, j] = tmp
    
    return result