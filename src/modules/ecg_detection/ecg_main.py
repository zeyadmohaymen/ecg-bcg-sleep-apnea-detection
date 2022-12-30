#!/usr/bin/python3

import math
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import heartpy as hp
import os
import pandas as pd
from scipy.signal import savgol_filter, resample
from modules.bcg_detection.modwt_matlab_fft import modwt
from modules.bcg_detection.modwt_mra_matlab_fft import modwtmra



def ecg_analysis(data):

    sample_rate = 50

    w = modwt(data, 'bior3.9', 4)
    dc = modwtmra(w, 'bior3.9')
    wavelet_cycle = dc[4]

    # Processes ECG, while segmenting the signal to 10 second windows
    # Returns a dictionary with signal stats
    wd, m = hp.process_segmentwise(wavelet_cycle, sample_rate, 10)

    # Return heartrates
    return [round(x, 1) for x in m['bpm']]