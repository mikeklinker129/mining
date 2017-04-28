# import numpy as np
# import matplotlib.pyplot as plt

# plt.rcParams['figure.figsize'] = (10, 8)

# # intial parameters
# n_iter = 50
# sz = (n_iter,) # size of array
# x = -0.3 # truth value (typo in example at top of p. 13 calls this z)
# t = np.arange(0,n_iter)
# z = np.sin(t/10.0) + np.random.normal(x,0.01,size=sz) # observations (normal about x, sigma=0.1)



# Q = 1e-5 # process variance

# # allocate space for arrays
# xhat=np.zeros(sz)      # a posteri estimate of x
# P=np.zeros(sz)         # a posteri error estimate
# xhatminus=np.zeros(sz) # a priori estimate of x
# Pminus=np.zeros(sz)    # a priori error estimate
# K=np.zeros(sz)         # gain or blending factor

# R = 0.1**2 # estimate of measurement variance, change to see effect

# # intial guesses
# xhat[0] = 0.0
# P[0] = 1.0

# for k in range(1,n_iter):
#     # time update
#     xhatminus[k] = xhat[k-1]
#     Pminus[k] = P[k-1]+Q

#     # measurement update
#     if k>5:
#         R = np.cov(z[0:k])

#     K[k] = Pminus[k]/( Pminus[k]+R )
#     xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
#     P[k] = (1-K[k])*Pminus[k]

# plt.figure()
# plt.plot(z,'k+',label='noisy measurements')
# plt.plot(xhat,'b-',label='a posteri estimate')
# plt.axhline(x,color='g',label='truth value')
# plt.legend()
# plt.title('Estimate vs. iteration step', fontweight='bold')
# plt.xlabel('Iteration')
# plt.ylabel('Voltage')

# plt.figure()
# valid_iter = range(1,n_iter) # Pminus not valid at step 0
# plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
# plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
# plt.xlabel('Iteration')
# plt.ylabel('$(Voltage)^2$')
# plt.setp(plt.gca(),'ylim',[0,.01])
# plt.show()





















#Kalman Filter

import numpy as np
import datetime
import matplotlib.pyplot as plt

n = 500
t = np.array(range(0,n))
meas = np.sin(t/50.0) + np.random.randn(n)/5.0




x_t=[]

r = np.cov(np.random.randn(n)/5)
q = .0001
p = 1
x =0


for i in range(0,n):

    x = np.sin(i/40.0)
    p = p + q

    k = p / (p+r)
    x = x + k * (meas[i] - x)
    p = (1-k)*p

    x_t.append(x) 



plt.plot(t,meas)
plt.plot(t,x_t)
plt.show()















    # def ekf(self):

    #     #predict
    #     x_k = f(x_km1) # predicted state given my last state
    #     P_k = F_km1 * P_km1 * F_km1 + Q_km1

    #     #update
    #     y_k = #measurement - predicted measurement
    #     S_k = H*P_k*H + R 
    #     K_k = P_k * H / S_k

    #     x = x_k + K_k * y_k
    #     P = (1-K_k*H) * P_k
 


# KF
# x = x
# p = p + q;
# k = p / (p + r);
# x = x + k * (measurement – x);
# p = (1 – k) * p;

# Where:
# q = process noise covariance
# r = measurement noise covariance
# x = value of interest
# p = estimation error covariance
# k = Kalman gain
