import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

def plot(x,y,p,dir_p="./",TS = None):
    MSG = []
    MSG.append("Plot: Print Requested!")
    xlist = np.linspace(0,x, x)
    ylist = np.linspace(0, y, y)
    X, Y = np.meshgrid(xlist, ylist)
    Z = p
    fig,ax=plt.subplots(1,1)
    lim = np.amax(p)
    v = np.linspace(-lim, lim, 100, endpoint=True)
    cp = ax.contourf(X, Y, Z,v,vmax = lim,vmin = -lim,cmap='seismic')
    fig.colorbar(cp)
    ax.set_title('Electric Potential')
    plt.gca().invert_yaxis()
    if not TS:
        a = time.asctime().split(" ")
        TS = a[3]+" "+a[1]+" "+a[5]+" "+a[4]
    MSG.append("Plot: Image Generated!")
    plt.savefig(dir_p+'/Plot '+TS+'.png')
    MSG.append("Plot: Image Saved!")
    return "\n".join(MSG)