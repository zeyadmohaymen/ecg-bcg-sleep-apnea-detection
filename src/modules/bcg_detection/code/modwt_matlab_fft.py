"""
Created on %(31/08/2016)
Program to compute Maximal Overlap Discrete Wavelet Transform
Equivalent to Matlab modwt
"""
import math
import sys

import numpy as np
import pyfftw
import pywt


def modwt(x, wname, J):
    # % Convert data to row vector
    if x.shape[0] > 1:
        x = x.flatten()

    # % Record original data length
    datalength = x.size

    # % Check that the level of the transform does not exceed floor(log2(len(x))
    Jmax = np.floor(math.log(datalength, 2))
    if J <= 0 or J > Jmax:
        print('Wavelet:modwt:MRALevel')
        sys.exit()

    # % obtain new signal length if needed
    siglen = x.size
    Nrep = siglen

    # % Scale the scaling and wavelet filters for the MODWT
    wavelet = pywt.Wavelet(wname)
    Lo = wavelet.rec_lo
    Hi = wavelet.rec_hi
    Lo = np.array(Lo) / np.sqrt(2)
    Hi = np.array(Hi) / np.sqrt(2)

    # % Ensure Lo and Hi are row vectors
    if Lo.shape[0] > 1:
        Lo = Lo.flatten()
    if Hi.shape[0] > 1:
        Hi = Hi.flatten()

    # % If the signal length is less than the filter length, need to
    # % periodize the signal in order to use the DFT algorithm
    if siglen < len(Lo):
        xp = np.tile(x, (1, len(Lo) - siglen))
        x = np.append(x, xp)
        Nrep = x.size

    # % Allocate coefficient array
    w = []  # np.zeros(shape=(J + 1, Nrep))

    # % Obtain the DFT of the filters
    G = pyfftw.interfaces.numpy_fft.fft(Lo, Nrep, planner_effort='FFTW_ESTIMATE', threads=1).T
    H = pyfftw.interfaces.numpy_fft.fft(Hi, Nrep, planner_effort='FFTW_ESTIMATE', threads=1).T

    # %Obtain the DFT of the data
    Vhat = pyfftw.interfaces.numpy_fft.fft(x, planner_effort='FFTW_ESTIMATE').T

    # % [Vhat,What] = modwtfft(X,G,H,J)
    def modwtdec(X, G, H, J):
        N = X.size
        upfactor = 2 ** J
        Gup = G[np.mod(upfactor * np.arange(0, N), N)]
        Hup = H[np.mod(upfactor * np.arange(0, N), N)]
        Vhat = np.multiply(Gup, X)
        What = np.multiply(Hup, X)
        return Vhat, What

    # % Main MODWT algorithm
    for jj in range(J):
        [Vhat, What] = modwtdec(Vhat, G, H, jj)
        w.append(pyfftw.interfaces.numpy_fft.ifft(What, planner_effort='FFTW_ESTIMATE', threads=1).real)
    w.append(pyfftw.interfaces.numpy_fft.ifft(Vhat, planner_effort='FFTW_ESTIMATE', threads=1).real)
    w = np.vstack(w)
    w = w[:, 0:siglen]
    return w
