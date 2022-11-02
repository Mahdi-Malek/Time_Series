# -*- coding: utf-8 -*-

import pandas as pd
import os
from statsmodels.tsa.deterministic import DeterministicProcess, CalendarFourier
from scipy.signal import periodogram
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression




def read_data(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(columns={'<DTYYYYMMDD>':'Date','<FIRST>':'First','<HIGH>':'High'
                            ,'<LOW>':'Low','<CLOSE>':'Close','<VALUE>':'Value',
                            '<VOL>':'Vol','<OPENINT>':'OpenInt','<PER>':'Per',
                            '<OPEN>':'Open','<LAST>':'Last'})   
    clean_df = df.iloc[:,1:]
    clean_df['Date'] = pd.to_datetime(clean_df['Date'],format='%Y%m%d')
    clean_df.index = clean_df['Date']
    clean_df = clean_df.iloc[:,1:]
    return(clean_df)
    
def find_files(dir):
    names = []
    paths = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            names = names + [name[:-4]]
            paths = paths + [os.path.join(root, name)]
    return(names, paths)  

def plot_mov_av(df, cols, win):
    moving_average = df[cols].rolling(window=win, center=True, min_periods=int(win/2)).mean()
    moving_average.plot()

def gen_time_trend_features(df, order, fore_steps):
    dp = DeterministicProcess(index=df.index, constant=False, order=order, drop=True)
    X_train = dp.in_sample()
    X_fore = dp.out_of_sample(steps=fore_steps)
    return(X_train, X_fore)

def plot_periodogram(ts, detrend='linear', ax=None):
    fs = pd.Timedelta("1Y") / pd.Timedelta("1D")
    freqencies, spectrum = periodogram(
        ts,
        fs=fs,
        detrend=detrend,
        window="boxcar",
        scaling='spectrum',
        )
    if ax is None:
        _, ax = plt.subplots()
    ax.step(freqencies, spectrum, color="purple")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12, 26, 52, 104])
    ax.set_xticklabels(
        [
            "Annual (1)",
            "Semiannual (2)",
            "Quarterly (4)",
            "Bimonthly (6)",
            "Monthly (12)",
            "Biweekly (26)",
            "Weekly (52)",
            "Semiweekly (104)",
        ],
        rotation=30,
    )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
    return ax

def seasonal_fourier_features(df, freq, fou_order, proc_order=1, seasonal=True):
    fourier = CalendarFourier(freq=freq, order=fou_order)  # fou_order sin/cos pairs for freq seasonality
    
    dp = DeterministicProcess(
        index=df.index,
        constant=True,               # dummy feature for bias (y-intercept)
        order=proc_order,            # trend (order 1 means linear)
        seasonal=seasonal,           # seasonality (indicators)
        additional_terms=[fourier],  # seasonality (fourier)
        drop=True,                   # drop terms to avoid collinearity
    )
    X = dp.in_sample()
    return(X)


