# Ocean optics FlameS spectrometer
# https://pypi.org/project/seabreeze/
# https://www.oceaninsight.com/support/software-downloads/  "SeaBreeze Open-Source OEM Device Driver"

import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
from seabreeze.spectrometers import Spectrometer

def FlameS_save(wavelength, integ, folder, filename):
    spec = Spectrometer.from_first_available()
    spec.integration_time_micros(integ)  #us
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
        print("Part of the spectrum is plotted.")

    plt.plot(a,b)
    plt.title('Flame-S, Diamond in box '+filename)
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()
    np.savetxt(folder + filename + "wl.csv", a, delimiter=",", fmt='%f')  # save wavelength
    np.savetxt(folder + filename + ".csv", b, delimiter=",", fmt='%f')  # save fluorescen intensity


def FlameS_view(wavelength, integ):
    if wavelength is not None:
        print("Part of the spectrum is plotted.")

    def animate(i):
        spec = Spectrometer.from_first_available()
        spec.integration_time_micros(integ)
        a = spec.wavelengths()
        b = spec.intensities()
        a = a[30:]  # delete the first pseudo peak
        b = b[30:]
        if b.max() > 65500:
            print("Flame is saturated, please reduce integration time")

        if wavelength is not None:
            step = abs(a[1] - a[0])
            p = np.where(abs(a - wavelength[0]) < step)[0][0]  # define baseline
            q = np.where(abs(a - wavelength[1]) < step)[0][0]
            a = a[p:q]
            b = b[p:q]

        ax1.clear()
        ax1.plot(a, b)
        print(i)
        # if i == 10:
        #     exit()


    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.title('Flame-S ')
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()


if __name__ == "__main__":
    folder = '/Users/yshi2/Documents/2020.8.14/'
    filename = 'ys20072101'
    wavelength = None
    wavelength = [550, 800]  # the region of wavelength you want to plot
    integ = 1000000          #integration time, us

    # FlameS_save(wavelength, integ, folder, filename)
    FlameS_view(wavelength, integ)