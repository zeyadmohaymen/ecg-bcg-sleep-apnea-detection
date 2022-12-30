import os

from modules.bcg_detection.bcg_main import bcg_analysis
from modules.ecg_detection.ecg_main import ecg_analysis
from modules.utils import errors_calc, save_to_txt, plots
import pandas as pd
from scipy.signal import resample





def main():

    # assign directory
    directory = 'datasets'
    open('results\output.txt', 'w').close()

    # iterate over all files in the directory
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        # check file validity
        if os.stat(path).st_size != 0:
            rawData = pd.read_csv(path, sep=",", header=None, skiprows=1).values

            # ECG data stored and downsampled from 1000 Hz to 50 Hz
            ecg_data = rawData[:, 0]
            ecg_data = resample(ecg_data, round(50 * len(ecg_data) / 1000))

            # BCG data stored and downsampled from 1000 Hz to 50 Hz
            bcg_data = rawData[:, 1]
            bcg_data = resample(bcg_data, round(50 * len(bcg_data) / 1000))

            # Analyze the two signals and return their respective heart rate estimates
            ecg_hr = ecg_analysis(ecg_data)
            bcg_hr = bcg_analysis(bcg_data)

            # Calculate MAE, RMSE, and MAPE between the two signals
            err1, err2, err3 = errors_calc(ecg_hr, bcg_hr)

            # Save results in .txt file (results/output.txt)
            save_to_txt(os.path.splitext(filename)[0], ecg_hr, bcg_hr, err1, err2, err3)


            if filename == 'X1010.csv':
                plots(ecg_hr, bcg_hr, os.path.splitext(filename)[0])



if __name__ == '__main__':
    main()
        