import pandas as pd
import os
import functions as f
import bdd_functions as bdf


#------------------------MAIN------------------------------
archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.csv'

df = f.dataframe_from_file(archivo)
dicc_df = f.dframe_to_dicc(df)
df_col_number,df_col_string = f.sep_col_string_and_num(df)

print(df_col_number.columns)
print(df_col_string.columns)
print(dicc_df)


#podría hacer un for, que recorra el diccionario del dataframe, dependiendo de si es string o numerico inserta la columna con 
#sus respectivos parametros, numericas solo los indices y string insertando igual los valores únicos






#----------------llamada funcion bdd----------------------
#c1, cx = bdf.conectarse()
#cx.execute('SELECT "ID", "NOM_COL", "TIPO_DATO" FROM pruebas."DICCIONARIO_DE_DATOS";')

#for i in cx.fetchall():
#    print(i[0]," - ",i[1]," - ",i[2])

#c1.close()