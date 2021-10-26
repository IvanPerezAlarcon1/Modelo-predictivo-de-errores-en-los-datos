import pandas as pd
import os
import functions as f
import bdd_functions as bdf
import n_grams_functions as ngf


archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\DESARROLLO\hotel_bookings_1_test2.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar

#------------------------MAIN------------------------------
df = f.dataframe_from_file(archivo)
#print(df)
df_col_numericas,df_col_string = f.sep_col_string_and_num(df)

#VALORES UNICOS DE LA COLUMNA QUE ESTOY ANALIZANDO
unicos = ngf.col_unique_values(df_col_string['hotel'])

#VALORES UNICOS DE LA COLUMNA ANALIZADA, PERO DESDE LA BDD
val_uni_col = ngf.col_bdd_unique_values(df_col_string['hotel'],'hotel')

cadena_entrada = unicos[0]
print(cadena_entrada)

cadena_bdd = val_uni_col[0]
print(cadena_bdd)

from ngram import NGram
print(NGram.compare(cadena_entrada,cadena_bdd))

print("DIFERENCIA")

a1, word1 = ngf.diff_ngram('Resort Htel','Resort Hotel', 3)
print("3-grams: ", a1,word1)

a2, word2 = ngf.diff_ngram("hola que tal?, soy iván","hola soy iván", 3)
print("3-grams: ", a2,word2)

'''
Lo que quiero hacer es, identificar la columna de entrada, con la del diccionario, por nombre, luego comparar los registros únicos
de cada listado de registros únicos, mediante N-grams ir comparando el grado de similitud y según el grado, ir tomando acciones

- Si similitud [0 - 0.45], son registros distintos, luego se compara similitud con el siguiente
- Si similitud [0.46 - 0.79], se identifica el registro como posible duplicado, entonces.......
- Si similitud [0.8 - 0.99], se asume son duplicados, luego la cadena en el conjunto de entrada, se reemplaza por su valor válido 
del diccionario
- Si similitud [1], se asume son duplicados, luego no se realizan más acciones y se deja de buscar duplicados para ese caso
'''