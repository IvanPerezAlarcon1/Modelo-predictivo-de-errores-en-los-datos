import pandas as pd
import os
import functions as f
import bdd_functions as bdf


#------------------------MAIN------------------------------
archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.csv' # se demora 2.8 seg en terminar
#archivo = r'C:\Users\ivan1\Desktop\Modelo-predictivo-de-errores-en-los-datos\hotel_bookings_1.xlsx' # se demora 43.9 seg en terminar

df = f.dataframe_from_file(archivo)
dicc_df = f.dframe_to_dicc(df)
df_col_numericas,df_col_string = f.sep_col_string_and_num(df)

bdf.insert_indic_bdd(df,df_col_string,df_col_numericas)
df_bdd_cols = bdf.columnas_df_bdd()
bdf.insert_unique_values_string(df_bdd_cols,df_col_string)



