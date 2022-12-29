"""
Created on %(31/08/2016)
Program to compute Multi-Resolution Analysis / Maximal Overlap Discrete Wavelet Transform
Equivalent to Matlab modwtmra
"""
import sys

import numpy as np
import pyfftw
import pywt


def modwtmra(w, wname):
    # % The input to modwtmra must be a matrix
    if w.shape[0] == 1 and w.shape[1] > 1 or w.shape[0] > 1 and w.shape[1] == 1:
        print('Wavelet:modwt:MRASize')
        sys.exit()

    # % get the size of the output coefficients
    cfslength = w.shape[1]
    J0 = w.shape[0] - 1

    nullinput = np.zeros(cfslength)
    N = cfslength

    # % Scale the scaling and wavelet filters for the MODWT
    wavelet = pywt.Wavelet(wname)
    Lo = wavelet.rec_lo
    Hi = wavelet.rec_hi
    Lo = np.array(Lo) / np.sqrt(2)
    Hi = np.array(Hi) / np.sqrt(2)

    if cfslength < len(Lo):
        wp = np.tile(w, (1, len(Lo) - cfslength))
        w = np.append(w, wp, axis=1)
        cfslength = w.shape[1]
        nullinput = np.zeros(cfslength)

    G = pyfftw.interfaces.numpy_fft.fft(Lo, cfslength, planner_effort='FFTW_ESTIMATE', threads=1).T
    H = pyfftw.interfaces.numpy_fft.fft(Hi, cfslength, planner_effort='FFTW_ESTIMATE', threads=1).T

    # % Allocate array for MRA
    mra = []  # np.zeros(shape=(J0 + 1, N))

    def imodwtrec(Vin, Win, G, H, J):
        N = Vin.size
        Vhat = pyfftw.interfaces.numpy_fft.fft(Vin, planner_effort='FFTW_ESTIMATE', threads=1).T
        What = pyfftw.interfaces.numpy_fft.fft(Win, planner_effort='FFTW_ESTIMATE', threads=1).T
        upfactor = 2 ** J
        Gup = np.conj(G[np.mod(upfactor * np.arange(0, N), N)])
        Hup = np.conj(H[np.mod(upfactor * np.arange(0, N), N)])
        Vout = pyfftw.interfaces.numpy_fft.ifft(np.multiply(Gup, Vhat) + np.multiply(Hup, What),
                                                planner_effort='FFTW_ESTIMATE', threads=1).real
        return Vout

    def imodwtDetails(coefs, nullinput, lev, Lo, Hi, N):
        v = nullinput
        w = coefs
        for jj in range(lev + 1, 0, -1):
            vout = imodwtrec(v, w, Lo, Hi, jj - 1)
            w = nullinput
            v = vout
        details = v[0:N]
        return details

    def imodwtSmooth(scalingcoefs, nullinput, Lo, Hi, N, J0):
        v = scalingcoefs
        for J in range(J0 + 1, 0, -1):
            vout = imodwtrec(v, nullinput, Lo, Hi, J - 1)
            v = vout
        smooth = v[0:N]
        return smooth

    # % Main MRA - MODWT algorithm
    for J in range(J0, 0, -1):
        wcfs = w[J - 1]
        details = imodwtDetails(wcfs, nullinput, J - 1, G, H, cfslength)
        details = details[0:N]
        mra.append(details)
    scalingcoefs = w[J0:]
    smooth = imodwtSmooth(scalingcoefs.flatten(), nullinput, G, H, cfslength, J0 - 1)
    mra = mra[::-1]
    mra.append(smooth[0: N])
    mra = np.vstack(mra)
    return mra
