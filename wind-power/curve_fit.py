import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

df = pd.read_csv('wind_data.csv')
df['ps'] = df['p'].shift(-1)
df = df.dropna()

df = df[df['Ws1'] <= 20]  

obs = df[['ps']].to_numpy().flatten()

data = df[['Ws1', 'Wd1']].to_numpy()

# Our function to fit is going to be a sum of two-dimensional Gaussians
def func(S,D,a,b,c,d,q,w):
    return a*S**3 + b*S**2 + c*S + d + S*q*np.cos(D/360 * 2 * np.pi + np.pi*w)

#q/(1+np.exp(-S)) + c*(a*S**2 + b*S) + d # + S*(c*D**2 + d*D) + q

# This is the callable that is passed to curve_fit. M is a (2,N) array
# where N is the total number of data points in Z, which will be ravelled
# to one dimension.
def _func(M, *args):
    S,D = M.T[0], M.T[1]
    arr = func(S, D, *args)
    return arr

# Flatten the initial guess parameter list.
p0 = np.random.randn(6)

popt, pcov = curve_fit(_func, data, obs, p0)

print(p0)
print(popt)

S = np.linspace(0,20,360)
D = np.linspace(0,359,360)

X,Y = np.meshgrid(S,D)

Z = func(X,Y,*popt)

nmse = np.mean((obs - func(data[:,0],data[:,1],*popt))**2) / np.mean((obs)**2)
print('RMS residual =', nmse)

idx = np.random.permutation(len(obs))[:1000]

# Plot the 3D figure of the fitted function and the residuals.

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, cmap='plasma')
ax.plot3D(data[idx,0],data[idx,1], obs[idx],'o')
ax.set_xlabel('Wind speed (m/s)')
ax.set_ylabel('Wind direction (degrees)')
ax.set_zlabel('Wind power generated (kW)')
plt.show()

"""
# Plot the test data as a 2D image and the fit as overlaid contours.
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(Z, origin='bottom', cmap='plasma',
          extent=(x.min(), x.max(), y.min(), y.max()))
ax.contour(X, Y, fit, colors='w')
plt.show()
"""
