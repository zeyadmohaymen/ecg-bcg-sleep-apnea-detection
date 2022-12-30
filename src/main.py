import os

from modules.bcg_detection.bcg_main import bcg_analysis
from modules.ecg_detection.ecg_main import ecg_analysis
import pandas as pd
import numpy as np
from scipy.signal import resample



def save_to_txt(patient, ecg, bcg, err1, err2, err3):
    arr_string = ''
    arr_string += f'---------------------------------------------------------------------------[Patient {patient}]----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n \n'

    arr_string += 'ECG Heartrates: \n'
    for i in range(len(ecg)):
        arr_string += '{:4}'.format(ecg[i])
        arr_string += '  '

    arr_string += '\n \nBCG Heartrates: \n'
    for i in range(len(bcg)):
        arr_string += '{:4}'.format(bcg[i])
        arr_string += '  '

    arr_string += f'\n \nMean Absolute Error = {err1} \n'
    arr_string += f'RMS Error = {err2} \n'
    arr_string += f'Mean Absolute Percentage Error = {err3} \n \n \n'
    # arr_string += '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n \n'


    text_file = open('results\output.txt', "a")
    text_file.write(arr_string)
    text_file.close()



def errors_calc(ecg,bcg):

    n = len(ecg)
    mean_abs_error = 0
    root_mean_square_error = 0
    mean_abs_percentage_error = 0

    for i in range(n):

        mean_abs_error += abs(ecg[i]-bcg[i])
        root_mean_square_error += (bcg[i] - ecg[i]) ** 2
        mean_abs_percentage_error += abs( (ecg[i] - bcg[i]) / ecg[i] )

    mean_abs_error = mean_abs_error / n
    root_mean_square_error = np.sqrt(root_mean_square_error / n)
    mean_abs_percentage_error = mean_abs_percentage_error / n

    return round(mean_abs_error, 2), round(root_mean_square_error, 2), round(mean_abs_percentage_error, 2)



# assign directory
directory = 'datasets'
open('results\output.txt', 'w').close()

# iterate over files in
# that directory
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    # checking if it is a file
    if os.stat(path).st_size != 0:
        rawData = pd.read_csv(path, sep=",", header=None, skiprows=1).values

        bcg_data = rawData[:, 1]
        bcg_data = resample(bcg_data, round(50 * len(bcg_data) / 1000))

        ecg_data = rawData[:, 0]
        ecg_data = resample(ecg_data, round(50 * len(ecg_data) / 1000))

        bcg_hr = bcg_analysis(bcg_data)
        ecg_hr = ecg_analysis(ecg_data)

        err1, err2, err3 = errors_calc(ecg_hr, bcg_hr)

        save_to_txt(os.path.splitext(filename)[0], ecg_hr, bcg_hr, err1, err2, err3)
        