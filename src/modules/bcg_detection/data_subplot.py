import matplotlib
matplotlib.use('agg')
from matplotlib.pyplot import plot, savefig, figure
import matplotlib.pyplot as plt
import numpy as np
import os

def normalize(sig):
    sig = np.divide(sig, np.sum(np.abs(sig) ** 2, axis=-1) ** (1. / 2))
    return sig


def data_subplot(raw_data, movement, breathing, dc, t1, t2):
    raw_data = normalize(raw_data)
    movement = normalize(movement)
    breathing = normalize(breathing)
    dc = normalize(dc)
    steps = np.arange(t1, t2) / 50

    fig = plt.figure()
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)

    ax1.plot(steps, raw_data[t1:t2], lw=2, color='k', label='Raw Signal')
    ax1.set_xlabel('Time [Seconds]')
    ax1.set_ylabel('Ampltiude')
    ax1.legend(bbox_to_anchor=(1, 1.3), loc='center right')
    plt.subplots_adjust(hspace=0.8)

    ax2.plot(steps, movement[t1:t2], lw=2, color='k', label='BCG Signal')
    ax2.plot(steps, dc[t1:t2], lw=2, color='r', ls='-.', label='Level 4 Smooth')
    ax2.set_xlabel('Time [Seconds]')
    ax2.set_ylabel('Ampltiude')
    ax2.legend(bbox_to_anchor=(1, 1.3), loc='center right')
    plt.subplots_adjust(hspace=0.8)

    ax3.plot(steps, breathing[t1:t2], lw=2, color='k', label='Respiratory Signal')
    ax3.set_xlabel('Time [Seconds]')
    ax3.set_ylabel('Ampltiude')
    ax3.legend(bbox_to_anchor=(1, 1.3), loc='center right')
    plt.subplots_adjust(hspace=0.8)
    
    plt.savefig('results/bcg_detection/vitals')
