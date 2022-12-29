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
    print('\nstart processing ...')

    # file = 'datasets\X1001.csv'

    # if file.endswith(".csv"):
    # fileName = os.path.join(file)
    # if os.stat(fileName).st_size != 0:
    # rawData = pd.read_csv(fileName, sep=",", header=None, skiprows=1).values
    # utc_time = rawData[:, 0]
    # data_stream = rawData[:, 5]
    data_stream = data
    utc_time = np.linspace(0, len(data_stream) / 50, len(data_stream))
    # data_stream, utc_time = resample(data_stream, round(50 * len(data_stream) / 1000), utc_time)

    start_point, end_point, window_shift, fs = 0, 500, 500, 50
    # ==========================================================================================================
    data_stream, utc_time = detect_patterns(start_point, end_point, window_shift, data_stream, utc_time, plot=1)
    # ==========================================================================================================
    # BCG signal extraction
    movement = band_pass_filtering(data_stream, fs, "bcg")
    # ==========================================================================================================
    # Respiratory signal extraction
    breathing = band_pass_filtering(data_stream, fs, "breath")
    breathing = remove_nonLinear_trend(breathing, 3)
    breathing = savgol_filter(breathing, 11, 3)
    # ==========================================================================================================
    w = modwt(movement, 'bior3.9', 4)
    dc = modwtmra(w, 'bior3.9')
    wavelet_cycle = dc[4]
    # ==========================================================================================================
    # Vital Signs estimation - (10 seconds window is an optimal size for vital signs measurement)
    t1, t2, window_length, window_shift = 0, 500, 500, 500
    # hop_size = math.floor((window_length - 1) / 2)
    limit = int(math.floor(breathing.size / window_shift))
    # ==========================================================================================================
    # Heart Rate
    beats = vitals(t1, t2, window_shift, limit, wavelet_cycle, fs, mpd=1, plot=0)
    print(beats)
    # print('\nHeart Rate Information')
    # print('Minimum pulse : ', np.around(np.min(beats)))
    # print('Maximum pulse : ', np.around(np.max(beats)))
    # print('Average pulse : ', np.around(np.mean(beats)))
    # # Breathing Rate
    # beats = vitals(t1, t2, window_shift, limit, breathing, fs, mpd=1, plot=0)
    # print('\nRespiratory Rate Information')
    # print('Minimum breathing : ', np.around(np.min(beats)))
    # print('Maximum breathing : ', np.around(np.max(beats)))
    # print('Average breathing : ', np.around(np.mean(beats)))
    # # ==============================================================================================================
    # thresh = 0.3
    # events = apnea_events(breathing, utc_time, thresh=thresh)
    # ==============================================================================================================
    # Plot Vitals Example
    t1, t2 = 2500, 2500 * 2
    data_subplot(data_stream, movement, breathing, wavelet_cycle, t1, t2)
    # ==============================================================================================================
    print('\nEnd processing ...')
    # ==================================================================================================================
    return beats