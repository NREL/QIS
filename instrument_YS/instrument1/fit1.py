# https://stackoverflow.com/questions/21420792/exponential-curve-fitting-in-scipy/21421137
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

import matplotlib.pylab as plt
import numpy as np
from pylab import *
from scipy.optimize import curve_fit

#increasing curve
def fit1one(p0, x, y, iter, legend1, title, color='#1f77b4'):
    def func(x, a, t, b):
        return a * (np.exp(x / t)) + b
    #initialization value a, t, b
    # p0 = [-100, 100, 40]       ##50-800

    popt, pcov = curve_fit(func, x, y, p0, maxfev=iter)
    # print(popt)  # a,b,c, d to minimize squared residuals of f(x, *popt) - y
    # print(pcov)   #2D array, estimated covariance of popt
    print('T1 is: ', popt[1])

    plot(x, y, 'o', c=color)
    x1 = linspace(x[0], x[-1], 50)  # reuse value x1
    plot(x1, func(x1, *popt), '--', c=color)

    plt.legend([legend1, 'fit'])
    plt.xlabel('Time between laser pulses, µs')
    plt.ylabel('Fluorescence Counts, AU')
    plt.title(title)
    show()
    return popt[1]

def fit1n(p0, x, y, iter, legend1, title, color, n):
    def func(x, a, t, b):
        return a * (np.exp(x / t)) + b
        # initialization value a, t, b

    # color = ['#1f77b4', 'orange', 'red', 'green']  # 'Default blue'
    # legend1 = ['FND', 'FND-H+ferredoxin', 'FND-OH']
    lg = []
    T1v = []
    # n = 3
    for i in range(n):
        popt, pcov = curve_fit(func, x[i], y[i], p0, maxfev=iter)
        # print(popt)  # a,b,c, d to minimize squared residuals of f(x, *popt) - y
        # print(pcov)   #2D array, estimated covariance of popt
        print('T1 is: ', popt[1])
        T1v.append(round(popt[1], 3))

        plot(x[i], y[i], 'o', c=color[i])
        x1 = linspace(x[i][0], x[i][-1], 50)  # reuse value x1
        plot(x1, func(x1, *popt), '--', c=color[i])
        lg.append(legend1[i])
        lg.append('fit')

    # np.savetxt(filename+".csv", flu, delimiter=",")
    # lg = ['FND', 'fit', 'FND-H+ferredoxin', 'fit']
    plt.legend(lg)
    plt.xlabel('Time between double pulses, µs')
    plt.ylabel('Fluorescence Counts, AU')
    plt.title(title)
    show()
    return T1v



if __name__ == "__main__":

    # FND
    x1=[250, 300, 350, 400, 500, 550, 600, 650, 700]  # 2020.9.17 invert
    y1=[289, 297, 262, 264, 313, 427, 663, 1128, 1762]  #T1=77us  gate0.5
    # FND+protein
    x2=[450, 500, 550, 600, 650, 700]  #2020.9.30
    y2=[1514, 1306, 1264, 1252, 1191, 1203]  #T1=52us *****
    x2=[250, 300, 350, 400, 450, 500]  #shift x
    y2=[1749, 746, 544, 486, 192, 250]  #normalize y

    # FND-OH
    x1=[200, 250, 300, 350, 400, 500, 550, 600, 650, 700]   # 2020.9.24  450,
    y1=[178, 176, 217, 192, 215, 218, 290, 444, 905, 1429]  #0.45 gate    287, T1=71.7us  *****
    x3=x1
    y3 = y1[:][::-1]  # invert y
    # 1429 905 444 290 218 215 192 217 176 178
    # FND-OH+protein
    x2=[450, 500, 550, 600, 650, 700]  #2020.10.5
    y2 = [1029, 825, 806, 722, 778, 778] #T1=35us
    x2=[250, 300, 350, 400, 450, 500]  #shift x
    y2=[1392, 463, 377, -4.8, 250, 250]  #normalize y

    # FND-H
    x1=[250, 300, 350, 400, 450, 500, 550, 600, 650, 700]  # 2020.9.25
    y1=[151, 157, 155, 168, 183, 176, 240, 361, 620, 928]
    #y1 928 620 361 240 176 183  168 155 157 151

    # FND-H+protein
    y2=[1270, 1096, 1063, 1068, 1087, 1069]  #2020.10.5
    y2=[928, 255, 127, 147, 220, 151]
    y2=[877, 204, 76, 96, 169, 100]
    y2=[907, 234, 106, 126, 199, 130]


    x1=x1[:]
    y1=y1[:][::-1]  #invert y
    x2=x2[:]
    y2=y2[:]
    # plt.plot(x3,y3)
    # plt.show()
    # exit()

    p0 = [-100, 100, 40]       ##50-800
    iter=50000
    title = 'T1 Relaxation'
    # color = None
    # legend1 = 'FND'
    # fitone(p0, x1, y1, iter, legend1, title)

    x=[]
    x.append(x1)
    x.append(x2)
    x.append(x3)

    y=[]
    y.append(y1)
    y.append(y2)
    y.append(y3)

    color=['#1f77b4', 'orange', 'red', 'green']  # 'Default blue'
    legend1 = ['FND', 'FND-H+ferredoxin', 'FND-OH']
    lg = []

    n=3
    fit1n(p0, x, y, iter, legend1, title, color, n)
    exit()
