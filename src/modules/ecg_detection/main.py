# #!/usr/bin/python3

# import numpy as np
# import matplotlib.pyplot as plt
# import pathlib
# from ecgdetectors import Detectors

# current_dir = pathlib.Path(__file__).resolve()

# example_dir = 'datasets\ECG.tsv'
# unfiltered_ecg_dat = np.loadtxt(example_dir) 
# unfiltered_ecg = unfiltered_ecg_dat[:, 0]
# fs = 250

# detectors = Detectors(fs)

# r_peaks = detectors.pan_tompkins_detector(unfiltered_ecg)

# plt.figure()
# plt.plot(unfiltered_ecg)
# plt.plot(r_peaks, unfiltered_ecg[r_peaks], 'ro')
# plt.title("Detected R peaks")

# plt.show()