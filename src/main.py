import os

from modules.bcg_detection.bcg_main import bcg_analysis
from modules.ecg_detection.ecg_main import ecg_analysis
import pandas as pd
from scipy.signal import resample

file = 'datasets\X1012.csv'

if file.endswith(".csv"):
    fileName = os.path.join(file)
    if os.stat(fileName).st_size != 0:
        rawData = pd.read_csv(fileName, sep=",", header=None, skiprows=1).values

        bcg_data = rawData[:, 2]
        bcg_data = resample(bcg_data, round(50 * len(bcg_data) / 1000))

        ecg_data = rawData[:, 0]
        ecg_data = resample(ecg_data, round(50 * len(ecg_data) / 1000))

        bcg_hr = bcg_analysis(bcg_data)
        ecg_hr = ecg_analysis(ecg_data)