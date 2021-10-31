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
#REVISAR, PARECE QUE SI RANGO INTER CUARTIL = 0 USAR TUKEY, SI ES != 0 SE USA GRUBBS
print("-----CARACTERISTICAS DE LAS COLUMNAS NUMERICAS PARA VER OUTLIERS Y NULOS-----\n\n")
for i in range(len(df_col_numericas.columns)):
	cur_col = round(df_col_numericas[df_col_numericas.columns[i]].kurt(),1)
	cont_null = df_col_numericas[df_col_numericas.columns[i]].isna().sum()
	print(df_col_numericas.columns[i], "- CURTOSIS: ", cur_col)
	print("FRECUENCIAS ",df_col_numericas.groupby(df_col_numericas.columns[i]).size())
	print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
	print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))

	#tukey
	probables_outliers, posibles_outliers = of.tukeys_method(df_col_numericas,df_col_numericas.columns[i])
	#print("PROBABLES OUTLIERS: ",probables_outliers)
	#print("POSIBLES_OUTLIERS",posibles_outliers)

	#grubbs
	#print("OUTLIERS MAXIMOS GRUBBS: ", grubbs.max_test_outliers(df_col_numericas[df_col_numericas.columns[i]], alpha = 0.05))
	#print("OUTLIERS MINIMOS GRUBBS: ", grubbs.min_test_outliers(df_col_numericas[df_col_numericas.columns[i]], alpha = 0.05))

	#of.ESD_Test(df_col_numericas[df_col_numericas.columns[i]],0.05,1,df,df_col_numericas,df_col_numericas.columns[i])
	#print("col despues trat. outliers: ", df_col_numericas[df_col_numericas.columns[i]].head(20)) #LA FUNCION NO ME CORRIGE EL VALOR QUE DEBERÍA
	#of.ESD_Test(df_col_numericas[df_col_numericas.columns[i]],0.05,1,df,df_col_numericas,df_col_numericas.columns[i])
	print("\n")

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

		#grubbs
		max_grubbs_outliers = grubbs.max_test_outliers(df_col_numericas[df_col_numericas.columns[i]], alpha = 0.05)
		min_grubbs_outliers = grubbs.min_test_outliers(df_col_numericas[df_col_numericas.columns[i]], alpha = 0.05)
		print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
		print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
		if(len(max_grubbs_outliers) > 0):
			for ma in max_grubbs_outliers:
				inp_f.imput_media(df,df_col_numericas,df_col_numericas.columns[i],ma)
		if(len(min_grubbs_outliers) > 0):
			for mi in min_grubbs_outliers:
					inp_f.imput_media(df,df_col_numericas,df_col_numericas.columns[i],mi)

		print("FRECUENCIAS ",df_col_numericas.groupby(df_col_numericas.columns[i]).size())
		#of.ESD_Test(df_col_numericas[df_col_numericas.columns[i]],0.05,1,df,df_col_numericas,df_col_numericas.columns[i])
		#print("col despues trat. outliers: ", df_col_numericas[df_col_numericas.columns[i]].head(20)) #LA FUNCION NO ME CORRIGE EL VALOR QUE DEBERÍA
		#of.ESD_Test(df_col_numericas[df_col_numericas.columns[i]],0.05,1,df,df_col_numericas,df_col_numericas.columns[i])
		print("\n")