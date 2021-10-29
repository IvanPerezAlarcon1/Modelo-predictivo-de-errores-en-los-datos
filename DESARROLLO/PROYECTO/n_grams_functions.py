import pandas as pd
import os
from textblob import TextBlob
import functions as f
import bdd_functions as bdf

def col_unique_values(col_string):
    var = []
    unicos = col_string.dropna().unique() #elimina valor nan. que dio problemas en algun momento
    #unicos = col_string.unique() #elimina valor nan. que dio problemas en algun momento
    for i in unicos:
        var.append(i)
    #print(unicos)
    return var

def col_bdd_unique_values(col_string,nom_col):
    c3, cz = bdf.conectarse()
    val_uni_col = []
    cz.execute("""
        SELECT u."ID", u."ID_DICC_DATOS", u."VAL_UNICO", d."N_GRAM"
        FROM pruebas."DICCIONARIO_DE_DATOS" d
        inner join pruebas."UNIQUE_VALUES_STRING_COLUMNS" u on u."ID_DICC_DATOS" = d."ID"
        where d."NOM_COL" = '{v1}';
        """.format(v1 = nom_col))
    for i in cz.fetchall():
        #print(i[0],i[1],i[2])
        val_uni_col.append(i[2])
        ID = i[1]
        n_gram = i[3]
    return val_uni_col, ID, n_gram

def ngram(sentence, num):
    tmp = [] 
    sent_len = len(sentence) - num +1
    for i in range(sent_len):
        tmp.append(sentence[i:i+num]) 
    return tmp

def diff_ngram(sent_a, sent_b, num):
    a = ngram(sent_a, num)
    b = ngram(sent_b, num) 
    common = [] 
    cnt = 0 
    for i in a:
        for j in b:
            if i == j:
                cnt += 1
                common.append(i)
    return cnt/len(a), common

#def insert_unique_values_string(val_unicos, nom_col):
#    c3, cz = conectarse()
#    for i in len(val_unicos):
#
#    cz.close()

def revisar_string_cols(df, df_string):
    for i in range(len(df_string.columns)):
        #valores unicos para la columna string analizada
        unicos_col = col_unique_values(df_string[df_string.columns[i]])
        aux = col_unique_values(df_string[df_string.columns[i]])
        #valores unicos registrados en la bdd, para la columna string ingresada
        unicos_col_bdd,ID, n_gram = col_bdd_unique_values(df_string[df_string.columns[i]], df_string.columns[i])
        #si un elemento del conjunto ingresado está en los unicos de la bdd, lo elimino ya que sería el escenario donde la similitud de los elementos seria igual y no requieren tratamiento
        for j in aux:
            if(j in unicos_col_bdd):
                unicos_col.remove(j)
        print("VAL UNICOS ENTRADA no encontrados en BDD: ", unicos_col)
        print("VALORES UNICOS BDD: ",unicos_col_bdd, '\n')

        print(ID)
        aux2 = 0
        aux3 = 0
        for l in unicos_col:
            print("unicos_col: ", l)
            for k in unicos_col_bdd:
                print("unicos_col_bdd: ", k)
                ind, com = diff_ngram(k,l, n_gram)
                if(ind >= 0.6):
                    print("3-grams - REEMPLAZA: ", ind, k, l)
                    df[df_string.columns[i]] = df[df_string.columns[i]].replace(to_replace = l,  value = k)
                    #df_string[df_string.columns[i]] = df_string[df_string.columns[i]].replace(to_replace = l,  value = k)
                    aux2 = 1
                    break
                if(ind < 0.6):
                    print("3-grams - NO REEMPLAZA, SE AGREGA A VALORES UNICOS: ", ind, k, l)
                    #SE INSERTAN LOS VALORES UNICOS
                    c3, cz = bdf.conectarse()
                    cz.execute(""" insert into pruebas."UNIQUE_VALUES_STRING_COLUMNS"("ID_DICC_DATOS","VAL_UNICO") VALUES 
                          ('{v1}','{v2}'); COMMIT;
                        """.format(v1 = ID , v2 = l ))
                    cz.close()
                    aux2 = 1
                    break
                else:
                    print("RESULTADO INDICE DE COMPARACIÓN INVÁLIDO: ", ind)
                    aux3 = 1
            print('\n')
            if(aux == 1):
                break
        if(aux3 == 1):
            break