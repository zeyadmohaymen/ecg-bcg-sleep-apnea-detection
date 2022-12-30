# Import required libraries
import math
import os
import time

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter, resample

from modules.bcg_detection.band_pass_filtering import band_pass_filtering
from modules.bcg_detection.compute_vitals import vitals
from modules.bcg_detection.detect_apnea_events import apnea_events
from modules.bcg_detection.detect_body_movements import detect_patterns
from modules.bcg_detection.modwt_matlab_fft import modwt
from modules.bcg_detection.modwt_mra_matlab_fft import modwtmra
from modules.bcg_detection.remove_nonLinear_trend import remove_nonLinear_trend
from modules.bcg_detection.data_subplot import data_subplot
# ======================================================================================================================

# Main program starts here

def bcg_analysis(data):
    
    data_stream = data
    utc_time = np.linspace(0, len(data_stream) / 50, len(data_stream))

    start_point, end_point, window_shift, fs = 0, 500, 500, 50
    # ==========================================================================================================
    data_stream, utc_time = detect_patterns(start_point, end_point, window_shift, data_stream, utc_time, plot=1)
    
    w = modwt(data_stream, 'bior3.9', 4)
    dc = modwtmra(w, 'bior3.9')
    wavelet_cycle = dc[4]
    # ==========================================================================================================
    # Vital Signs estimation - (10 seconds window is an optimal size for vital signs measurement)
    t1, t2, window_length, window_shift = 0, 500, 500, 500
    limit = int(math.floor(data_stream.size / window_shift))
    # Heart Rate
    beats = vitals(t1, t2, window_shift, limit, wavelet_cycle, fs, mpd=1, plot=0)

    return beats