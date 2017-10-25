# -*- coding: utf-8 -*-
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

def robust_var(x, ratio=0.05, ddof=0):
    mean_x = x.mean()
    dev_x_sq = (x-mean_x) ** 2
    dev_x_sq = np.sort(dev_x_sq)
    
    N = len(dev_x_sq)
    return np.mean(dev_x_sq[int(N*ratio):int(N*(1-ratio))]) * N / (N-ddof)

def robust_mean(x, ratio=0.05):
    sorted_x = np.sort(x)
    N = len(sorted_x)
    return np.mean(sorted_x[int(N*ratio):int(N*(1-ratio))])

def one_dim_kalman_filter(z_seq, measure_std_seq, proc_std, 
                          dim_x=3, x0=None, P0=None, dt=1):
    # NOTE: we do not specify velocity and acceleration in predict function, 
    # since the filter will track it
    assert dim_x == 2 or dim_x == 3
    kf = KalmanFilter(dim_x=dim_x, dim_z=1)    
    if dim_x == 2:
        # x is the state vector
        if x0 is None:
            kf.x = np.array([z_seq[0], 0])
        else:
            assert x0.shape[0] == dim_x
            kf.x = x0
        # P is the covariance matrix of state
        if P0 is None:
            kf.P = np.array([[1, 0],
                             [0, 1]])
        else:
            assert P0.shape[0] == dim_x and P0.shape[1] == dim_x
            kf.P = P0
        # F is the state transmition function
        kf.F = np.array([[1, dt],
                         [0,  1]])
        # H is the measurement function
        kf.H = np.array([[1, 0]])
    else:
        if x0 is None:
            kf.x = np.array([z_seq[0], 0, 0])
        else:
            assert x0.shape[0] == dim_x
            kf.x = x0
        if P0 is None:
            kf.P = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])
        else:
            assert P0.shape[0] == dim_x and P0.shape[1] == dim_x
            kf.P = P0
        kf.F = np.array([[1, dt, 0.5*dt**2],
                         [0,  1,        dt],
                         [0,  0,         1]])
        kf.H = np.array([[1, 0, 0]])
    
    # Q is the covariance matrix of process noise    
    kf.Q = Q_discrete_white_noise(dim=dim_x, dt=dt, var=proc_std**2)
    
    # TODO: change the scale of R??
    std_scale = 1
    R_seq = (measure_std_seq * std_scale) ** 2    
    
    x_seq, cov_seq = [kf.x], [kf.P]
    # z is the measurement vector
    # R is the covariance matrix of measurement noise
    for z, R in zip(z_seq[1:], R_seq[1:]):
        kf.predict()
        kf.update(z, R=np.array([[R]]))
        x_seq.append(kf.x)
        cov_seq.append(kf.P)
    x_seq, cov_seq = np.array(x_seq), np.array(cov_seq)
    
    return x_seq[:, 0]
    
    
    