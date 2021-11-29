import numpy as numpy
import pandas as pd

import bdd_functions as bdf
import outliers_functions as of

#--------------NUMERICOS-----------------------
def imput_media(df,df_num,col_num_name,to_replace_val):
	df[col_num_name] = df[col_num_name].replace(to_replace = to_replace_val, value = round(df[col_num_name].mean(),2))
	df_num[col_num_name] = df_num[col_num_name].replace(to_replace = to_replace_val, value = round(df_num[col_num_name].mean(),2))

def input_mediana_outliers(df,df_num,col_num_name,to_replace_val):
	df[col_num_name] = df[col_num_name].replace(to_replace = to_replace_val, value = round(df[col_num_name].median(),2))
	df_num[col_num_name] = df_num[col_num_name].replace(to_replace = to_replace_val, value = round(df_num[col_num_name].median(),2))

def input_mediana_outliers_ing_n(df,df_num,col_num_name,to_replace_val,mediana):
	#indicador = bdf.extrae_ind_col_num(col_num_name)
	df[col_num_name] = df[col_num_name].replace(to_replace = to_replace_val, value = round(mediana,2))
	df_num[col_num_name] = df_num[col_num_name].replace(to_replace = to_replace_val, value = round(mediana,2))


def input_mediana(df,df_num,col_num_name):
	df[col_num_name] = df[col_num_name].fillna(df_num[col_num_name].median())
	df_num[col_num_name] = df_num[col_num_name].fillna(df_num[col_num_name].median())
	return df_num[col_num_name].median()

def input_media_2(df,df_num,col_num_name):
	df[col_num_name] = df[col_num_name].fillna(round(df_num[col_num_name].mean(),2))
	df_num[col_num_name] = df_num[col_num_name].fillna(round(df_num[col_num_name].mean(),2))
	return round(df_num[col_num_name].mean(),2)


#----------------------INPUTS DE MEDIA, MEDIANA, MODA PARA ENTRADA N, DEBE TOMAR LOS ESTADISTICOS DESDE LA BDD----------
	#NOTA: Si ingreso el estadístico en una columna cuyos valores están muy acotados y el estadístico es un outlier dentro de ese conjunto ingresado,
	#la tecnica de depuración toma solo los datos de entrada para el análisis por lo que podría ir detectando outliers que no lo son.
	#POSIBLE SOLUCIÓN, se podrían mezclar en un dataframe, los datos históricos para esa columna y analizar la mezcla de los datos de entrada con los del historico para detectar outliers

def input_media_ing_n(df,df_num,col_num_name):
	c1,c2 = bdf.conectarse()
	c2.execute("""
		SELECT "MODA", "MEDIA", "MEDIANA" FROM pruebas."DICCIONARIO_DE_DATOS" WHERE "NOM_COL" = '{v1}';
		""".format(v1 = col_num_name))
	for i in c2.fetchall():
		df[col_num_name] = df[col_num_name].fillna(round(i[1],2))
		df_num[col_num_name] = df_num[col_num_name].fillna(round(i[1],2))
		var = round(i[1],2)
	return var
	c2.close()

def input_mediana_ing_n(df,df_num,col_num_name):
	c1,c2 = bdf.conectarse()
	c2.execute("""
		SELECT "MODA", "MEDIA", "MEDIANA" FROM pruebas."DICCIONARIO_DE_DATOS" WHERE "NOM_COL" = '{v1}';
		""".format(v1 = col_num_name))
	for i in c2.fetchall():
		df[col_num_name] = df[col_num_name].fillna(round(i[2],2))
		df_num[col_num_name] = df_num[col_num_name].fillna(round(i[2],2))
		var = round(i[2],2)
	return var
	c2.close()

#-----------------------------------------------------------------------------------------------------------------------

'''

def input_df_numerico(df,df_num):
	for i in range(len(df_num.columns)):
		cur_col = round(df_num[df_num.columns[i]].kurt(),1) #curtosis
		count_null = df_num[df_num.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = of.inter_cuar_rang(df_num[df_num.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		porc_nulos = (count_null/cant_filas_df)*100

		print("Columna analizada: ", df_num.columns[i])
		print("Cant. nulos: ", count_null)
		#print(cant_filas_df)
		#print(porc_nulos)

		if(porc_nulos == 0):
			print("La columna [{}], no requiere tratamiento de nulos.".format(df_num.columns[i]))
		elif(porc_nulos <= 10 and porc_nulos > 0):
			print("La columna [{}], contiene un {}% de nulos, por lo que es tratable.".format(df_num.columns[i], porc_nulos))
			if(cur_col >= -3.0 and cur_col <=3.0):
				#SI LA COLUMNA CONTIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIANA - ESTE ESCENARIO SE ABORDA EN outliers_functions.py
				#SI LA COLUMNA NO TIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIA
				var = input_media_ing_n(df,df_num,df_num.columns[i])
				print("Esta columna posee una distribucion normal o cercana a normal, y CURTOSIS es {}".format(cur_col),", por lo que, se imputará por la media de la columna [{}].".format(var))
				#input_media_2(df,df_num,df_num.columns[i])
			else:
				#SE IMPUTA POR MEDIANA
				var2 = input_mediana_ing_n(df,df_num,df_num.columns[i])
				print("Esta columna no posee una distrib normal o cercana a normal, y su curtosis es {}".format(cur_col),", por lo que, se imputará por la mediana de la columna [{}].".format(var2))
				#input_mediana(df,df_num,df_num.columns[i])


		elif(porc_nulos > 10):
			print("La columna [{}], posee un {}% de valores nulos, se recomienda imputar valores hasta obtener menos del 10% de valores nulos para que el conjunto tenga un grado de credibilidad aceptable.".format(df_num.columns[i], porc_nulos))
			#break
		else:
			print('{},{}'.format(df_num.columns[i], porc_nulos))
			print("Se ha presentado un error en el proceso de detección de outliers.")
			break
		print('\n')


'''

def input_df_numerico(df,df_num):
	for i in range(len(df_num.columns)):
		cur_col = round(df_num[df_num.columns[i]].kurt(),1) #curtosis
		count_null = df_num[df_num.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = of.inter_cuar_rang(df_num[df_num.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		porc_nulos = (count_null/cant_filas_df)*100

		#----------------------28-11-2021---------
		indicadores = bdf.extrae_ind_col_num(df_num.columns[i])

		print("Columna analizada: ", df_num.columns[i])
		print("Cant. nulos: ", count_null)
		#print(cant_filas_df)
		#print(porc_nulos)

		if(indicadores[10] == '0'):			
			if(porc_nulos == 0):
				print("La columna [{}], no requiere tratamiento de nulos.".format(df_num.columns[i]))
			elif(porc_nulos <= 10 and porc_nulos > 0):
				print("La columna [{}], contiene un {}% de nulos, por lo que es tratable.".format(df_num.columns[i], porc_nulos))
				if(cur_col >= -3.0 and cur_col <=3.0):
					#SI LA COLUMNA CONTIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIANA - ESTE ESCENARIO SE ABORDA EN outliers_functions.py
					#SI LA COLUMNA NO TIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIA
					var = input_media_ing_n(df,df_num,df_num.columns[i])
					print("Esta columna posee una distribucion normal o cercana a normal, y CURTOSIS es {}".format(cur_col),", por lo que, se imputará por la media de la columna [{}].".format(var))
					#input_media_2(df,df_num,df_num.columns[i])
				else:
					#SE IMPUTA POR MEDIANA
					var2 = input_mediana_ing_n(df,df_num,df_num.columns[i])
					print("Esta columna no posee una distrib normal o cercana a normal, y su curtosis es {}".format(cur_col),", por lo que, se imputará por la mediana de la columna [{}].".format(var2))
					#input_mediana(df,df_num,df_num.columns[i])


			elif(porc_nulos > 10):
				print("La columna [{}], posee un {}% de valores nulos, se recomienda imputar valores hasta obtener menos del 10% de valores nulos para que el conjunto tenga un grado de credibilidad aceptable.".format(df_num.columns[i], porc_nulos))
				#break
			else:
				print('{},{}'.format(df_num.columns[i], porc_nulos))
				print("Se ha presentado un error en el proceso de detección de outliers.")
				break
		elif (indicadores[10] != '0'):
			print("La columna [{}], contiene en este ingreso {}% de nulos. Pero se ha especificado en el diccionario que no sean corregidos debido al contexto.".format(df_num.columns[i],porc_nulos))
		else:
			print("Algo ha salido mal con la corrección de nulos para esta columna.")
		print('\n')




def input_df_numerico_1ra_entrada(df,df_num):
	for i in range(len(df_num.columns)):
		cur_col = round(df_num[df_num.columns[i]].kurt(),1) #curtosis
		count_null = df_num[df_num.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = of.inter_cuar_rang(df_num[df_num.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		porc_nulos = (count_null/cant_filas_df)*100

		print("Columna analizada: ", df_num.columns[i])
		print("Cant. nulos: ", count_null)
		#print(cant_filas_df)
		#print(porc_nulos)

		if(porc_nulos == 0):
			print("La columna [{}], no requiere tratamiento de nulos.".format(df_num.columns[i]))
		elif(porc_nulos <= 10 and porc_nulos > 0):
			print("La columna [{}], contiene un {}% de nulos, por lo que es tratable.".format(df_num.columns[i], porc_nulos))
			if(cur_col >= -3.0 and cur_col <=3.0):
				#SI LA COLUMNA CONTIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIANA - ESTE ESCENARIO SE ABORDA EN outliers_functions.py
				#SI LA COLUMNA NO TIENE OUTLIERS, LOS NULOS SE IMPUTAN POR MEDIA
				var = input_media_2(df,df_num,df_num.columns[i])
				print("Esta columna posee una distribucion normal o cercana a normal, y su CURTOSIS es {}.".format(cur_col),", por lo que, se imputará por la media de la columna [{}].".format(var))

			else:
				#SE IMPUTA POR MEDIANA
				var2 = input_mediana(df,df_num,df_num.columns[i])
				print("Esta columna no posee una distribucion normal o cercana a normal, y su curtosis es {}.".format(cur_col),", por lo que, se imputará por la mediana de la columna [{}].".format(var2))



		elif(porc_nulos > 10):
			print("La columna [{}], posee un {}% de valores nulos, se recomienda imputar valores hasta obtener menos del 10% de valores nulos para que el conjunto tenga un grado de credibilidad aceptable.".format(df_num.columns[i], porc_nulos))
			#break
		else:
			print('{},{}'.format(df_num.columns[i], porc_nulos))
			print("Se ha presentado un error en el proceso de detección de outliers.")
			break
		print('\n')

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
		var = i[1]
	cx.close()
	return var


def imput_df_string(df,df_string):
	cant_filas_df = df.shape[0] #CANT. DE FILAS DEL DATAFRAME
	for i in range(len(df_string.columns)):
		count_null = df_string[df_string.columns[i]].isna().sum() #cant.nulos columna
		porc_nulos = (count_null/cant_filas_df)*100
		print("Columna analizada: {}".format(df_string.columns[i]))
		print("CANT. NULOS: ", count_null)
		if(porc_nulos == 0.0):
			#SI EL % DE NULOS ES 0%, LA COLUMNA NO REQUIERE TRATAMIENTO
			print("La columna {}, no requiere tratamiento de valores nulos, ya que tiene un {}% de valores nulos.".format(df_string.columns[i],porc_nulos))
			print("\n")
		elif(porc_nulos <= 10.0):
			#SI EL % DE NULOS ES <=10% SE REQUIERE TRATAMIENTO TIPO STRING, O SEA IMPUTACIÓN POR MODA O VALOR PREDEFINIDO
			var = imputar_col_string(df,df_string,df_string.columns[i])
			print("La columna [{}], será tratada, su porcentaje de nulos no supera el 10%, ya que es de {}%, se imputará por el valor moda de [{}]".format(df_string.columns[i],porc_nulos,var))
			print("\n")
		else:
			#SI EL % DE NULOS ES > 10%, NO SE REALIZARÁN MÁS ACCIONES SOBRE EL CONJUNTO YA QUE UNA COLUMNA POSEE UN NIVEL DE DATOS MUY POCO REPRESENTATIVO.
			print("La columna {}, posee un {}% de nulos, el cual supera el 10%, favor de ingresar un conjunto de datos que no supere este porcentaje de nulos en cualquiera de sus columnas.")
			#break #rompe el ciclo for

def imput_df_string_1ra_entrada(df,df_string):
	cant_filas_df = df.shape[0] #CANT. DE FILAS DEL DATAFRAME
	for i in range(len(df_string.columns)):
		count_null = df_string[df_string.columns[i]].isna().sum() #cant.nulos columna
		porc_nulos = round((count_null/cant_filas_df)*100,1)
		print("Columna analizada: {}".format(df_string.columns[i]))
		print("CANT. NULOS: ", count_null)
		if(porc_nulos == 0.0):
			#SI EL % DE NULOS ES 0%, LA COLUMNA NO REQUIERE TRATAMIENTO
			print("La columna [{}], no requiere tratamiento de valores nulos, ya que tiene un {}% de valores nulos.".format(df_string.columns[i],porc_nulos))
			print("\n")
		elif(porc_nulos <= 10.0):
			#SI EL % DE NULOS ES <=10% SE REQUIERE TRATAMIENTO TIPO STRING, O SEA IMPUTACIÓN POR MODA O VALOR PREDEFINIDO
			var = imputar_col_string(df,df_string,df_string.columns[i])
			print("La columna [{}], será tratada, su porcentaje de nulos no supera el 10%, ya que es de {}%, se imputará por el valor moda de [{}]".format(df_string.columns[i],porc_nulos,var))
			print("\n")
		else:
			#SI EL % DE NULOS ES > 10%, NO SE REALIZARÁN MÁS ACCIONES SOBRE EL CONJUNTO YA QUE UNA COLUMNA POSEE UN NIVEL DE DATOS MUY POCO REPRESENTATIVO.
			print("La columna [{}], posee un {}% de nulos, el cual supera el 10%, favor de ingresar un conjunto de datos que no supere este porcentaje de nulos en cualquiera de sus columnas.")
			#break #rompe el ciclo for

'''
def imput_n_grams(df,df_string,col_string_name,to_replace_val,new_value):
	df[df_string.columns[col_string_name]] = df[df_string.columns[col_string_name]].replace(to_replace = to_replace_val,  value = new_value)
	df_string[df_string.columns[col_string_name]] = df_string[df_string.columns[col_string_name]].replace(to_replace = to_replace_val,  value = new_value)

'''

def imput_string_new_val(ID,new_value):
	c3, cz = bdf.conectarse()
	cz.execute(""" insert into pruebas."UNIQUE_VALUES_STRING_COLUMNS"("ID_DICC_DATOS","VAL_UNICO") VALUES 
				('{v1}','{v2}'); COMMIT; """.format(v1 = ID , v2 = new_value))
	cz.close()
