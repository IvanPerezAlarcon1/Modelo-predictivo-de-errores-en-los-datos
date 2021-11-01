import pandas as pd
import os

import functions as f

archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_NGRAMS-test-2-cols--witherrors.csv'
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar

df = f.dataframe_from_file(archivo)

df_col_numericas,df_col_string = f.sep_col_string_and_num(df)

cant_filas_df = df_col_numericas.shape[0] #CANT. DE FILAS DEL DATAFRAME
cant_col_df = df_col_numericas.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
print("Cant. filas dataframe: ", cant_filas_df,"\n","Cant. columnas dataframe: ", cant_col_df,"\n")


print("Imputaciones para columnas STRING: ") #para columnas string, si debe ser el de la bdd el valor a imputar, ya que el usuario puede modificar este valor
print(df_col_string.columns)
for i in range(len(df_col_string.columns)):
	count_null = cont_null = df_col_string[df_col_string.columns[i]].isna().sum() #cant.nulos columna
	porc_nulos = round((cont_null/cant_filas_df)*100,1)
	print(df_col_string.columns[i], "CANT. NULLOS: ", count_null, "PORCENTAJE DE NULOS: {}%".format(porc_nulos))
	if(porc_nulos == 0.0):
		print("La columna {}, no requiere tratamiento de valores nulos, ya que tiene un {}% de valores nulos.".format(df_col_string.columns[i],porc_nulos))
		print("\n")
	if(porc_nulos <= 10.0):
		print("La columna {}, será tratada, su porcentaje de nulos no supera el 10%, ya que es de {}%".format(df_col_string.columns[i],porc_nulos))
		print("\n")
	else:
		print("La columna {}, posee un {}% de nulos, el cual supera el 10%, favor de ingresar un conjunto de datos que no supere este porcentaje de nulos en cualquiera de sus columnas.")
		break #rompe el ciclo for, no la iteracion solamente

#print("\n")
#print("Imputaciones para columnas NUMÉRICAS: ")
#print(df_col_numericas.columns)

