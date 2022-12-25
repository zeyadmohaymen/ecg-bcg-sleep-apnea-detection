"""
Created on %(25/09/2017)
Function to remove nonlinear trend.
"""

import numpy as np


def remove_nonLinear_trend(input_signal, order):
    # Detrend with a n order polynomial
    model = np.polyfit(np.arange(0, input_signal.size), input_signal, order)
    predicted = np.polyval(model, np.arange(0, input_signal.size))
    filteredSignal = input_signal - predicted
    return filteredSignal
