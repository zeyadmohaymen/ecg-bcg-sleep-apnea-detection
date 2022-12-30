import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

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
    mean_abs_percentage_error = mean_abs_percentage_error / n * 100

    return round(mean_abs_error, 2), round(root_mean_square_error, 2), round(mean_abs_percentage_error, 2)



def save_to_txt(patient, ecg, bcg, err1, err2, err3):
    arr_string = ''
    arr_string += f'--------------------------------------------------------------------------- [Patient {patient}] ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n \n'

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
    arr_string += f'Mean Absolute Percentage Error = {err3} % \n \n \n'


    text_file = open('results\output.txt', "a")
    text_file.write(arr_string)
    text_file.close()


def plots(ecg, bcg, patient):

    # Bland-Altman
    sm.graphics.mean_diff_plot(ecg, bcg)
    plt.title(f'{patient}\'s Bland-Altman Plot')
    plt.savefig('results/bland_altman', bbox_inches='tight')

    # Pearson Correlation
    plt.figure(figsize = (9, 5))
    plt.scatter(ecg, bcg)
    pearson_corr_coeff = round(np.corrcoef(ecg, bcg)[0][1], 3)
    plt.title(f'{patient}\'s Pearson Correlation Coefficient of {pearson_corr_coeff}')
    plt.xlabel('ECG')
    plt.ylabel('BCG')
    plt.savefig('results/pearson_correlation', bbox_inches='tight')