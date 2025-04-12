import pandas as pd
import numpy as np
file_path=r'D:\coderviewsTech.Pvt.ltd\mynotebook\customer_shopping_data.csv'
def read():
    '''
    This function used for read the data for data analysis 
    '''
    data=pd.read_csv(file_path)
    return data.head()