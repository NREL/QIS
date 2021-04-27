# Ocean optics FlameS spectrometer
# https://pypi.org/project/seabreeze/
# https://www.oceaninsight.com/support/software-downloads/  "SeaBreeze Open-Source OEM Device Driver"

import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
import seabreeze
from seabreeze.spectrometers import Spectrometer

def FlameS_save(wavelength1, wavelength2, integ, folder, filename, title):
    spec = Spectrometer.from_first_available()
    spec.integration_time_micros(integ)  #us
    a = spec.wavelengths()
    b = spec.intensities()
    a = a[30:]  # delete the first pseudo peak
    b = b[30:]
    msg=''

    if b.max() > 65500:
        msg = "Flame is saturated, please reduce integration time."
        print(msg)

    step = abs(a[1] - a[0])

    if (wavelength1 is not None) and (wavelength2 is not None):
        msg=msg+"\nPart of the spectrum is plotted."
        print(msg)

    if wavelength1 is not None:
        p = np.where(abs(a-wavelength1)<step)[0][0]   # define baseline
        a = a[p:]
        b = b[p:]

    if wavelength2 is not None:
        q = np.where(abs(a-wavelength2)<step)[0][0]
        a = a[:q]
        b = b[:q]

    np.savetxt(folder + '/' + filename + "wl.csv", a, delimiter=",")  # save wavelength
    np.savetxt(folder + '/' + filename + ".csv", b, delimiter=",")  # save fluorescen intensity
    plt.plot(a,b)
    plt.title(title + ' ' + filename)
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()
    return msg


def FlameS_view(wavelength1, wavelength2, integ, title='Ocean Insight FLAME-S VIS-NIR Spectrometer'):
    msg=''
    if (wavelength1 is not None) and (wavelength2 is not None):
        msg="Part of the spectrum is plotted."
        print(msg)

    def animate(i):
        spec = Spectrometer.from_first_available()
        spec.integration_time_micros(integ)
        a = spec.wavelengths()
        b = spec.intensities()
        a = a[30:]  # delete the first pseudo peak
        b = b[30:]
        if b.max() > 65500:
            msg="Flame is saturated, please reduce integration time"
            print(msg)

        step = abs(a[1] - a[0])
        if wavelength1 is not None:
            p = np.where(abs(a - wavelength1) < step)[0][0]  # define baseline
            a = a[p:]
            b = b[p:]

        if wavelength2 is not None:
            q = np.where(abs(a - wavelength2) < step)[0][0]
            a = a[:q]
            b = b[:q]

        # for i in range(len(b)):  #filter out peaks
        #     if b[i]>3000:
        #         b[i]=2400

        ax1.clear()
        ax1.plot(a, b)
        plt.title(title)
        plt.xlabel('Wavelength, nm')
        plt.ylabel('Signal Amplitude, AU')
        print(i)
        # if i == 10:
        #     exit()
        # return msg


    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()


if __name__ == "__main__":
    folder='/Users/yshi2/Desktop/instrument1'
    filename = 'ys21021801'
    wavelength1 = None
    wavelength2 = None
    wavelength1 = 550
    wavelength2 = 800  # the region of wavelength you want to plot
    integ = 1000000          #integration time, us
    title = 'Flame-S'

    k = seabreeze.spectrometers.list_devices()
    print(k)

    FlameS_view(wavelength1, wavelength2, integ, title)
    # FlameS_save(wavelength1, wavelength2, integ, folder, filename, title)
