import pandas as pd
import os

import functions as f
import bdd_functions as bbf
import n_grams_functions as ngf
import imputaciones_functions as imf
import outliers_functions as of

#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_NGRAMS-test-2-cols--witherrors.csv'
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2-imput-manual-agent-col.csv' # se demora 2.8 seg en terminar

#df = f.dataframe_from_file(archivo)
#df_col_numericas,df_col_string = f.sep_col_string_and_num(df)

def ingreso_n_datos(df):
	df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
	diccionario = bbf.columnas_df_bdd() #obtengo las columnas que tiene el diccionario de datos, las cuales deben coincidir con el archivo de entrada

	#--------acciones sobre columnas strings----------
	imf.imput_df_string(df,df_col_string)
	ngf.revisar_string_cols_ing_n(df,df_col_string) #quita duplicados en las columnas string, agrega los que no se parecen a algun otor registro unico registado

	#--------acciones sobre columnas numéricas--------
	imf.input_df_numerico(df,df_col_numericas)
	of.sep_casos_ingreso_n(df,df_col_numericas)

	#falta hacer ingreso de datos a la tabla histórica final en el ingreso n
	bbf.insert_df_atabla(df)
	
	bbf.actualiza_dicc_datos()# actualiza los indicadores del diccionario de datos a partir de la tabla historica luego del nuevo ingreso de datos


#ingreso_n_datos(df)