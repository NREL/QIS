#dynamic acquisition
import matplotlib.pylab as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import numpy as np

style.use('fivethirtyeight')
from seabreeze.spectrometers import Spectrometer
wavelength = None
wavelength = [550,800]  #the region of wavelength you want to plot

def animate(i):
    print(time.time())
    spec.integration_time_micros(1000000)
    a = spec.wavelengths()
    b = spec.intensities()
    a = a[30:]  # delete the first pseudo peak
    b = b[30:]
    if b.max() > 65500:
        print("Flame is saturated, please reduce integration time")

    if wavelength is not None:
        step = abs(a[1] - a[0])
        p = np.where(abs(a-wavelength[0])<step)[0][0]   # define baseline
        q = np.where(abs(a-wavelength[1])<step)[0][0]
        a = a[p:q]
        b = b[p:q]
        # print("Part of the spectrum is plotted.")

    # with open('ooflame.txt', 'a') as f:
    #     f.write(str(b)+',')

    ax1.clear()
    ax1.plot(a, b)
    print(i)
    if i == 10:
        exit()

if __name__ == "__main__":
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    spec = Spectrometer.from_first_available()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.title('Flame-S ')
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()


