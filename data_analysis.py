# -*- coding: utf-8 -*-

import pandas as pd
import os



def read_data(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(columns={'<DTYYYYMMDD>':'Date','<FIRST>':'First','<HIGH>':'High'
                            ,'<LOW>':'Low','<CLOSE>':'Close','<VALUE>':'Value',
                            '<VOL>':'Vol','<OPENINT>':'OpenInt','<PER>':'Per',
                            '<OPEN>':'Open','<LAST>':'Last'})   
    clean_df = df.iloc[:,1:]
    pd.to_datetime(clean_df['Date'],format='%Y%m%d')
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
    from statsmodels.tsa.deterministic import DeterministicProcess
    dp = DeterministicProcess(index=df.index, constant=False, order=order, drop=True)
    X_train = dp.in_sample()
    X_fore = dp.out_ofsample(steps=fore_steps)
    return(X_train, X_fore)
