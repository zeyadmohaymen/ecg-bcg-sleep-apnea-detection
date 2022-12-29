"""
Created on %(25/09/2017)
Function to perform a Chebyshev type I bandpass filter for heart rate and breathing.
"""

from scipy.signal import cheby1, filtfilt


def band_pass_filtering(data, fs, filter_type):
    if filter_type == "bcg":
        [b_cheby_high, a_cheby_high] = cheby1(2, 0.5, [2.5 / (fs / 2)], btype='high', analog=False)
        bcg_ = filtfilt(b_cheby_high, a_cheby_high, data)
        [b_cheby_low, a_cheby_low] = cheby1(4, 0.5, [5.0 / (fs / 2)], btype='low', analog=False)
        filtered_data = filtfilt(b_cheby_low, a_cheby_low, bcg_)
    elif filter_type == "breath":
        [b_cheby_high, a_cheby_high] = cheby1(2, 0.5, [0.01 / (fs / 2)], btype='high', analog=False)
        bcg_ = filtfilt(b_cheby_high, a_cheby_high, data)
        [b_cheby_low, a_cheby_low] = cheby1(4, 0.5, [0.4 / (fs / 2)], btype='low', analog=False)
        filtered_data = filtfilt(b_cheby_low, a_cheby_low, bcg_)
    else:
        filtered_data = data
    return filtered_data
