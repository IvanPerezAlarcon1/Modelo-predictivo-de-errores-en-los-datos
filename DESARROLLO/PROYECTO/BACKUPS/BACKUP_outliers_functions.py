#PRUEBA PARA TUKEY detección de outliers
'''
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

		#-----------28-11-2021
		if(ind_col_num_bdd[9] == '0'):

			if (val_max > ind_col_num_bdd[3] or val_min < ind_col_num_bdd[2]):
				if(cur_col >= -3.0 and cur_col <=3.0):
					print(df_num_col.columns[i], "- CURTOSIS: ", cur_col)
					print("FRECUENCIAS:",df_num_col.groupby(df_num_col.columns[i]).size())
					#print("NULOS: ",cont_null) # muestra los valores unicos de la columna y sus frecuencias
					#print("PORCENTAJE DE NULOS EN LA COLUMNA: {}%".format(round((cont_null/cant_filas_df)*100,1)))
					print("IRQ: ", IRQ)

					if(cant_filas_df <=200):
						#Calcular outliers con dixon, cambiando los valores outliers por la MEDIANA
						print("Se debería usar Prueba de Dixon para buscar outliers en este conjunto, dado que su nro de registros es: {}".format(cant_filas_df))
						break
					else:
						#CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY
						if(IRQ == 0):
							#IRQ != 0 SE USA GRUBBS
							print("Esta col, se analizará por GRUBBS, si encuentra outliers los corregirá por la mediana de la columna, [{}].".format(mediana))
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
							#CORRECCION, SE USABA GRUBBS CUANDO IRQ = 0 Y TUKEY CUANDO IRQ != 0, PERO GRUBBS HA DADO BUENOS RESULTADOS EN EL SEGUNDO CASO, PUES EL SEGUNDO CASO ES MUY RARO DE DARSE, PODRÍA IMPLEMENTARSE SOLO GRUBBS PARA AMBOS CASOS
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
					print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.\n".format(df_num_col.columns[i], cur_col))

			elif(val_max <= ind_col_num_bdd[3] and val_min >= ind_col_num_bdd[2]):
				print("Los valores máximo y mínimo de la columna [{}] del conjunto de entrada MAX: {} y MIN: {}, están dentro de los rangos definidos en el primer ingreso MAX: {} y MIN: {}. Esta columna no requiere corrección de outliers.\n".format(df_num_col.columns[i], val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2]))
				#break
			else:
				print("HA OCURRIDO UN ERROR EN LA DETECCION DE OUTLIERS EN LA COLUMNA [{}].".format(df_num_col.columns[i]))
				print(val_max,val_min,ind_col_num_bdd[3], ind_col_num_bdd[2])
				break
		elif(ind_col_num_bdd[9] != '0'):
			print("Se ha especificado en el diccionario de datos, que la columna [{}], no sea tratada para outliers, debido al contexto.\n".format(df_num_col.columns[i]))
		else:
			print("Ha ocurrido un error en la corrección de outliers para la columna [{}]\n".format(df_num_col.columns[i]))

'''



'''
#------ se validaba para implementar dixon pero al final no se agrega asique se comenta
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

			if(cant_filas_df <=200):
				#Calcular outliers con dixon, cambiando los valores outliers por la MEDIANA
				print("Se debería usar Prueba de Dixon para buscar outliers en este conjunto, dado que su nro de registros es: {}".format(cant_filas_df))
				#break
			else:
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
					print("Esta col, se debe analizar por método de Tukey")
					probables_outliers, posibles_outliers = of.tukeys_method(df_num_col,df_num_col.columns[i])
					print("PROBABLES OUTLIERS: ",probables_outliers)
					print("POSIBLES_OUTLIERS",posibles_outliers)
				print("FRECUENCIAS - POST Correccion:",df_num_col.groupby(df_num_col.columns[i]).size())
			print('\n')
		else:
				print("La columna [{}], posee una curtosis de {}, por lo cual no se tratará su corrección de outliers en esta versión del prototipo.".format(df_num_col.columns[i], cur_col))

'''




"""
#--------------------------------grubbs------------------------
#Funcion para calcular las características G
def grubbs_stat(y):
	std_dev = np.std(y)
	avg_y = np.mean(y)
	abs_val_minus_avg = abs(y - avg_y)
	max_of_deviations = max(abs_val_minus_avg)
	max_ind = np.argmax(abs_val_minus_avg)
	Gcal = max_of_deviations / std_dev
	print ("Grubbs Statistics value: {}".format(Gcal))
	return Gcal,max_ind

def calculate_critical_value(size,alpha):
	t_dist = stats.t.ppf(1 - alpha / (2* size),size - 2)
	numerator = (size - 1) * np.sqrt(np.square(t_dist))
	denominator = np.sqrt(size) * np.sqrt(size - 2 + np.square(t_dist))
	critical_value = numerator / denominator
	print("Grubbs critical value: {}".format(critical_value))
	return critical_value

def check_G_values(Gs, Gc, inp, max_index):
	if Gs > Gc:
		print("{} is an outlier. G > G-critical: {:.4f} > {:.4f} \n".format(inp[max_index], Gs, Gc))
	else:
		print("{} is not an outlier. G > G-critical: {:.4f} > {:.4f} \n".format(inp[max_index],Gs,Gc))

#PARAMETROS: VECTOR NUMERICO CON LOS DATOS A ANALIZAR, ALPHA = NIVEL DE SIGNIFICANCIA DEL TEST, NUMERO MAXIMO DE OUTLIERS A DETECTAR
def ESD_Test(input_series, alpha, max_outliers,df,df_col_num,nom_col_num):
	for iterations in range (max_outliers):
		Gcritical = calculate_critical_value(len(input_series), alpha)
		Gstat, max_index = grubbs_stat(input_series)
		check_G_values(Gstat, Gcritical, input_series, max_index)
		#dado este escenario, donde los datos tienen distrib normnal, conjunto con outliers, debe imputarse por la media el valor
		print(input_series.head(20), "indice valor: ",max_index, "valor: ", input_series[max_index], "MEDIA: ", input_series.mean())
		#input_series = np.delete(input_series, max_index) #aqui me borra el elemento, porque esta echo para un array, pero como lo usaré para una columna de un dataframe debo cambiar el valor por uno valido, POR ESO ME ARROJA 100 TODO EL RATO 

"""