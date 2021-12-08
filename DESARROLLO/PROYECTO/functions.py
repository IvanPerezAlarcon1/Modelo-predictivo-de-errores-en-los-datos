import pandas as pd
import os

def dataframe_from_file(archivo): #detecta el tipo de archivo y devuelve un dataframe del archivo ingresado
    aux1 , aux2 = os.path.splitext(archivo)
    if (aux2) == '.csv':
        dataframe = pd.read_csv(archivo)
    if (aux2) == '.xlsx':
        dataframe = pd.read_excel(archivo)
    return dataframe

def dataframe_from_file_sep(archivo,separador):
    aux1, aux2 =  os.path.splitext(archivo)
    if (aux2) == '.csv':
        dataframe = pd.read_csv(archivo,sep = separador)
    if(aux2) == '.xlsx':
        dataframe = pd.read_excel(archivo)
    return dataframe

def dataframe_from_excel(archivo):
	dataframe = pd.read_excel(archivo)

def nombre_archivo(archivo): #retorna el nombre del archivo ingresado
	aux1,aux2 = os.path.splitext(os.path.basename(archivo))
	return aux1

def dframe_to_dicc(dataframe): #devuelve un diccionario con parametros comunes para toda columna
    dic = {}
    dic.setdefault('COLUMNAS',[])
    dic.setdefault('TYPES',[])
    dic.setdefault('MODA',[])
    for i in range(len(dataframe.columns)):
        dic['COLUMNAS'].append(dataframe.columns[i])
        dic['TYPES'].append(dataframe[dic['COLUMNAS'][i]].dtype.name)
        dic['MODA'].append(dataframe[dataframe.columns[i]].mode()[0])
    return dic


#NOTA: Se podría corroborar que los registros sean válidos para la columna
def sep_col_string_and_num(dataframe): #devuelve 2 DATAFRAMES con las columnas tipo numericas y string
    df_num = dataframe.select_dtypes(include=['int64','float64','number'])
    df_string = dataframe.select_dtypes(exclude=['int64','float64'])
    return df_num,df_string


def indicadores_col_num(df_num): #ingresa un df con las columnas numericas y retorna un diccionario con los indicadores definidos ese tipo
	cols = {}
	cols.setdefault('NAME',[]), cols.setdefault('TYPE',[]), cols.setdefault('MODA',[]),
	cols.setdefault('MAX_VAL',[]), cols.setdefault('MIN_VAL',[]), 
	cols.setdefault('MEDIA',[]), cols.setdefault('MEDIANA',[]), cols.setdefault('CURTOSIS',[])
	for i in range(len(df_num.columns)):
		cols['NAME'].append(df_num.columns[i]), cols['TYPE'].append(df_num[df_num.columns[i]].dtype.name),
		cols['MODA'].append(df_num[df_num.columns[i]].mode()[0]),
		cols['MAX_VAL'].append(df_num[df_num.columns[i]].max()), cols['MIN_VAL'].append(df_num[df_num.columns[i]].min()),
		cols['MEDIA'].append(df_num[df_num.columns[i]].mean()), cols['MEDIANA'].append(df_num[df_num.columns[i]].median()),
		cols['CURTOSIS'].append(df_num[df_num.columns[i]].kurt())
		"""
		print( i+1, "NAME: ", df_num.columns[i], 
		"//TYPE: ", df_num[df_num.columns[i]].dtype.name, "// MAX_VAL:", df_num[df_num.columns[i]].max(), 
		"// MIN_VAL: ", df_num[df_num.columns[i]].min(), "// MEDIA: ", df_num[df_num.columns[i]].mean(),
		"//MEDIANA: ", df_num[df_num.columns[i]].median(), "//CURTOSIS: ", df_num[df_num.columns[i]].kurt())
		"""
	return cols

def indicadores_col_string(df_string):
	cols = {}
	cols.setdefault('NAME',[]), 
	cols.setdefault('TYPE',[]),
	cols.setdefault('MODA',[])
	for i in range(len(df_string.columns)):
		cols['NAME'].append(df_string.columns[i]), cols['TYPE'].append(df_string[df_string.columns[i]].dtype.name),
		cols['MODA'].append(df_string[df_string.columns[i]].mode()[0])
	return cols