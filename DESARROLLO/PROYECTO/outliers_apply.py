import pandas as pd
import os
from outliers import smirnov_grubbs as grubbs

import functions as f
import bdd_functions as bdf
import n_grams_functions as ngf
import outliers_functions as of
import imputaciones_functions as inp_f



archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_NGRAMS-test-2-cols--witherrors.csv'
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar

#------------------------MAIN------------------------------
df = f.dataframe_from_file(archivo)

df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
print(df_col_numericas.columns)

cant_filas_df = df_col_numericas.shape[0] #CANT. DE FILAS DEL DATAFRAME
cant_col_df = df_col_numericas.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
print("Cant. filas dataframe: ", cant_filas_df,"\n","Cant. columnas dataframe: ", cant_col_df,"\n")
#print(df_col_numericas['is_canceled'])
'''
print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
for i in range(len(df_col_numericas.columns)):
	cur_col = round(df_col_numericas[df_col_numericas.columns[i]].kurt(),1)
	cont_null = df_col_numericas[df_col_numericas.columns[i]].isna().sum()
	#print(df_col_numericas.columns[i], "- CURTOSIS: ", cur_col)
	if(cur_col >= -3.0 and cur_col <=3.0):
		print(df_col_numericas.columns[i], "- CURTOSIS: ", cur_col)
		print("FRECUENCIAS ",df_col_numericas.groupby(df_col_numericas.columns[i]).size())
		print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
		print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))

#TUKEY: IMPORTANTE PARA ESTABLECER SU EFECTIVIDAD, SI EL RANGO INTER CUARTIL ES = 0, TODOS LOS VALORES DEL CONJUNTO, DISTINTOS DE CERO, SERÁN CATALOGADOS COMOA TÍPICOS
		#tukey
		probables_outliers, posibles_outliers = of.tukeys_method(df_col_numericas,df_col_numericas.columns[i])
		#print("PROBABLES OUTLIERS: ",probables_outliers)
		#print("POSIBLES_OUTLIERS",posibles_outliers)
'''
print("--------------------FRECUENCIAS PRE-CORRECCION----------------")
for i in range(len(df_col_numericas.columns)):
	print("FRECUENCIAS PRE:",df_col_numericas.groupby(df_col_numericas.columns[i]).size())

of.sep_casos(df,df_col_numericas)

print("--------------------FRECUENCIAS POST-CORRECCION----------------")
for i in range(len(df_col_numericas.columns)):
	print("FRECUENCIAS POST:",df_col_numericas.groupby(df_col_numericas.columns[i]).size())
print("\n")