import psycopg2
import pandas as pd
import os
import io
from sqlalchemy import create_engine
import sqlalchemy

import functions as f

from datetime import datetime
now = datetime.now()
date_time = now.strftime("%m-%d-%Y %H:%M:%S")

def conectarse():
    try:
        conn = psycopg2.connect(host='localhost', database='TRABAJO_DE_TITULO', user= 'postgres', password='admin', port = 5433)
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print( 'Error en getConfiguracion:\nTypeError:{}\nError:{}'.format( type(e), e ) )


def insert_indic_bdd(df,df_string,df_num): 
    for i in range(len(df.columns)):
        if(df.columns[i] in df_string.columns):
            c1, cx = conectarse()
            cx.execute(""" insert into pruebas."DICCIONARIO_DE_DATOS"("NOM_COL", "TIPO_DATO", "MODA") 
                       VALUES ('{v1}','{v2}','{v3}'); commit;""".format(v1 = df.columns[i], 
                       v2 = df_string[df.columns[i]].dtype.name, v3 = df_string[df.columns[i]].mode()[0]))
            cx.close()

        if(df.columns[i] in df_num.columns):
            c2, cy = conectarse()
            cy.execute(""" insert into pruebas."DICCIONARIO_DE_DATOS"("NOM_COL", "TIPO_DATO", "MODA", "VAL_MIN", "VAL_MAX", 
                       "MEDIA", "MEDIANA","CURTOSIS") 
                       VALUES ('{v1}','{v2}','{v3}','{v4}','{v5}','{v6}','{v7}','{v8}'); commit;""".format(v1 = df.columns[i],
                       v2 = df_num[df.columns[i]].dtype.name, v3 = df_num[df.columns[i]].mode()[0],
                       v4 = df_num[df.columns[i]].min(), v5 = df_num[df.columns[i]].max(),
                       v6 = df_num[df.columns[i]].mean() , v7 = df_num[df.columns[i]].median(),
                       v8 = df_num[df.columns[i]].kurt()
                       ))
            cy.close()


#primero debo ingresar todos los registros a la bdd, luego consultar por los ID asignados a las columnas STRING, luego ingresar
#los valores únicos para esas columnas segun el id que se les asignó al ingresar el registro de la columna
def columnas_df_bdd():
    dicc = {}
    dicc.setdefault('ID',[])
    dicc.setdefault('COLUMNAS',[])
    dicc.setdefault('TYPES',[])
    c3, cz = conectarse()
    cz.execute(""" SELECT "ID", "NOM_COL", "TIPO_DATO" FROM pruebas."DICCIONARIO_DE_DATOS";""")
    for i in cz.fetchall():
        #print(i[0]," - ",i[1]," - ",i[2])
        dicc["ID"].append(i[0])
        dicc["COLUMNAS"].append(i[1])
        dicc["TYPES"].append(i[2])
    cz.close()
    return dicc




def extrae_ind_col_num(nom_col):
    dicc = []
    #print(nom_col)
    c3, cz = conectarse()
    cz.execute(""" SELECT "ID", "NOM_COL", "VAL_MIN", "VAL_MAX", "CURTOSIS", "MODA", "MEDIA", "MEDIANA", "TIPO_DATO", "OUTLIERS", "NULLS" FROM pruebas."DICCIONARIO_DE_DATOS"
                 where "NOM_COL" = '{v1}';""".format(v1 = nom_col))
    for i in cz.fetchall():
        dicc.append(i[0])
        dicc.append(i[1])
        dicc.append(i[2])
        dicc.append(i[3])
        dicc.append(i[4])
        dicc.append(i[5])
        dicc.append(i[6])
        dicc.append(i[7])
        dicc.append(i[8])
        dicc.append(i[9])
        dicc.append(i[10])
    cz.close()
    return dicc




def insert_unique_values_string(dataframe_cols,string_dataframe):
    c3, cz = conectarse()
    for i in range(len(dataframe_cols["TYPES"])):
        if(dataframe_cols["TYPES"][i] not in ['int64','float64','number']):
            aux = string_dataframe[dataframe_cols["COLUMNAS"][i]].unique()
            for j in range(len(aux)):
                cz.execute(""" insert into pruebas."UNIQUE_VALUES_STRING_COLUMNS"("ID_DICC_DATOS","VAL_UNICO") VALUES 
                          ('{v1}','{v2}'); COMMIT;""".format(v1 = dataframe_cols["ID"][i], v2 = aux[j]))
    cz.close()

def alter_num_types(df_num):
  for i in range(len(df_num.columns)):
    c2, cy = conectarse()
    cy.execute("""
      alter table public."TABLA_HISTORICA_DATOS" alter column "{v1}" type double precision; commit;
      """.format(v1 = df_num.columns[i]))
    cy.close()

def crea_tabla_historica(df):
  df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
  #crea la tabla historica con el nombre del primer archivo ingresado
  engine = create_engine('postgresql://postgres:admin@localhost:5433/TRABAJO_DE_TITULO')
  df['fecha_carga'] = date_time
  df.head(0).to_sql('TABLA_HISTORICA_DATOS', engine, if_exists='replace',index=False)
  #df.head(0).to_sql('TABLA_HISTORICA_{}'.format(table_name), engine, if_exists='replace',index=False)
  #pobla la tabla creada con la data depurada del dataframe de entrada
  conn = engine.raw_connection()
  cur = conn.cursor()
  output = io.StringIO()
  df.to_csv(output, sep='\t', header=False, index=False)
  output.seek(0)
  contents = output.getvalue()
  cur.copy_from(output, 'TABLA_HISTORICA_DATOS', null="") # null values become ''
  #cur.copy_from(output, 'TABLA_HISTORICA_{}'.format(table_name), null="") # null values become ''
  conn.commit()
  alter_num_types(df_col_numericas)

def insert_df_atabla(df):
  engine = create_engine('postgresql://postgres:admin@localhost:5433/TRABAJO_DE_TITULO')
  conn = engine.raw_connection()
  cur = conn.cursor()
  output = io.StringIO()
  df['fecha_carga'] = date_time
  df.to_csv(output, sep='\t', header=False, index=False)
  output.seek(0)
  contents = output.getvalue()
  cur.copy_from(output, 'TABLA_HISTORICA_DATOS', null="") # null values become ''
  #cur.copy_from(output, 'TABLA_HISTORICA_{}'.format(table_name), null="") # null values become ''
  conn.commit()


def update_indic_bdd(df,df_string,df_num): 
    for i in range(len(df.columns)):
        if(df.columns[i] in df_string.columns):
            c1, cx = conectarse()
            cx.execute(""" update pruebas."DICCIONARIO_DE_DATOS" set "MODA" = '{v1}' 
                       where "NOM_COL" = '{v2}'; commit;""".format(v1 = df_string[df.columns[i]].mode()[0], 
                       v2 = df.columns[i]))
            cx.close()

        if(df.columns[i] in df_num.columns):
            c2, cy = conectarse()
            cy.execute(""" update pruebas."DICCIONARIO_DE_DATOS" set "MODA" = {v1}, 
                       "MEDIA" = {v2}, "MEDIANA" = {v3}, "CURTOSIS" = {v4}
                       where "NOM_COL" = '{v5}'; commit;""".format( v1 = df_num[df.columns[i]].mode()[0],
                       v2 = df_num[df.columns[i]].mean() , v3 = df_num[df.columns[i]].median(),
                       v4 = df_num[df.columns[i]].kurt(), v5 = df.columns[i]
                       ))
            cy.close()


def actualiza_dicc_datos():
  tabla = 'TABLA_HISTORICA_DATOS'
  engine = create_engine('postgresql://postgres:admin@localhost:5433/TRABAJO_DE_TITULO')
  df = pd.read_sql_table(tabla,engine)
  #print(df.columns)
  df_col_numericas,df_col_string = f.sep_col_string_and_num(df)
  #print(df_col_numericas.columns)
  #print(df_col_string.columns)
  update_indic_bdd(df,df_col_string, df_col_numericas)


#actualiza_dicc_datos()





def trae_tabla_bdd(tabla): #trae tabla por el nombre en caso de que se ingrese como parámetro
  try:
    engine = create_engine('postgresql://postgres:admin@localhost:5433/TRABAJO_DE_TITULO')
    df = pd.read_sql_table(tabla,engine)
    #print(df.columns)
    #print(df)
    return df
  except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    #print(error)
    print("El error es: ",e,type(e), error)


def lista_tablas_bdd():
  tablas = []
  c3, cz = conectarse()
  cz.execute("""
    SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';
    """)
  for i in cz.fetchall():
    tablas.append(i[0])
  #print(tablas)
  cz.close()
  return tablas



#lista_tablas_bdd()
