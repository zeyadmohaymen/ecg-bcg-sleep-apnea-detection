import numpy as np

from detect_peaks import detect_peaks


def compute_rate(beats, time, mpd):

    indices = detect_peaks(beats, mpd=mpd)

    if len(indices) > 1:
        peak_to_peak = []
        for i in range(0, indices.size - 1):
            peak_to_peak = np.append(peak_to_peak, time[indices[i + 1]] - time[indices[i]])
        mean_heart_rate = np.average(peak_to_peak, axis=0)
        if mean_heart_rate != 0: bpm_avg = 1000 * (60 / mean_heart_rate)
        else: bpm_avg = 0
        return np.round(bpm_avg, decimals=2), indices
    else:
        return 0.0, 0.0
