import pandas as pd
import os

import functions as f
import bdd_functions as bdf
import imputaciones_functions as imf
import n_grams_functions as ngf
import outliers_functions as of

archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar

#df = f.dataframe_from_file(archivo)
#name_file = f.nombre_archivo(archivo)

def main_primer_ingreso(df,name_file):
	df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
	#primer ingreso, se deben tener indicadores para poder realizar la depuracion a la primera entrada de datos
	bdf.insert_indic_bdd(df,df_col_string,df_col_numericas) #inserta indicadores al diccionario
	df_bdd_cols = bdf.columnas_df_bdd() #extrae las columnas que posee el diccionario de datos ya contextualizado
	bdf.insert_unique_values_string(df_bdd_cols,df_col_string) #inserta valores unicos para columnas tipo string en la tabla UNIQUE_VALUES_STRING_COLUMNS

	#--------acciones sobre columnas strings----------

	imf.imput_df_string_1ra_entrada(df,df_col_string)
	ngf.revisar_string_cols(df,df_col_string) #quita duplicados en las columnas string, agrega los que no se parecen a algun otro registro unico registado

	#--------acciones sobre columnas numéricas--------

	imf.input_df_numerico_1ra_entrada(df,df_col_numericas)
	of.sep_casos(df,df_col_numericas)

	#Crea tabla historica y la pobla con los datos depurados del dataframe de entrada
	bdf.crea_tabla_historica(df)

#llamada a funcion, si funciona primer ingreso
#main_primer_ingreso(df,name_file)