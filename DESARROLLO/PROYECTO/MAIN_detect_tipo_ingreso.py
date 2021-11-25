# Se busca diferencias entre la primera entrada de un dataframe para poder contextualizarlo, con respecto a la entrada n

import pandas as pd
import os

import functions as f
import bdd_functions as bbf
import n_grams_functions as ngf
import imputaciones_functions as imf
import outliers_functions as of
import main_primer_ingreso as mpi
import main_ingreso_n as minn

#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.csv' # --> USADO PARA PRIMER INGRESO

#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\DATASETS PRUEBAS\hotel_bookings_25000 - errores string.csv' #errores string

#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\DATASETS PRUEBAS\hotel_bookings_25000 ERROR_OUTLIERS.csv' #errores outliers
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\DATASETS PRUEBAS\hotel_bookings_150 ERROR_OUTLIERS.csv' #errores outliers que deben detectarse por dixon

#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\DATASETS PRUEBAS\hotel_bookings_25000 - NULLS CORRECCION.csv'



col_fal = []
col_sob = []

def corrobora_columnas(diccionario,df_columns,columnas_faltantes,columnas_sobrantes):
	for i in df_columns:
		if(i not in diccionario):
			columnas_sobrantes.append(i)
	for j in diccionario:
		if (j not in df_columns):
			columnas_faltantes.append(j)


df = f.dataframe_from_file(archivo)
name_file = f.nombre_archivo(archivo)
df_col_numericas,df_col_string = f.sep_col_string_and_num(df)

diccionario = bbf.columnas_df_bdd() #obtengo las columnas que tiene el diccionario de datos, las cuales deben coincidir con el archivo de entrada
#example_list = ['col1','col2']


#-----------------------------MAIN--------------------------------------------------
if(len(diccionario["COLUMNAS"]) <= 0):
	#REALIZAR PRIMER INGRESO DE DATOS
	print("No se ha detectado un contexto para el prototipo, luego este se generará con los datos de esta primera entrada de datos.")
#------------------------------------main_primer_ingreso.py---------------------------------------------------------------------------
	mpi.main_primer_ingreso(df, name_file)
#-------------------------------------------------------------------------------------------------------------------------------------
elif(len(diccionario["COLUMNAS"]) > 0):
	corrobora_columnas(diccionario["COLUMNAS"], df.columns,col_fal,col_sob)
	#corrobora_columnas(diccionario["COLUMNAS"], exaple_list,col_fal,col_sob)
	print("COLUMNAS FALTANTES: ", col_fal)
	print("COLUMNAS SOBRANTES: ", col_sob)
	if(len(col_fal) == 0 and len(col_sob) == 0):
		#SE AGREGA ENTRADA N DEL DATASET CORRESPONDIENTE AL CONTEXTO DEL PROTOTIPO
		print("Se ha detectado correctamente la estructura del dataset, concuerda con el contexto del diccionario de datos. Se corregiran y cargaran los datos a la tabla histórica.")
#------------------------------------main_ingreso.py---------------------------------------------------------------------------
		minn.ingreso_n_datos(df)
#-------------------------------------------------------------------------------------------------------------------------------------
	else:
		#Lo que debería aparecer si es dataset no tiene los mismos nombres ni cantidad de columnas que los que se tienen registrados
		print("---El dataframe ingresado no posee las características del contexto ingresado previamente, las columnas del dataset ingresado son: ")
		print(df.columns,'\n')
		print("---Las columnas del contexto con el que se está trabajando son las siguientes: ")
		print(diccionario["COLUMNAS"])
		print("---Verifique que las columnas del dataset ingresado correspondan con las del contexto actual e ingrese nuevamente el dataset.")
else:
	print("Ha ocurrido un error en detectar si el dataset se ingresa por primera vez o no.")






