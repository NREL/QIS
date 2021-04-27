# all spectra analysis: read Bruker data, read csv, replot
# line width, signal-to-noise ratio, backcor(background correction)
import matplotlib.pylab as plt
import numpy as np
import os, csv
from tkinter import *
import struct
from matplotlib.font_manager import FontProperties

def LW(spectrum, sweep):
    sp = zeroline(spectrum, 0.05)
    N = len(sp)
    n = N - 1
    x = np.arange(n+1)
    xn = (x - n / 2) / n

    M = 2000
    n = M - 1
    x = np.arange(n + 1)
    xm = (x - n / 2) / n

    if M > N:
        sp = np.interp(xm, xn, sp)   #don't need zero baseline

    mx = max(sp)
    inx = sp > (mx / 2)
    N = len(sp)
    linewidth = round(1000 * sum(inx) / N * sweep)
    return linewidth


def zeroline(spectrum, extent):
    L = len(spectrum)
    edge = round(extent * L)
    if edge == 0:
        edge=1

    Sleft = sum(spectrum[0:edge]) / edge
    Sright = sum(spectrum[L - edge:L+1]) / edge
    s = len(spectrum)

    LL = np.arange(1,L+1)
    tmp = Sleft + (Sright - Sleft) / L * LL
    if len(tmp) != s:
        tmp = tmp.T
    res = spectrum - tmp
    return res


def SNRLW(start, stop, data, p1, p2, n1, n2, n3, n4):

    pts = len(data)
    x = np.linspace(start, stop, pts)

    y = np.abs(data)  # absolute value
    # peakrange = [2840, 2900]  # region includes the peak, [MHz] 6A
    # noiserange1 = [2700, 2800]  # includes noise section 1, [MHz]
    # noiserange2 = [2910, 2980]  # includes noise section 2, [MHz]

    # SNR ######
    step = abs(x[1] - x[0])
    m = np.where(abs(x - p1) < step)[0][0]   # define peak
    n = np.where(abs(x - p2) < step)[0][0]
    peak = y[m:n]

    p = np.where(abs(x - n1) < step)[0][0]  # define baseline
    q = np.where(abs(x - n2) < step)[0][0]
    noise1 = np.std(y[p:q])  # p:q or q:p if h reverses
    p = np.where(abs(x - n3) < step)[0][0]
    q = np.where(abs(x - n4) < step)[0][0]
    noise2 = np.std(y[p:q])  # p:q or q:p if h reverses
    noise = (noise1 + noise2) / 2
    peak_amp = max(peak)  # signal
    SNR = round(peak_amp / noise, 1)

    ### Calculate linewidth
    swpeak = len(peak)
    pphh = round(LW(peak, swpeak) / 1000, 2)

    return SNR, pphh


def replot(start, stop, y, title, lx, ly, lg=''):
    pts = len(y)
    x = np.linspace(start, stop, pts)
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(lx)
    plt.ylabel(ly)
    if lg:
        plt.legend([lg])
    plt.show()


def fineplot(start, stop, y, title, lx, ly, lg):
    pts = len(y)
    x = np.linspace(start, stop, pts)
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Arial')
    # font.set_style('italic')
    fig, ax = plt.subplots()

    ax.plot(x, y, 'k', linewidth=1, label=lg)
    ax.legend(prop=font)
    ax.set_xlabel(lx, fontname="Arial", fontsize=14)
    ax.set_ylabel(ly, fontname="Arial", fontsize=14)
    ax.set_title(title, fontname='Arial', fontsize=18)

    for tick in ax.get_xticklabels():
        tick.set_fontname("Arial")
    for tick in ax.get_yticklabels():
        tick.set_fontname("Arial")

    plt.show()
    exit()


def backcor(n, y, ord, s, fct):
    #Background estimation by minimizing a non-quadratic cost function; reference[1]
    # Rescaling
    N = len(n)
    i = np.argsort(n)
    n.sort()
    y = y[i]
    maxy = np.amax(y)
    dely = (maxy - np.amin(y)) / 2
    n = 2 * (n[:] - n[N - 1]) / (n[N - 1] - n[0]) + 1
    y = (y[:] - maxy) / dely + 1

    # Vandermonde matrix
    p = np.arange(ord + 1)
    T1 = np.matlib.repmat(n, ord + 1, 1)
    T2 = np.matlib.repmat(p, N, 1)
    TT = np.power(T1.T, T2)
    T3 = np.linalg.pinv(np.matmul(TT.T, TT))
    Tinv = np.matmul(T3, TT.T)

    # Initialisation (least-squares estimation)
    a = np.matmul(Tinv, y)
    z = np.matmul(TT, a)

    # Other variables
    alpha = 0.99 * 1 / 2  # Scale parameter alpha
    it = 0  # Iteration number

    # LEGEND
    while True:
        it = it + 1       # Iteration number
        zp = z            # Previous estimation
        res = y - z       # Residual

        # Estimate d
        if (fct == 'sh'):
            d = (res * (2 * alpha - 1)) * (abs(res) < s) + (-alpha * 2 * s - res) * (res <= -s) + (
                        alpha * 2 * s - res) * (res >= s)
        elif (fct == 'ah'):
            d = (res * (2 * alpha - 1)) * (res < s) + (alpha * 2 * s - res) * (res >= s)
        elif (fct == 'stq'):
            d = (res * (2 * alpha - 1)) * (abs(res) < s) - res * (abs(res) >= s)
        elif (fct == 'atq'):
            d = (res * (2 * alpha - 1)) * (res < s) - res * (res >= s)

        # Estimate z
        a = np.matmul(Tinv, y + d)
        z = np.matmul(TT, a)

        z1 = sum(np.power(z - zp, 2)) / sum(np.power(zp, 2))
        if z1 < 1e-9:
            break

    # Rescaling
    j = np.argsort(i)
    z = (z[j] - 1) * dely + maxy
    a[0] = a[0] - 1
    a = a * dely  # + maxy
    return z


class mclass:   #for backcor function
    def __init__(self,window):
        self.window = window

        self.l1 = Label(window, text="Background Correction      ", font=("Helvitca", 14))
        self.l2 = Label(window, text="Order     ")
        self.l3 = Label(window, text="Threshold      ")
        self.l4 = Label(window, text="Function      ")
        self.l5 = Label(window, text=" ")

        self.l1.grid(row=1, column=1, sticky=W, columnspan=5)
        self.l2.grid(row=2, column=1, sticky=E)
        self.l3.grid(row=3, column=1, sticky=E)
        self.l4.grid(row=4, column=1, sticky=E)
        self.l5.grid(row=5, column=1, sticky=E)

        self.e2 = Entry(window)
        self.e2.insert(0, 0.01)
        self.e2.grid(row=3, column=2, sticky=W)

        self.v1 = StringVar(window)
        self.v1.set("6")
        self.w1 = OptionMenu(window, self.v1, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.w1.grid(row=2, column=2, sticky=W)

        self.v3 = StringVar(window)
        self.v3.set("ah")
        self.w = OptionMenu(window, self.v3, "sh", "ah", "stq", "atq")
        self.w.grid(row=4, column=2, sticky=W)

        self.b1 = Button(window, text='  Select and Plot  ', command=self.plotbg)
        self.b1.grid(row=6, column=1, sticky=E)
        # self.b2 = Button(window, text='  OK  ', command=window.destroy)  #possible close button
        # self.b2.grid(row=6, column=2, sticky=E)
        self.l6 = Label(window, text="When done, close window \nand background plot to proceed. ")
        self.l6.grid(row=7, column=1, sticky=W, columnspan=2)

    def plotbg(self):
        plt.clf()
        ord = int(self.v1.get())
        s = float(self.e2.get())
        fct = self.v3.get()
        reader = csv.reader(open('temp/xdata.csv', "r"), delimiter=",")
        x = list(reader)
        h1 = np.array(x).astype("float")
        h = h1[:, 0]
        reader = csv.reader(open('temp/ydata.csv', "r"), delimiter=",")
        x = list(reader)
        AB1 = np.array(x).astype("float")
        AB = AB1[:,0]
        print(type(h))
        print(h[0])
        print(AB)
        print(AB[0])

        BG = backcor(h, AB, ord, s, fct)
        np.savetxt("temp/ybackcor.csv", AB-BG, delimiter=",")

        plt.plot(h, AB, h,BG)
        plt.gca().legend(('Orginal', 'Background'))
        plt.title('Background Corrected Plot ')
        # plt.clf()
        plt.show()
        plt.close()    #must have this so this plot will close


def bcremove(y, start, stop, bca='', bcb='', bcc=''):
    pts = len(y)
    x = np.linspace(start, stop, pts)

    if bca and bcb and bcc:
        print('given parameters')
        x1 = np.array(x)
        y1 = np.array(y)
        bg = backcor(x1, y1, bca, bcb, bcc)
        AB = y-bg

    else:
        np.savetxt("temp/xdata.csv", x, delimiter=",")
        np.savetxt("temp/ydata.csv", y, delimiter=",")
        window = Tk()
        window.title("backcor")
        window.geometry("300x250+900+200")
        start = mclass(window)
        window.mainloop()

        reader = csv.reader(open('temp/ybackcor.csv', "r"), delimiter=",")
        x = list(reader)
        AB1 = np.array(x).astype("float")
        AB = AB1[:, 0]
        print("background corrected spectrum is saved as temp/ybackcor.csv")
    return AB


def Bruker(folder, fn):  #read bruker format DTA, DSC data
    if folder:
        fn = folder + '/' + filename

    # check if files exist
    if os.path.isfile(fn + '.DTA') and os.path.isfile(fn + '.DSC'):
        print('Bruker file ' + fn)
    elif os.path.isfile(fn + '.DTA') and (os.path.isfile(fn + '.DSC') == 0):
        print('Bruke data file \'DTA\' is present, but the parameter file \'DSC\' is missing.')
    else:
        print('Bruker file does not exit!')
        exit()

    Bruker = []
    fin = open(fn + '.DTA', 'rb')
    with open(fn + '.DTA', 'rb') as inh:
        indata = inh.read()
    for i in range(0, len(indata), 8):
        pos = struct.unpack('>d', indata[i:i + 8])
        Bruker.append(pos[0]);
    fin.close()
    return Bruker


def readcsv1(fn):  #read csv format
    reader = csv.reader(open(fn + '.csv', "r"), delimiter=",")
    x = list(reader)
    data = np.array(x).astype(float)
    return data


def readcsv(folder, filename):  #read csv format
    if folder:
        filename = folder + '/' + filename
    data = np.genfromtxt(filename + '.csv', delimiter=',')
    return data


if __name__ == "__main__":
    # folder = 'C:/Users/ODMR/Desktop/Instrument-YS/'
    folder = '/Users/yshi2/Documents/2021.2.18goldring/'
    # folder = '/Users/yshi2/Desktop/UI/instrument1/'
    folder = 'testdata'
    # filename = 'ys21031901'  #csv
    filename = 'ys20071612'    #bruker

    #earlier replot version
    early = 0
    if early:
        f1 = np.genfromtxt(folder + '/' + filename + '.csv', delimiter=',')
        # plt.plot(f1)
        # plt.show()
        # exit()

        # n = 0
        # flu = []
        # a = 500
        # ch2 = 1
        # point = 300
        # for i in range (point):
        #     d = np.mean(f1[n:n+a])
        #     n = n + a
        #     flu.append(d)
        #
        # if ch2:
        #     for i in range(point):
        #         d = np.mean(f1[n:n + a])
        #         n = n + a
        #         flu[i] = -(flu[i] ** 2 + d ** 2) ** 0.5


        # x = [0] * 300
        # y = [0] * 300
        # flu = [0] * 300
        # for i in range(300):
        #     x[i] = np.mean(f1[(i*500): (i*500+500)])
        #     y[i] = np.mean(f1[(150000 + i*500): (150000 + i*500+500)])
        #     flu[i] = -(x[i] ** 2 + y[i] ** 2) ** 0.5

        x = [0] * 700
        y = [0] * 700
        flu = [0] * 700
        for i in range(700):
            x[i] = np.mean(f1[(i*500): (i*500+500)])
            y[i] = np.mean(f1[(350000 + i*500): (350000 + i*500+500)])
            flu[i] = -(x[i] ** 2 + y[i] ** 2) ** 0.5

        np.savetxt(folder + '/' + filename+".csv", flu, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals
        plt.plot(flu)
        plt.show()
        exit()

    title = 'NV Diamond Crystal ODMR spectrum, ' + filename
    lg = 'NV Diamond Crystal'  #legend
    start = 2700
    stop = 3000
    CF = 3500  #center field
    SW = 1400  #sweep width

    unit = 'MHz'
    lx = 'Microwave frequency, MHz'
    ly = 'Fluorescence Intensity, AU'

    p1 = 2840   # peakrange
    p2 = 2900
    n1 = 2700   # noiserange1
    n2 = 2840
    n3 = 2900   # noiserange2
    n4 = 2980

    #read y, one way or the other
    # y=readcsv(folder, filename)

    y = Bruker(folder, filename)
    # np.savetxt("testdata/y.csv", y, delimiter=",")   #, fmt="%d")   #double
    start = CF-SW/2
    stop = CF+SW/2

    ## SNR and linewidth
    # SNR, pphh = SNRLW(start, stop, y, p1, p2, n1, n2, n3, n4)
    # print('signal-to-noise ratio and lw at half height of absorption signal:')
    # print('S/N: ', SNR)
    # print('LWHH, ' + unit + ': ', pphh)

    ##backcor background correction
    # y = bcremove(y, start, stop)  #try parameters
    # # bca= 4
    # # bcb=0.01
    # # bcc='sh'
    # # y = bcremove(y, start, stop, bca, bcb, bcc)   #know parameters

    # replot(start, stop, y, title, lx, ly,)   #optional: lg
    fineplot(start, stop, y, title, lx, ly, lg)
    exit()

    ###### customized plot multiple
    fn1 = 'ys20100904'           # MgB
    fn2 = 'ys20100905'           # MgB ball milled
    fn3 = 'ys20100906'           # MgB 10% graphene
    CF = 3350                   # center field
    SW = 2000                   # sweep width
    start = CF-SW/2
    stop = CF+SW/2

    y1 = Bruker(folder, fn1)
    y2 = Bruker(folder, fn2)
    y3 = Bruker(folder, fn3)
    y1 = np.array(y1)*2+1
    y2 = np.array(y2)/2
    y3 = np.array(y3)/2-2
    x=np.linspace(CF-SW/2, CF+SW/2, len(y1))

    font = FontProperties()
    font.set_family('serif')
    font.set_name('Arial')
    # font.set_style('italic')
    fig, ax = plt.subplots()

    ax.plot(x, y1, 'k', linewidth=1, label='MgB2 Pure')
    ax.plot(x, y2, 'b', linewidth=1, label='MgB2 Ball Milled')
    ax.plot(x, y3, 'g', linewidth=1, label='MgB2 + 10% graphene')

    ax.legend(prop=font)
    lx = 'Magnetic Field, G'
    ly = 'Signal Amplitude Scaled, AU'
    ax.set_xlabel(lx, fontname="Arial", fontsize=14)
    ax.set_ylabel(ly, fontname="Arial", fontsize=14)
    ax.set_title("EPR Spectra, Room Temperature", fontname='Arial', fontsize=18)

    for tick in ax.get_xticklabels():
        tick.set_fontname("Arial")
    for tick in ax.get_yticklabels():
        tick.set_fontname("Arial")

    plt.show()



