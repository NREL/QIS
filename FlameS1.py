# Source code
# https://pypi.org/project/seabreeze/
#single spectrum acquistion
import matplotlib.pylab as plt
import numpy as np
from seabreeze.spectrometers import Spectrometer


wavelength = None
wavelength = [550,800]  #the region of wavelength you want to plot

if __name__ == "__main__":
    spec = Spectrometer.from_first_available()
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
        print("Part of the spectrum is plotted.")

    plt.plot(a,b)
    plt.title('Flame-S ')
    plt.xlabel('Wavelength, nm')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()
    # np.savetxt("ys20021419ewl.csv", a, delimiter=",")  # save wavelength
    # np.savetxt("ys20021419e.csv", b, delimiter=",")  # save fluorescen intensity