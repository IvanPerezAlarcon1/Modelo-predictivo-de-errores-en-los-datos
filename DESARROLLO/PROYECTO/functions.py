import pandas as pd
import os

def dataframe_from_file(archivo): #detecta el tipo de archivo y devuelve un dataframe del archivo ingresado
    aux1 , aux2 = os.path.splitext(archivo)
    if (aux2) == '.csv':
        dataframe = pd.read_csv(archivo)
    if (aux2) == '.xlsx':
        dataframe = pd.read_excel(archivo)
    return dataframe


def dframe_to_dicc(dataframe): #devuelve un diccionario con parametros comunes para toda columna
    dic = {}
    dic.setdefault('COLUMNAS',[])
    dic.setdefault('TYPES',[])
    dic.setdefault('MODA',[])
    for i in range(len(dataframe.columns)):
        dic['COLUMNAS'].append(dataframe.columns[i])
        dic['TYPES'].append(dataframe[dic['COLUMNAS'][i]].dtype.name)
        dic['MODA'].append(dataframe[dataframe.columns[i]].mode()[0])
    return dic


def sep_col_string_and_num(dataframe): #devuelve 2 arreglos con los nombres de columnas tipo numericas y string
    df_num = dataframe.select_dtypes(include=['int64','float64'])
    df_string = dataframe.select_dtypes(exclude=['int64','float64'])
    return df_num,df_string