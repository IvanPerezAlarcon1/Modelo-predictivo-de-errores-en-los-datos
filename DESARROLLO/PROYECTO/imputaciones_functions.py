import numpy as numpy
import pandas as pd

def imput_media(df,df_num,col_num_name,to_replace_val):
	df[col_num_name] = df[col_num_name].replace(to_replace = to_replace_val, value = round(df[col_num_name].mean(),2))
	df_num[col_num_name] = df_num[col_num_name].replace(to_replace = to_replace_val, value = round(df_num[col_num_name].mean(),2))


#def imputar_col_string():
