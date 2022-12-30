
import matplotlib.pyplot as plt
import numpy as np


def box_plot(array,array2):
 
    # Creating dataset
    
   
    data = [array, array2 ]

    
    fig = plt.figure()
    # Creating axes instance
   
    ax = fig.add_axes([0.05,0.05,0.9,0.9])
    bp =ax.boxplot(data)
    # Creating plot
    plt.savefig('box_plot_ecg.png')
    # plt.boxplot(data)
    
    # show plot
