import pandas as pd
import os

import functions as f
import imputaciones_functions as imf
import outliers_functions as of

#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_NGRAMS-test-2-cols--witherrors.csv'
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar
archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2-imput-manual-agent-col.csv' # se demora 2.8 seg en terminar

df = f.dataframe_from_file(archivo)

df_col_numericas,df_col_string = f.sep_col_string_and_num(df)

cant_filas_df = df_col_numericas.shape[0] #CANT. DE FILAS DEL DATAFRAME
cant_col_df = df_col_numericas.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
print("Cant. filas dataframe: ", cant_filas_df,"\n","Cant. columnas dataframe: ", cant_col_df,"\n")

print("Imputaciones para columnas STRING: ") #para columnas string, si debe ser el de la bdd el valor a imputar, ya que el usuario puede modificar este valor
print(df_col_string.columns)
print("--------------PRE-CORRECCION DE NULOS----------")
imf.imput_df_string(df,df_col_string)

print("--------------POST-CORRECCION DE NULOS STRING----------")
for i in range(len(df_col_string.columns)):
    count_null = cont_null = df_col_string[df_col_string.columns[i]].isna().sum() #cant.nulos columna
    porc_nulos = round((cont_null/cant_filas_df)*100,1)
    print(df_col_string.columns[i], "CANT. NULOS: ", count_null, "PORCENTAJE DE NULOS: {}%".format(porc_nulos))
    print(df_col_string[df_col_string.columns[i]].unique())
    print('\n')





print("--------------Imputaciones para columnas NUMÉRICAS: -----------------------")
print(df_col_numericas.columns)

imf.input_df_numerico(df,df_col_numericas)

print("--------------COLUMNAS NUMERICAS POST-IMPUTACION: -----------------------")
for i in range(len(df_col_numericas.columns)):
    cur_col = round(df_col_numericas[df_col_numericas.columns[i]].kurt(),1) #curtosis
    count_null = df_col_numericas[df_col_numericas.columns[i]].isna().sum() #cant.nulos columna
    cant_filas_df = df_col_numericas.shape[0] #CANT. DE FILAS DEL DATAFRAME
    cant_col_df = df_col_numericas.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
    IRQ = of.inter_cuar_rang(df_col_numericas[df_col_numericas.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
    porc_nulos = round((count_null/cant_filas_df)*100,1)

    print(df_col_numericas.columns[i])
    print(count_null)
    print(cant_filas_df)
    print(porc_nulos)