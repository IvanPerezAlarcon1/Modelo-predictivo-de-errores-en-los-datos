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
        SELECT "ID", "ID_DICC_DATOS", "VAL_UNICO"
        FROM pruebas."UNIQUE_VALUES_STRING_COLUMNS"
        WHERE "ID_DICC_DATOS" = (SELECT "ID" FROM pruebas."DICCIONARIO_DE_DATOS" WHERE "NOM_COL" = '{v1}');
        """.format(v1 = nom_col))
    for i in cz.fetchall():
        #print(i[0],i[1],i[2])
        val_uni_col.append(i[2])
    return val_uni_col

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