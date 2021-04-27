#for fitting specially
import matplotlib.pylab as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from scipy.optimize import curve_fit


if __name__ == "__main__":
    # initialization value a, t, b
    def func(x, a, t, b):
        return a * (np.exp(-x / t)) + b

    x1 = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    x2 = x1

    # FND-H + ferredoxin
    y1 = [6208, 3405, 1342, 483, 461, 416, 392, 400, 407, 419, 423]
    y2 = [6209, 2403, 832, 390, 435, 462, 519, 339, 468, 477, 423]

    #crystal+ferredoxin
    # y1 = [8360, 5843, 3205, 1202, 526, 428, 464, 767, 480, 454, 456]  #crystal
    # y2 = [8442, 3205, 1044, 435, 497, 534, 612, 365, 542, 555, 481]   #crystal+protein

    p0 = [10, 10, -20]
    iter=50000
    title = 'T1 Relaxation'
    # color=['black', 'black', 'red', 'green']  # 'Default blue'
    # legend1 = ['FND-H', 'fit', 'FND-H+ferredoxin', 'fit']

    font = FontProperties()
    font.set_family('serif')
    font.set_name('Arial')
    # font.set_style('italic')
    fig, ax = plt.subplots()

    ##line1
    popt, pcov = curve_fit(func, x1, y1, p0, maxfev=iter)
    print('T1 is: ', popt[1])
    ax.plot(x1, y1, 'o', linewidth=1, label = 'FND-H', color='#1f77b4')
    x0 = np.linspace(x1[0], x1[-1], 50)
    ax.plot(x0, func(x0, *popt), '--', linewidth=1, label = 'fit')

    ## line2
    popt, pcov = curve_fit(func, x2, y2, p0, maxfev=iter)
    print('T1 is: ', popt[1])
    ax.plot(x2, y2, 'o', linewidth=1, label = 'FND-H + ferredoxin', color='orange')
    x0 = np.linspace(x2[0], x2[-1], 50)
    ax.plot(x0, func(x0, *popt), '--', linewidth=1, label = 'fit', color='orange')

    ax.legend(prop=font)
    lx = 'Time between laser pulses, µs'
    ly = 'Scaled Fluorescence Counts, AU'
    ax.set_xlabel(lx, fontname="Arial", fontsize=14)
    ax.set_ylabel(ly, fontname="Arial", fontsize=14)

    for tick in ax.get_xticklabels():
        tick.set_fontname("Arial")
    for tick in ax.get_yticklabels():
        tick.set_fontname("Arial")

    plt.show()

# symbols
# color=['#1f77b4', 'orange', 'red', 'green']  # 'Default blue'
# 'k--'
# 'k-.'
# 'ko', mfc='none'
