import numpy as np
import pandas as pd
import scipy.stats as stats
from outliers import smirnov_grubbs as grubbs
import imputaciones_functions as inp_f
import bdd_functions as bdf

def inter_cuar_rang(df_num_col):
	q1 = df_num_col.quantile(0.25)
	q3 = df_num_col.quantile(0.75)
	iqr = q3-q1
	return iqr

#Tukey's method
def tukeys_method(df, variable):
	#Takes two parameters: dataframe & variable of interest as string
	q1 = df[variable].quantile(0.25) #Q1
	q3 = df[variable].quantile(0.75) #Q3
	iqr = q3-q1 #RANGO INTERCUARTIL
	inner_fence = 1.5*iqr
	outer_fence = 3*iqr
	
	#inner fence lower and upper end
	inner_fence_le = q1-inner_fence #LOWER_LIMIT
	inner_fence_ue = q3+inner_fence #UPPER_LIMIT
	
	#outer fence lower and upper end
	outer_fence_le = q1-outer_fence #LOWER_LIMIT
	outer_fence_ue = q3+outer_fence #UPPER_LIMIT
	print("Q1:{} // Q3: {} // IQR: {} // LIMITES INFERIORES ({},{}) // LIMITES SUPERIORES({},{})".format(q1,q3,iqr,outer_fence_le,inner_fence_le,inner_fence_ue,outer_fence_ue))
	outliers_prob = []
	outliers_poss = []
	for index, x in enumerate(df[variable]):
		if x <= outer_fence_le or x >= outer_fence_ue:
			#outliers_prob.append(index) #indice
			outliers_prob.append(x) #valor
	for index, x in enumerate(df[variable]):
		if x <= inner_fence_le or x >= inner_fence_ue:
			#outliers_poss.append(index)
			outliers_poss.append(x)
	return outliers_prob, outliers_poss

'''

def sep_casos(df, df_num_col):
	print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
	for i in range(len(df_num_col.columns)):
		cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
		cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = inter_cuar_rang(df_num_col[df_num_col.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		#PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
		if(cur_col >= -3.0 and cur_col <=3.0):
			print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
			print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
			#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
			#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
			print("IRQ: ", IRQ)

			#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
			if(IRQ != 0):
				#IRQ != 0 SE USA GRUBBS
				print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna [{}].".format(df_num_col[df_num_col.columns[i]].median()))
				max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
				min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
				#while que itera mediante grubbs hasta que deja de detectar outliers, los cuales son corregidos en el df
				while(len(max_grubbs_outliers) > 0 or len(min_grubbs_outliers) > 0):
					max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
					min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
					print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
					print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
					#en estos casos se debe imputar por la mediana, no por la media
					if(len(max_grubbs_outliers) > 0):
						for ma in max_grubbs_outliers:
							#inp_f.imput_media(df,df_num_col,df_num_col.columns[i],ma)
							inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],ma)

					if(len(min_grubbs_outliers) > 0):
						for mi in min_grubbs_outliers:
							#inp_f.imput_media(df,df_num_col,df_num_col.columns[i],mi)
							inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],mi)
			else:
				#--------------------------FALTA HACER IMPLEMENTACIÓN DE TUKEY-------01-11-2021-------------------------
				#SI IRQ = 0, SE USA TUKEY para detectar outliers, cambiando valores de outliers por, la MEDIANA
				print("Esta col, se debe analizar por método de Tukey, si se encuentran outliers, se corregiran por la mediana de la columna, [{}].".format(mediana))
				probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
				#while(len(probables_outliers) > 0 or len(posibles_outliers) > 0): #EN POSIBLES OUTLIERS APARECEN TANTO LOS PROBABLES COMO POSIBLES
				while(len(posibles_outliers) > 0):
					#probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
					#print("PROBABLES OUTLIERS: ",probables_outliers)
					print("OUTLIERS DETECTADOS",posibles_outliers)
					#if(len(probables_outliers) > 0):
					#	for po in probables_outliers:
					#		inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],po)
					if(len(posibles_outliers) > 0):
						for pos_o in posibles_outliers:
							inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],pos_o)
					probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])

			print("FRECUENCIAS - POST Correccion:",df_num_col.groupby(df_num_col.columns[i]).size())
			print('\n')
		else:
			print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))

'''



def sep_casos(df, df_num_col):
	print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
	for i in range(len(df_num_col.columns)):
		cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
		cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = inter_cuar_rang(df_num_col[df_num_col.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		#PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
		ind_col_num_bdd = bdf.extrae_ind_col_num(df_num_col.columns[i]) #extrae indicadores almacenados para la columna numerica
		if(cur_col >= -3.0 and cur_col <=3.0):
			print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
			print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
			#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
			#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
			print("IRQ: ", IRQ)

			#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
			if(IRQ != 0):
				#IRQ != 0 SE USA GRUBBS
				print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna [{}].".format(df_num_col[df_num_col.columns[i]].median()))
				max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
				min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
				#while que itera mediante grubbs hasta que deja de detectar outliers, los cuales son corregidos en el df
				print("Outliers detectados por prueba de Grubbs para la columna [{}], en este conjunto de entrada de datos.".format(df_num_col.columns[i]))
				while(len(max_grubbs_outliers) > 0 or len(min_grubbs_outliers) > 0):
					max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
					min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
					print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
					print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
					#en estos casos se debe imputar por la mediana, no por la media
					if(len(max_grubbs_outliers) > 0):
						for ma in max_grubbs_outliers:
							#inp_f.imput_media(df,df_num_col,df_num_col.columns[i],ma)
							inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],ma)

					if(len(min_grubbs_outliers) > 0):
						for mi in min_grubbs_outliers:
							#inp_f.imput_media(df,df_num_col,df_num_col.columns[i],mi)
							inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],mi)
			else:
				#--------------------------FALTA HACER IMPLEMENTACIÓN DE TUKEY-------01-11-2021-------------------------
				#SI IRQ = 0, SE USA TUKEY para detectar outliers, cambiando valores de outliers por, la MEDIANA
				print("Esta col, se debe analizar por método de Tukey, si se encuentran outliers, se corregiran por la mediana de la columna, [{}].".format(df_num_col[df_num_col.columns[i]].median()))
				probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
				#while(len(probables_outliers) > 0 or len(posibles_outliers) > 0): #EN POSIBLES OUTLIERS APARECEN TANTO LOS PROBABLES COMO POSIBLES
				while(len(posibles_outliers) > 0):
					#probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
					#print("PROBABLES OUTLIERS: ",probables_outliers)
					print("OUTLIERS DETECTADOS",posibles_outliers)
					#if(len(probables_outliers) > 0):
					#	for po in probables_outliers:
					#		inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],po)
					if(len(posibles_outliers) > 0):
						for pos_o in posibles_outliers:
							inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],pos_o)
					probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])

			print("VALORES y FRECUENCIAS FINALES Columna:",df_num_col.groupby(df_num_col.columns[i]).size())
			print('\n')
		else:
			print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))



def sep_casos_ingreso_n(df, df_num_col):
	cols_num_outl = []
	print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
	df_aux = df.copy()
	df_num_col_aux = df_num_col.copy()
	for i in range(len(df_num_col.columns)):
		#INDICADORES DE LA COLUMNA DESDE EL DF INGRESADO EN LA ENTRADA
		cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
		cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = inter_cuar_rang(df_num_col[df_num_col.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		#PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
		#----------------------13-11-2021---------
		#INDICADORES DE LA COLUMNA DESDE LA BDD
		val_max = df_num_col[df_num_col.columns[i]].max()
		val_min = df_num_col[df_num_col.columns[i]].min()
		mediana = df_num_col[df_num_col.columns[i]].median()
		ind_col_num_bdd = bdf.extrae_ind_col_num(df_num_col.columns[i]) #extrae indicadores almacenados para la columna numerica
		if(ind_col_num_bdd[9] == '0'):

			if (val_max > ind_col_num_bdd[3] or val_min < ind_col_num_bdd[2]):
				outliers_up = []
				outliers_down = []
				if(cur_col >= -3.0 and cur_col <=3.0):
					print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
					print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
					#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
					#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
					print("IRQ: ", IRQ)

					#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
					if(IRQ != 0):
						#IRQ != 0 SE USA GRUBBS
						print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna [{}].".format(mediana))
						max_grubbs_outliers = grubbs.max_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
						min_grubbs_outliers = grubbs.min_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
						#while que itera mediante grubbs hasta que deja de detectar outliers, los cuales son corregidos en el df
						while(len(max_grubbs_outliers) > 0 or len(min_grubbs_outliers) > 0):
							max_grubbs_outliers = grubbs.max_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
							min_grubbs_outliers = grubbs.min_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
							print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
							print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
							#en estos casos se debe imputar por la mediana, no por la media
							if(len(max_grubbs_outliers) > 0):
								for ma in max_grubbs_outliers:
									outliers_up.append(ma)
									inp_f.input_mediana_outliers(df_aux,df_num_col_aux,df_num_col_aux.columns[i],ma)
									#inp_f.input_mediana_outliers_ing_n(df,df_num_col,df_num_col.columns[i],ma,indicadores[7]) #no funciona
							if(len(min_grubbs_outliers) > 0):
								for mi in min_grubbs_outliers:
									outliers_down.append(mi)
									inp_f.input_mediana_outliers(df_aux,df_num_col_aux,df_num_col_aux.columns[i],mi)
						print("Outliers fuera del contexto corregidos efectivamente")
						corregidos = []
						#print(np.unique(outliers_up))
						#print(np.unique(outliers_down))
						for u in np.unique(outliers_up):
							if (u > ind_col_num_bdd[3] or u < ind_col_num_bdd[2]):
								corregidos.append(u)
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],u)
						for d in np.unique(outliers_down):
							if(d > ind_col_num_bdd[3] or d < ind_col_num_bdd[2]):
								corregidos.append(d)
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],d)
						print(corregidos)
						if(len(corregidos) > 0):
							cols_num_outl.append(df_num_col.columns[i])
						#AHORA LUEGO DE ESTAS VALIDACIONES SE PODRIA AGREGAR UNA CORRECCION DE LOS VALORES QUE DIRECTAMENTE ESTAN FUERA DEL RANGO PERMITIDO EN LA COLUMNA


					else:
						#--------------------------FALTA HACER IMPLEMENTACIÓN DE TUKEY-------01-11-2021-------------------------
						#SI IRQ = 0, SE USA TUKEY para detectar outliers, cambiando valores de outliers por, la MEDIANA
						print("Esta col, se debe analizar por método de Tukey, si se encuentran outliers, se corregiran por la mediana de la columna, [{}].".format(mediana))
						probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
						#while(len(probables_outliers) > 0 or len(posibles_outliers) > 0): #EN POSIBLES OUTLIERS APARECEN TANTO LOS PROBABLES COMO POSIBLES
						while(len(posibles_outliers) > 0):
							#probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
							#print("PROBABLES OUTLIERS: ",probables_outliers)
							print("OUTLIERS DETECTADOS",posibles_outliers)
							#if(len(probables_outliers) > 0):
							#	for po in probables_outliers:
							#		inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],po)
							if(len(posibles_outliers) > 0):
								for pos_o in posibles_outliers:
									inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],pos_o)
							probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])

					print("FRECUENCIAS - POST Correccion:",df_num_col.groupby(df_num_col.columns[i]).size())
					print('\n')
				else:
					print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))

			elif(val_max <= ind_col_num_bdd[3] and val_min >= ind_col_num_bdd[2]):
				print("Los valores máximo y mínimo de la columna [{}] del conjunto de entrada MAX: {} y MIN: {}, están dentro de los rangos definidos en el primer ingreso MAX: {} y MIN: {}. Esta columna no requiere corrección de outliers.".format(df_num_col.columns[i], val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2]))
				#break
			else:
				print("HA OCURRIDO UN ERROR EN LA DETECCION DE OUTLIERS EN LA COLUMNA [{}].".format(df_num_col.columns[i]))
				print(val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2])
				#break
		else:
			print("Se ha especificado por diccionario, que la columna [{}], admita valores outliers, por lo que no serán corregidos".format(df_num_col.columns[i]))
	return cols_num_outl



'''

#--FUNCIONAL PERO NO RETORNA LAS COLUMNAS EFECTIVAMENTE CORREGIDAS EN TERMINOS DE OUTLIERS
#caso en que las herramientas de outliers detectan los outliers y corrigen solo los que están fuera de los rangos del contexto
def sep_casos_ingreso_n(df, df_num_col):
	print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
	df_aux = df.copy()
	df_num_col_aux = df_num_col.copy()
	for i in range(len(df_num_col.columns)):
		#INDICADORES DE LA COLUMNA DESDE EL DF INGRESADO EN LA ENTRADA
		cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
		cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = inter_cuar_rang(df_num_col[df_num_col.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		#PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
		#----------------------13-11-2021---------
		#INDICADORES DE LA COLUMNA DESDE LA BDD
		val_max = df_num_col[df_num_col.columns[i]].max()
		val_min = df_num_col[df_num_col.columns[i]].min()
		mediana = df_num_col[df_num_col.columns[i]].median()
		ind_col_num_bdd = bdf.extrae_ind_col_num(df_num_col.columns[i]) #extrae indicadores almacenados para la columna numerica
		if(ind_col_num_bdd[9] == '0'):

			if (val_max > ind_col_num_bdd[3] or val_min < ind_col_num_bdd[2]):
				outliers_up = []
				outliers_down = []
				if(cur_col >= -3.0 and cur_col <=3.0):
					print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
					print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
					#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
					#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
					print("IRQ: ", IRQ)

					#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
					if(IRQ != 0):
						#IRQ != 0 SE USA GRUBBS
						print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna [{}].".format(mediana))
						max_grubbs_outliers = grubbs.max_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
						min_grubbs_outliers = grubbs.min_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
						#while que itera mediante grubbs hasta que deja de detectar outliers, los cuales son corregidos en el df
						while(len(max_grubbs_outliers) > 0 or len(min_grubbs_outliers) > 0):
							max_grubbs_outliers = grubbs.max_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
							min_grubbs_outliers = grubbs.min_test_outliers(df_num_col_aux[df_num_col_aux.columns[i]], alpha = 0.05)
							print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
							print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
							#en estos casos se debe imputar por la mediana, no por la media
							if(len(max_grubbs_outliers) > 0):
								for ma in max_grubbs_outliers:
									outliers_up.append(ma)
									inp_f.input_mediana_outliers(df_aux,df_num_col_aux,df_num_col_aux.columns[i],ma)
									#inp_f.input_mediana_outliers_ing_n(df,df_num_col,df_num_col.columns[i],ma,indicadores[7]) #no funciona
							if(len(min_grubbs_outliers) > 0):
								for mi in min_grubbs_outliers:
									outliers_down.append(mi)
									inp_f.input_mediana_outliers(df_aux,df_num_col_aux,df_num_col_aux.columns[i],mi)
						print("Outliers fuera del contexto corregidos efectivamente")
						corregidos = []
						#print(np.unique(outliers_up))
						#print(np.unique(outliers_down))
						for u in np.unique(outliers_up):
							if (u > ind_col_num_bdd[3] or u < ind_col_num_bdd[2]):
								corregidos.append(u)
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],u)
						for d in np.unique(outliers_down):
							if(d > ind_col_num_bdd[3] or d < ind_col_num_bdd[2]):
								corregidos.append(d)
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],d)
						print(corregidos)
						#AHORA LUEGO DE ESTAS VALIDACIONES SE PODRIA AGREGAR UNA CORRECCION DE LOS VALORES QUE DIRECTAMENTE ESTAN FUERA DEL RANGO PERMITIDO EN LA COLUMNA


					else:
						#--------------------------FALTA HACER IMPLEMENTACIÓN DE TUKEY-------01-11-2021-------------------------
						#SI IRQ = 0, SE USA TUKEY para detectar outliers, cambiando valores de outliers por, la MEDIANA
						print("Esta col, se debe analizar por método de Tukey, si se encuentran outliers, se corregiran por la mediana de la columna, [{}].".format(mediana))
						probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
						#while(len(probables_outliers) > 0 or len(posibles_outliers) > 0): #EN POSIBLES OUTLIERS APARECEN TANTO LOS PROBABLES COMO POSIBLES
						while(len(posibles_outliers) > 0):
							#probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
							#print("PROBABLES OUTLIERS: ",probables_outliers)
							print("OUTLIERS DETECTADOS",posibles_outliers)
							#if(len(probables_outliers) > 0):
							#	for po in probables_outliers:
							#		inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],po)
							if(len(posibles_outliers) > 0):
								for pos_o in posibles_outliers:
									inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],pos_o)
							probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])

					print("FRECUENCIAS - POST Correccion:",df_num_col.groupby(df_num_col.columns[i]).size())
					print('\n')
				else:
					print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))

			elif(val_max <= ind_col_num_bdd[3] and val_min >= ind_col_num_bdd[2]):
				print("Los valores máximo y mínimo de la columna [{}] del conjunto de entrada MAX: {} y MIN: {}, están dentro de los rangos definidos en el primer ingreso MAX: {} y MIN: {}. Esta columna no requiere corrección de outliers.".format(df_num_col.columns[i], val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2]))
				#break
			else:
				print("HA OCURRIDO UN ERROR EN LA DETECCION DE OUTLIERS EN LA COLUMNA [{}].".format(df_num_col.columns[i]))
				print(val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2])
				#break
		else:
			print("Se ha especificado por diccionario, que la columna [{}], admita valores outliers, por lo que no serán corregidos".format(df_num_col.columns[i]))

'''

'''

#----------ya funcional con correccion por grubbs - respaldo para hacer pruebas con tukey


def sep_casos_ingreso_n(df, df_num_col):
	print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
	for i in range(len(df_num_col.columns)):
		#INDICADORES DE LA COLUMNA DESDE EL DF INGRESADO EN LA ENTRADA
		cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
		cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = inter_cuar_rang(df_num_col[df_num_col.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		#PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
		#----------------------13-11-2021---------
		#INDICADORES DE LA COLUMNA DESDE LA BDD
		val_max = df_num_col[df_num_col.columns[i]].max()
		val_min = df_num_col[df_num_col.columns[i]].min()
		mediana = df_num_col[df_num_col.columns[i]].median()
		ind_col_num_bdd = bdf.extrae_ind_col_num(df_num_col.columns[i]) #extrae indicadores almacenados para la columna numerica
		if(ind_col_num_bdd[9] == '0'):

			if (val_max > ind_col_num_bdd[3] or val_min < ind_col_num_bdd[2]):

				if(cur_col >= -3.0 and cur_col <=3.0):
					print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
					print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
					#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
					#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
					print("IRQ: ", IRQ)

					#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
					if(IRQ != 0):
						#IRQ != 0 SE USA GRUBBS
						print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna [{}].".format(mediana))
						max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
						min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
						#while que itera mediante grubbs hasta que deja de detectar outliers, los cuales son corregidos en el df
						while(len(max_grubbs_outliers) > 0 or len(min_grubbs_outliers) > 0):
							max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
							min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
							print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
							print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
							#en estos casos se debe imputar por la mediana, no por la media
							if(len(max_grubbs_outliers) > 0):
								for ma in max_grubbs_outliers:
									inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],ma)
									#inp_f.input_mediana_outliers_ing_n(df,df_num_col,df_num_col.columns[i],ma,indicadores[7]) #no funciona
							if(len(min_grubbs_outliers) > 0):
								for mi in min_grubbs_outliers:
									inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],mi)
									#inp_f.input_mediana_outliers_ing_n(df,df_num_col,df_num_col.columns[i],ma,indicadores[7]) #no funciona
					else:
						#--------------------------FALTA HACER IMPLEMENTACIÓN DE TUKEY-------01-11-2021-------------------------
						#SI IRQ = 0, SE USA TUKEY para detectar outliers, cambiando valores de outliers por, la MEDIANA
						print("Esta col, se debe analizar por método de Tukey, si se encuentran outliers, se corregiran por la mediana de la columna, [{}].".format(mediana))
						probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
						#while(len(probables_outliers) > 0 or len(posibles_outliers) > 0): #EN POSIBLES OUTLIERS APARECEN TANTO LOS PROBABLES COMO POSIBLES
						while(len(posibles_outliers) > 0):
							#probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
							#print("PROBABLES OUTLIERS: ",probables_outliers)
							print("OUTLIERS DETECTADOS",posibles_outliers)
							#if(len(probables_outliers) > 0):
							#	for po in probables_outliers:
							#		inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],po)
							if(len(posibles_outliers) > 0):
								for pos_o in posibles_outliers:
									inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],pos_o)
							probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])

					print("FRECUENCIAS - POST Correccion:",df_num_col.groupby(df_num_col.columns[i]).size())
					print('\n')
				else:
					print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))

			elif(val_max <= ind_col_num_bdd[3] and val_min >= ind_col_num_bdd[2]):
				print("Los valores máximo y mínimo de la columna [{}] del conjunto de entrada MAX: {} y MIN: {}, están dentro de los rangos definidos en el primer ingreso MAX: {} y MIN: {}. Esta columna no requiere corrección de outliers.".format(df_num_col.columns[i], val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2]))
				#break
			else:
				print("HA OCURRIDO UN ERROR EN LA DETECCION DE OUTLIERS EN LA COLUMNA [{}].".format(df_num_col.columns[i]))
				print(val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2])
				#break
		else:
			print("Se ha especificado por diccionario, que la columna [{}], admita valores outliers, por lo que no serán corregidos".format(df_num_col.columns[i]))

'''



'''
#---------codigo sin corroborar indicador para corregir outliers
def sep_casos_ingreso_n(df, df_num_col):
	print("---------COLUMNAS CON CURTOSIS ENTRE [-3,3], DEL DF DE ENTRADA--------\n\n")
	for i in range(len(df_num_col.columns)):
		#INDICADORES DE LA COLUMNA DESDE EL DF INGRESADO EN LA ENTRADA
		cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
		cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
		cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
		cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
		IRQ = inter_cuar_rang(df_num_col[df_num_col.columns[i]]) #RANGO INTERCUARTIL DE LA COLUMNA
		#PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
		#----------------------13-11-2021---------
		#INDICADORES DE LA COLUMNA DESDE LA BDD
		val_max = df_num_col[df_num_col.columns[i]].max()
		val_min = df_num_col[df_num_col.columns[i]].min()
		mediana = df_num_col[df_num_col.columns[i]].median()
		ind_col_num_bdd = bdf.extrae_ind_col_num(df_num_col.columns[i]) #extrae indicadores almacenados para la columna numerica
		if (val_max > ind_col_num_bdd[3] or val_min < ind_col_num_bdd[2]):

			if(cur_col >= -3.0 and cur_col <=3.0):
				print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
				print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
				#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
				#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
				print("IRQ: ", IRQ)

				#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
				if(IRQ != 0):
					#IRQ != 0 SE USA GRUBBS
					print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna [{}].".format(mediana))
					max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
					min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
					#while que itera mediante grubbs hasta que deja de detectar outliers, los cuales son corregidos en el df
					while(len(max_grubbs_outliers) > 0 or len(min_grubbs_outliers) > 0):
						max_grubbs_outliers = grubbs.max_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
						min_grubbs_outliers = grubbs.min_test_outliers(df_num_col[df_num_col.columns[i]], alpha = 0.05)
						print("OUTLIERS MAXIMOS GRUBBS: ", max_grubbs_outliers)
						print("OUTLIERS MINIMOS GRUBBS: ", min_grubbs_outliers)
						#en estos casos se debe imputar por la mediana, no por la media
						if(len(max_grubbs_outliers) > 0):
							for ma in max_grubbs_outliers:
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],ma)
								#inp_f.input_mediana_outliers_ing_n(df,df_num_col,df_num_col.columns[i],ma,indicadores[7]) #no funciona
						if(len(min_grubbs_outliers) > 0):
							for mi in min_grubbs_outliers:
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],mi)
								#inp_f.input_mediana_outliers_ing_n(df,df_num_col,df_num_col.columns[i],ma,indicadores[7]) #no funciona
				else:
					#--------------------------FALTA HACER IMPLEMENTACIÓN DE TUKEY-------01-11-2021-------------------------
					#SI IRQ = 0, SE USA TUKEY para detectar outliers, cambiando valores de outliers por, la MEDIANA
					print("Esta col, se debe analizar por método de Tukey, si se encuentran outliers, se corregiran por la mediana de la columna, [{}].".format(mediana))
					probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
					#while(len(probables_outliers) > 0 or len(posibles_outliers) > 0): #EN POSIBLES OUTLIERS APARECEN TANTO LOS PROBABLES COMO POSIBLES
					while(len(posibles_outliers) > 0):
						#probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])
						#print("PROBABLES OUTLIERS: ",probables_outliers)
						print("OUTLIERS DETECTADOS",posibles_outliers)
						#if(len(probables_outliers) > 0):
						#	for po in probables_outliers:
						#		inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],po)
						if(len(posibles_outliers) > 0):
							for pos_o in posibles_outliers:
								inp_f.input_mediana_outliers(df,df_num_col,df_num_col.columns[i],pos_o)
						probables_outliers, posibles_outliers = tukeys_method(df_num_col,df_num_col.columns[i])

				print("FRECUENCIAS - POST Correccion:",df_num_col.groupby(df_num_col.columns[i]).size())
				print('\n')
			else:
				print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))

		elif(val_max <= ind_col_num_bdd[3] and val_min >= ind_col_num_bdd[2]):
			print("Los valores máximo y mínimo de la columna [{}] del conjunto de entrada MAX: {} y MIN: {}, están dentro de los rangos definidos en el primer ingreso MAX: {} y MIN: {}. Esta columna no requiere corrección de outliers.".format(df_num_col.columns[i], val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2]))
			#break
		else:
			print("HA OCURRIDO UN ERROR EN LA DETECCION DE OUTLIERS EN LA COLUMNA [{}].".format(df_num_col.columns[i]))
			print(val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2])
			#break


'''
