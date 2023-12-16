<h1 align="center" id="title">Sleep Apnea Detection Using Ballistocardiography And ECG</h1>

<p align="center"><img src="https://socialify.git.ci/zeyadmohaymen/ecg-bcg-sleep-apnea-detection/image?font=Raleway&amp;language=1&amp;name=1&amp;pattern=Signal&amp;theme=Dark" alt="project-image"></p>

<p id="description">A signal processing algorithm that uses simultaneously collected BCG and ECG data and estimates heart rate for apnea detection. Various error metrics and comparative plots are generated to compare the accuracy of heart rate estimation algorithms using BCD as compared to ECG.</p>
  
  <br />
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Import ballistocardiography and ecg datasets
*   Signals preprocessing
*   Peak detection and heart rate estimation using fixed-interval windowing
*   MAE RMSE and MAPE metrics are calculated to evaluate accuracy of BCG algorithm
*   Bland-Altman Pearson Correlation and Boxplots generated for the two algorithms

  <br />
<h2>🎯 Results</h2>

### Plots
| Bland Altman | Boxplots | Pearson Correlation | 
| --- | --- | --- |
| ![Bland-Altman](/results/bland_altman.png) | ![Boxplots](/results/box_plot.png) |![Pearson](/results/pearson_correlation.png) | 

### Documents
- [Statistical Summary Text File](/results/output.txt)
- [Presentation](/docs/Presentation.pdf)
- [Report](/docs/Report.pdf)

<br />
<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository.</p>

<p>2. Install dependecies</p>

```
pip install -r requirements.txt
```

<p>3. Download and extract dataset.</p>

<p>4. Run the program.</p>

```
python main.py
```

## References

> Sadek, Ibrahim, and Bessam Abdulrazak. “A comparison of three heart rate
detection algorithms over ballistocardiogram signals.” Biomedical Signal
Processing and Control (2021).

> Sadek, Ibrahim, et al. “A new approach for detecting sleep apnea using a
contactless bed sensor: Comparison study.” Journal of medical Internet research
(2020).
