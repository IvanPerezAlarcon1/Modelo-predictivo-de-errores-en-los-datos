import numpy as numpy
import pandas as pd

import bdd_functions as bdf

#--------------NUMERICOS-----------------------
def imput_media(df,df_num,col_num_name,to_replace_val):
    df[col_num_name] = df[col_num_name].replace(to_replace = to_replace_val, value = round(df[col_num_name].mean(),2))
    df_num[col_num_name] = df_num[col_num_name].replace(to_replace = to_replace_val, value = round(df_num[col_num_name].mean(),2))





#--------------------STRINGS----------------------------

def imputar_col_string(df,df_string,nom_col_string):
    c1, cx = bdf.conectarse()
    cx.execute("""
        SELECT "NOM_COL", "MODA", "TIPO_DATO"
        FROM pruebas."DICCIONARIO_DE_DATOS" WHERE "NOM_COL" = '{v1}';
        """.format(v1 = nom_col_string))
    for i in cx.fetchall():
        df[nom_col_string] = df[nom_col_string].fillna(i[1])
        df_string[nom_col_string] = df_string[nom_col_string].fillna(i[1])
    cx.close()


def imput_df_string(df,df_string):
    cant_filas_df = df.shape[0] #CANT. DE FILAS DEL DATAFRAME
    for i in range(len(df_string.columns)):
        count_null = df_string[df_string.columns[i]].isna().sum() #cant.nulos columna
        porc_nulos = round((count_null/cant_filas_df)*100,1)
        print(df_string.columns[i], "CANT. NULOS: ", count_null, "PORCENTAJE DE NULOS: {}%".format(porc_nulos))
        if(porc_nulos == 0.0):
            #SI EL % DE NULOS ES 0%, LA COLUMNA NO REQUIERE TRATAMIENTO
            print("La columna {}, no requiere tratamiento de valores nulos, ya que tiene un {}% de valores nulos.".format(df_string.columns[i],porc_nulos))
            print("\n")
        if(porc_nulos <= 10.0):
            #SI EL % DE NULOS ES <=10% SE REQUIERE TRATAMIENTO TIPO STRING, O SEA IMPUTACIÓN POR MODA O VALOR PREDEFINIDO
            print("La columna {}, será tratada, su porcentaje de nulos no supera el 10%, ya que es de {}%".format(df_string.columns[i],porc_nulos))
            imputar_col_string(df,df_string,df_string.columns[i])
            print("\n")
        else:
            #SI EL % DE NULOS ES > 10%, NO SE REALIZARÁN MÁS ACCIONES SOBRE EL CONJUNTO YA QUE UNA COLUMNA POSEE UN NIVEL DE DATOS MUY POCO REPRESENTATIVO.
            print("La columna {}, posee un {}% de nulos, el cual supera el 10%, favor de ingresar un conjunto de datos que no supere este porcentaje de nulos en cualquiera de sus columnas.")
            break #rompe el ciclo for, no la iteracion solamente
