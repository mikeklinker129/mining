import numpy as np
import matplotlib.pyplot as plt

def autocorrelation (x) :
    """
    Compute the autocorrelation of the signal, based on the properties of the
    power spectral density of the signal.
    """
    xp = x-np.mean(x)
    f = np.fft.fft(xp)
    p = np.array([np.real(v)**2+np.imag(v)**2 for v in f])
    pi = np.fft.ifft(p)
    return np.real(pi)[:x.size/2]/np.sum(xp**2)


# generate some data
x = np.arange(0.,2*3.14,0.01)

y = np.sin(x)
y = np.random.uniform(size=len(x))+np.sin(x)
yunbiased = y-np.mean(y)
ynorm = np.sum(yunbiased**2)
acor = np.correlate(yunbiased, yunbiased, "same")/ynorm
# use only second halfB
acor = acor[len(acor)/2:]

plt.figure(0)
plt.plot(x,y)
plt.plot(x,yunbiased)

plt.figure(1)
plt.plot(acor,linewidth=4)
plt.show()