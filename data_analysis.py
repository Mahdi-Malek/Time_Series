# -*- coding: utf-8 -*-

import pandas as pd



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
    
    
