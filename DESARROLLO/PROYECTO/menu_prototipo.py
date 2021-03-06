import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy
import os
import sys
from datetime import datetime


import functions as f
import bdd_functions as bbf
import n_grams_functions as ngf
import imputaciones_functions as imf
import outliers_functions as of
import main_primer_ingreso as mpi
import main_ingreso_n as minn

col_fal = []
col_sob = []

def resumen(col_string_nulls,col_string_dupli,cols_num_nulls,cols_num_outl):
	print("----Se encontraron y corrigieron valores nulos en las siguientes columnas tipo string: ")
	print(col_string_nulls)
	print("\n")
	print("----Se encontraron y corrigieron duplicados en las siguientes columnas: ")
	print(col_string_dupli)
	print("\n")
	print("----Se encontraron y corrigieron valores nulos en las siguientes columnas numéricas: ")
	print(cols_num_nulls)
	print("\n")
	print("----Se encontraron y corrigieron valores outliers en las siguientes columnas numéricas: ")
	print(cols_num_outl)
	print("\n")

def corrobora_columnas(diccionario,df_columns,columnas_faltantes,columnas_sobrantes):
	for i in df_columns:
		if(i not in diccionario):
			columnas_sobrantes.append(i)
	for j in diccionario:
		if (j not in df_columns):
			columnas_faltantes.append(j)

def corrobora_tipos(diccionario,df):
	ind = 0
	col_string_input = []
	col_bdd = []
	col_string_bdd = []
	for i in range(len(df.columns)):
		if(df[df.columns[i]].dtype == 'object'):
			col_string_input.append(df.columns[i]) #columnas string de la entrada
	#print("col_string conjunto de entrada: ", col_string_input)
	for j in range(len(diccionario["COLUMNAS"])):
		col_bdd.append(diccionario["COLUMNAS"][j]) #guardo todas las columnas del diccionario por orden
		if(diccionario["TYPES"][j] == 'object'):
			col_string_bdd.append(diccionario["COLUMNAS"][j]) #columnas string de la bdd
	for k in range(len(col_string_bdd)):
		if(col_string_bdd[k] in col_string_input):
			col_string_input.remove(col_string_bdd[k]) #se quitan las col string que deben serlo segun bdd
	#print("\n")
	#print("Columnas string en la entrada que no lo son en el la bdd: ", col_string_input)
	types_bdd = []
	types_input = []
	for l in range(len(col_string_input)):
		var = df[col_string_input[l]].dtype
		types_input.append(var)
	for m in range(len(diccionario["COLUMNAS"])):
		if(diccionario["COLUMNAS"][m] in col_string_input):
			var1 = diccionario["TYPES"][m]
			types_bdd.append(var1)
	for n in range(len(col_string_input)):
		print("La columna [{}], por contexto tiene el tipo de dato {}, pero en la entrada tiene el tipo {}, puede que existan datos de otro tipo en la columna, corregir el archivo y reprocesarlo.".format(col_string_input[n],types_bdd[n],types_input[n]))
		print("\n")
	if(len(col_string_input) > 0):
		ind = 1
	return ind


def principales(archivo, separador):
	df = f.dataframe_from_file_sep(archivo,separador)
	name_file = f.nombre_archivo(archivo)
	df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
	diccionario = bbf.columnas_df_bdd() #obtengo las columnas que tiene el diccionario de datos, las cuales deben coincidir con las del archivo de entrada
	return df,name_file,df_col_numericas,df_col_string, diccionario


if not os.path.exists("LOGS"):
	os.mkdir("LOGS")


print("\nBienvenido al prototipo v1 del 'Modelo predictivo de errores en los datos' \n")

ans = True
while ans:
	print("\n-----------------Menú--------------------------\n")
	print("Seleccione entre las opciones disponibles, el método de ingreso de archivo: \n")
	print("1 - archivo de extensión .csv")
	print("2 - archivo excel de extensión .xlsx")
	print("3 - nombre de tabla base de datos postgresql (la tabla debe estar en la misma bdd que el prototipo, esquema public)")
	print("4 - Mostrar contexto actual del prototipo")
	print("5 - **Resetear prototipo**")
	print("6 - para salir.")
	print("\n")
	ans = input("Ingrese la opción requerida: ")
	if(ans == "1"):
		archivo = input("Ingrese el archivo .csv: ")
		if os.path.exists(archivo):
			separador = input("Ingrese el separador del archivo .csv: ")
			df,name_file,df_col_numericas,df_col_string, diccionario = principales(archivo, separador)

			#-----------------------------MAIN--------------------------------------------------
			if(len(diccionario["COLUMNAS"]) <= 0):
				#REALIZAR PRIMER INGRESO DE DATOS
				print("\n----No se ha detectado un contexto para el prototipo, luego este se generará con los datos de esta primera entrada de datos.----\n")
				#------------------------------------main_primer_ingreso.py---------------------------------------------------------------------------

				now = datetime.now()
				date_time = now.strftime("%m-%d-%Y_%H_%M_%S")
				name_logfile = "LOG_" + date_time
				orig_stdout = sys.stdout

				f1le = open("LOGS/CONTEXTUALIZACION-{}.txt".format(name_logfile),'w')
				sys.stdout = f1le

				mpi.main_primer_ingreso(df, name_file)

				sys.stdout = orig_stdout
				f1le.close()

				#-------------------------------------------------------------------------------------------------------------------------------------
			elif(len(diccionario["COLUMNAS"]) > 0):
				corrobora_columnas(diccionario["COLUMNAS"], df.columns,col_fal,col_sob)
				#corrobora_columnas(diccionario["COLUMNAS"], exaple_list,col_fal,col_sob)
				print("COLUMNAS FALTANTES: ", col_fal)
				print("COLUMNAS SOBRANTES: ", col_sob)
				print("\n")

				if(len(col_fal) == 0 and len(col_sob) == 0):
					#SE AGREGA ENTRADA N DEL DATASET CORRESPONDIENTE AL CONTEXTO DEL PROTOTIPO
					print("Las columnas del dataset de entrada, concuerdan con el contexto del diccionario de datos. Se corregiran y cargaran los datos a la tabla histórica.\n\n")

					ind = corrobora_tipos(diccionario,df)
					if(ind == 0): 
				#------------------------------------main_ingreso.py----------------------------------------------------------------------------------
						now = datetime.now()
						date_time = now.strftime("%m-%d-%Y_%H_%M_%S")
						name_logfile = "LOG_" + date_time
						name_logfile2 = "LOGS/{}.txt".format(name_logfile)

						orig_stdout = sys.stdout
						f1le = open("LOGS/{}.txt".format(name_logfile),'w')
						sys.stdout = f1le

						csn,csd,cnn,cno = minn.ingreso_n_datos(df)

						sys.stdout = orig_stdout
						f1le.close()			

						resumen(csn,csd,cnn,cno)
						print("Para detalles de lo realizado revisar: {}".format(name_logfile2))

				#-------------------------------------------------------------------------------------------------------------------------------------
				else:
					#Lo que debería aparecer si es dataset no tiene los mismos nombres ni cantidad de columnas que los que se tienen registrados
					print("\n---El dataframe ingresado no posee las columnas del contexto ingresado previamente, las columnas del dataset ingresado son: ")
					print(df.columns,'\n')
					print("---Las columnas del contexto con el que se está trabajando son las siguientes: ")
					print(diccionario["COLUMNAS"])
					print("---Verifique que las columnas del dataset ingresado correspondan con las del contexto actual e ingrese nuevamente el dataset.")
			else:
				print("Ha ocurrido un error en detectar si el dataset se ingresa por primera vez o no.")
		else:
			print("La ruta {}, ingresada para el archivo de entrada no existe, ingresela nuevamente.".format(archivo))

	elif(ans == "2"):
		archivo = ''
		archivo = input("Ingrese el archivo .xlsx: ")
		if os.path.exists(archivo):			
			separador = ''
			df,name_file,df_col_numericas,df_col_string, diccionario = principales(archivo,separador)

			#-----------------------------MAIN--------------------------------------------------
			if(len(diccionario["COLUMNAS"]) <= 0):
				#REALIZAR PRIMER INGRESO DE DATOS
				print("No se ha detectado un contexto para el prototipo, luego este se generará con los datos de esta primera entrada de datos.")
				#------------------------------------main_primer_ingreso.py---------------------------------------------------------------------------

				now = datetime.now()
				date_time = now.strftime("%m-%d-%Y_%H_%M_%S")
				name_logfile = "LOG_" + date_time

				orig_stdout = sys.stdout
				f1le = open("LOGS/CONTEXTUALIZACION-{}.txt".format(name_logfile),'w')
				sys.stdout = f1le

				mpi.main_primer_ingreso(df, name_file)

				sys.stdout = orig_stdout
				f1le.close()

				#-------------------------------------------------------------------------------------------------------------------------------------
			elif(len(diccionario["COLUMNAS"]) > 0):
				corrobora_columnas(diccionario["COLUMNAS"], df.columns,col_fal,col_sob)
				#corrobora_columnas(diccionario["COLUMNAS"], exaple_list,col_fal,col_sob)
				print("COLUMNAS FALTANTES: ", col_fal)
				print("COLUMNAS SOBRANTES: ", col_sob)
				print("\n")
				if(len(col_fal) == 0 and len(col_sob) == 0):

					ind = corrobora_tipos(diccionario,df)
					if(ind == 0): 

						#SE AGREGA ENTRADA N DEL DATASET CORRESPONDIENTE AL CONTEXTO DEL PROTOTIPO
						print("Las columnas del dataset de entrada, concuerdan con el contexto del diccionario de datos. Se corregiran y cargaran los datos a la tabla histórica.\n\n")			#------------------------------------main_ingreso.py---------------------------------------------------------------------------

						now = datetime.now()
						date_time = now.strftime("%m-%d-%Y_%H_%M_%S")
						name_logfile = "LOG_" + date_time
						name_logfile2 = "LOGS/{}.txt".format(name_logfile)

						orig_stdout = sys.stdout
						f1le = open("LOGS/{}.txt".format(name_logfile),'w')
						sys.stdout = f1le

						csn,csd,cnn,cno = minn.ingreso_n_datos(df)

						sys.stdout = orig_stdout
						f1le.close()			

						resumen(csn,csd,cnn,cno)
						print("Para detalles de lo realizado revisar: {}".format(name_logfile2))
					
			#-------------------------------------------------------------------------------------------------------------------------------------
				else:
					#Lo que debería aparecer si es dataset no tiene los mismos nombres ni cantidad de columnas que los que se tienen registrados
					print("\n---El dataframe ingresado no posee las columnas del contexto ingresado previamente, las columnas del dataset ingresado son: ")
					print(df.columns,'\n')
					print("---Las columnas del contexto con el que se está trabajando son las siguientes: ")
					print(diccionario["COLUMNAS"])
					print("---Verifique que las columnas del dataset ingresado correspondan con las del contexto actual e ingrese nuevamente el dataset.")
			else:
				print("Ha ocurrido un error en detectar si el dataset se ingresa por primera vez o no.")
		else:
			print("La ruta {}, ingresada para el archivo de entrada no existe, ingresela nuevamente.".format(archivo))

	elif(ans == "3"):
		tabla = input("Ingrese el nombre de la tabla bdd postgresql de entrada: ")
		tablas = bbf.lista_tablas_bdd()
		if(tabla not in tablas):
			print("No se detectó la tabla {}. Intente nuevamente".format(tabla))
		elif(tabla in tablas):
			#comprobar que campos coincidan
			df = bbf.trae_tabla_bdd(tabla) # trae la tabla con el nombre ingresado ya que existe
			name_file = tabla
			df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
			diccionario = bbf.columnas_df_bdd() #obtengo las columnas que tiene el diccionario de datos, las cuales deben coincidir con el archivo de entrada

				#-----------------------------MAIN--------------------------------------------------
			if(len(diccionario["COLUMNAS"]) <= 0):
				#REALIZAR PRIMER INGRESO DE DATOS
				print("No se ha detectado un contexto para el prototipo, luego este se generará con los datos de esta primera entrada de datos.")
				#------------------------------------main_primer_ingreso.py---------------------------------------------------------------------------

				now = datetime.now()
				date_time = now.strftime("%m-%d-%Y_%H_%M_%S")
				name_logfile = "LOG_" + date_time

				orig_stdout = sys.stdout
				f1le = open("LOGS/CONTEXTUALIZACION-{}.txt".format(name_logfile),'w')
				sys.stdout = f1le

				mpi.main_primer_ingreso(df, name_file)

				sys.stdout = orig_stdout
				f1le.close()

				#-------------------------------------------------------------------------------------------------------------------------------------
			elif(len(diccionario["COLUMNAS"]) > 0):
				corrobora_columnas(diccionario["COLUMNAS"], df.columns,col_fal,col_sob)
				#corrobora_columnas(diccionario["COLUMNAS"], exaple_list,col_fal,col_sob)
				print("COLUMNAS FALTANTES: ", col_fal)
				print("COLUMNAS SOBRANTES: ", col_sob)
				print("\n")
				if(len(col_fal) == 0 and len(col_sob) == 0):

					ind = corrobora_tipos(diccionario,df)
					if(ind == 0): 

						#SE AGREGA ENTRADA N DEL DATASET CORRESPONDIENTE AL CONTEXTO DEL PROTOTIPO
						print("Las columnas del dataset de entrada, concuerdan con el contexto del diccionario de datos. Se corregiran y cargaran los datos a la tabla histórica.\n\n")			#------------------------------------main_ingreso.py---------------------------------------------------------------------------

						now = datetime.now()
						date_time = now.strftime("%m-%d-%Y_%H_%M_%S")
						name_logfile = "LOG_" + date_time
						name_logfile2 = "LOGS/{}.txt".format(name_logfile)

						orig_stdout = sys.stdout
						f1le = open("LOGS/{}.txt".format(name_logfile),'w')
						sys.stdout = f1le

						csn,csd,cnn,cno = minn.ingreso_n_datos(df)

						sys.stdout = orig_stdout
						f1le.close()			

						resumen(csn,csd,cnn,cno)
						print("Para detalles de lo realizado revisar: {}".format(name_logfile2))
					
			#-------------------------------------------------------------------------------------------------------------------------------------
				else:
					#Lo que debería aparecer si es dataset no tiene los mismos nombres ni cantidad de columnas que los que se tienen registrados
					print("\n---El dataframe ingresado no posee las columnas del contexto ingresado previamente, las columnas del dataset ingresado son: ")
					print(df.columns,'\n')
					print("---Las columnas del contexto con el que se está trabajando son las siguientes: ")
					print(diccionario["COLUMNAS"])
					print("---Verifique que las columnas del dataset ingresado correspondan con las del contexto actual e ingrese nuevamente el dataset.")
			else:
				print("Ha ocurrido un error en detectar si el dataset se ingresa por primera vez o no.")


		else:
			print("La tabla ingresada de nombre [{}], no existe en la base de datos. Intente nuevamente.".format(tabla))

	elif(ans == "4"):
		diccionario = bbf.columnas_df_bdd()
		if(len(diccionario["COLUMNAS"]) > 0):
			print("El contexto actual del prototipo contiene las siguientes {} columnas: \n".format(len(diccionario["COLUMNAS"])))
			for i in range(len(diccionario["COLUMNAS"])):
				print("Columna: [{}] - Tipo: [{}]".format(diccionario["COLUMNAS"][i],diccionario["TYPES"][i]))
			#print(diccionario["COLUMNAS"],diccionario["TYPES"])
		elif(len(diccionario["COLUMNAS"]) == 0):
			print("Actualmente no existe un contexto asociado al prototipo.\n")
		else:
			print("Algo salió mal al obtener el contexto del prototipo.\n")
		print("\n")

	elif(ans == "5"):
		ans2 = True
		while ans2:
			ans2 = input("¿Está seguro de resetar el prototipo? (y/n)")
			if(ans2 == "y" or ans2 == "Y"):
				bbf.resetear()
				print("\nLas tablas del prototipo han sido reseteadas. El proximo ingreso de datos se tomará como contexto.\n")
				ans2 = False
			elif(ans2 == "n" or ans2 == "N"):
				ans2 = False
			else:
				print("Ingrese un caracter válido (y/n)")


	elif(ans == "6"):
		print("Ha salido del programa.")
		ans = False
	elif (ans != ""):
		print("***Opción no válida, ingrese una opción válida***\n")

	col_fal = []
	col_sob = []