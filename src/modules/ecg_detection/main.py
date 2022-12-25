#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pathlib
from ecgdetectors import Detectors
import os
import pandas as pd


file = 'datasets\X1001.csv'

if file.endswith(".csv"):
    fileName = os.path.join(file)
    if os.stat(fileName).st_size != 0:
        rawData = pd.read_csv(fileName, sep=",", header=None, skiprows=1).values
        utc_time = rawData[:, 0]
        unfiltered_ecg = rawData[:, 3]
        fs = 1000 #250

        detectors = Detectors(fs)

        r_peaks = detectors.pan_tompkins_detector(unfiltered_ecg)

        plt.figure()
        plt.plot(unfiltered_ecg)
        plt.plot(r_peaks, unfiltered_ecg[r_peaks], 'ro')
        plt.title("Detected R peaks")

        plt.show()