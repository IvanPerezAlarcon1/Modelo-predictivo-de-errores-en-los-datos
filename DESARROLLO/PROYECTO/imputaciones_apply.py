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

'''
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
'''

print("--------------Imputaciones para columnas NUMÉRICAS: -----------------------")
print(df_col_numericas.columns)

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
    if(porc_nulos == 0):
        print("La columna {}, no requiere tratamiento de nulos.".format(df_col_numericas.columns[i]))
    elif(porc_nulos <= 10 and porc_nulos > 0):
        print("La columna {}, contiene un {}% de nulos, por lo que es tratable.".format(df_col_numericas.columns[i], porc_nulos))
        if(cur_col >= -3.0 and cur_col <=3.0):
            #SI LA COLUMNA CONTIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIANA - ESTE ESCENARIO SE ABORDA EN outliers_functions.py
            #SI LA COLUMNA NO TIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIA
            print("Esta columna posee una distribucion normal o cercana a normal, ya que su CURTOSIS es {}.".format(cur_col))
            imf.input_media_2(df,df_col_numericas,df_col_numericas.columns[i])
        else:
            #SE IMPUTA POR MEDIANA
            print("Esta columna no posee una distrib normal o cercana, ya que su curtosis es {}.".format(cur_col))
            imf.input_mediana(df,df_col_numericas,df_col_numericas.columns[i])


    elif(porc_nulos > 10):
        print("La columna {}, posee un {}% de valores nulos, se recomienda imputar valores hasta obtener menos del 10% de valores nulos para que el conjunto tenga un grado de credibilidad aceptable.".format(df_col_numericas.columns[i], porc_nulos))
        break
    else:
        print('{},{}'.format(df_col_numericas.columns[i], porc_nulos))
        print("Se ha presentado un error en el proceso.")
        break
    print('\n')


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