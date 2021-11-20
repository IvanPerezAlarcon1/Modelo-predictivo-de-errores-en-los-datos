import pandas as pd
pd.options.mode.chained_assignment = None
import os
from textblob import TextBlob
import functions as f
import bdd_functions as bdf
import imputaciones_functions as impf 

#indicador de similitud de n-grams, que indica desde que valor de similitud se acepta como duplicado
#IND_MAX_SIM = 0.45
IND_MAX_SIM = 0.6

def col_unique_values(col_string):
    var = []
    unicos = col_string.dropna().unique() #elimina valor nan. que dio problemas en algun momento
    #unicos = col_string.unique() #elimina valor nan. que dio problemas en algun momento
    for i in unicos:
        var.append(i)
        #var.append(i.upper())
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
        #val_uni_col.append(i[2].upper())
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
        print("Columna analizada: {}".format(df_string.columns[i]))
        for j in aux:
            if(j in unicos_col_bdd):
                unicos_col.remove(j)
        print("VAL UNICOS ENTRADA no encontrados en BDD: ", unicos_col)
        print("VALORES UNICOS BDD: ",unicos_col_bdd, '\n')

        aux2 = 0
        aux3 = 0
        for l in unicos_col:
            print("unicos_col: ", l)
            for k in unicos_col_bdd:
                print("unicos_col_bdd: ", k)
                ind, com = diff_ngram(k,l, n_gram)
                if(ind >= IND_MAX_SIM):
                #if(ind >= 0.46):
                    #print("3-grams - REEMPLAZA: ", ind, k, l)
                    print("{}-grams - REEMPLAZA: {} {} {} ".format(n_gram,ind,k,l))
                    df[df_string.columns[i]] = df[df_string.columns[i]].replace(to_replace = l,  value = k)
                    df_string[df_string.columns[i]] = df_string[df_string.columns[i]].replace(to_replace = l,  value = k)
                    aux2 = 1
                    break
                if(ind < IND_MAX_SIM):
                #if(ind <= 0.45):
                    #print("3-grams - NO REEMPLAZA, SE AGREGA A VALORES UNICOS: ", ind, k, l)
                    print("{}-grams - NO REEMPLAZA: {} {} {} ".format(n_gram,ind,k,l))
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


#---------------------EXPERIMENTACION PARA CORREGIR TECNICA N-GRAMS


def revisar_string_cols_ing_n(df, df_string):
    for i in range(len(df_string.columns)):
        #valores unicos para la columna string analizada
        unicos_col = col_unique_values(df_string[df_string.columns[i]])
        aux = col_unique_values(df_string[df_string.columns[i]])
        #valores unicos registrados en la bdd, para la columna string ingresada
        unicos_col_bdd,ID, n_gram = col_bdd_unique_values(df_string[df_string.columns[i]], df_string.columns[i])
        #si un elemento del conjunto ingresado está en los unicos de la bdd, lo elimino ya que sería el escenario donde la similitud de los elementos seria igual y no requieren tratamiento
        print("Columna analizada: {}".format(df_string.columns[i]))
        for j in aux:
            if(j in unicos_col_bdd):
                unicos_col.remove(j)
        print("VAL UNICOS ENTRADA no encontrados en BDD: ", unicos_col)
        print("VALORES UNICOS BDD: ",unicos_col_bdd, '\n')

        if(len(unicos_col) > 0):
            similitud(unicos_col,unicos_col_bdd,n_gram,df,df_string,df_string.columns[i],ID)
        else:
            print("Esta columna no tiene valores únicos diferentes de los registrados, no se le realizan acciones. \n")


val1 = ['Resort Htel', 'rsort Hotel', 'Cty otel', 'city hotl', 'CITY HTEL', 'C hoTEL', 'Resort h', 'resort H', 'city H', 'City h.', 'city H.', 'Hotel Resort', 'Hotel city']
val2 = ['Resort Hotel', 'City Hotel'] 

#podría, comparar el valor erroneo del conjunto de entrada, guardar en una lista el indice de similitud para cada registro único de la bdd para esa columna
#luego comparar, si la mayor similitud es < 0.6 se agrega como registro único, si es >= a este indice, se reemplaza por ese valor.


def similitud(unico_col,unicos_bdd,n_gram,df,df_string,col_string_name,ID):
    aux = len(unico_col)
    while(aux > 0):
        #print(aux)
        #print(unico_col[0])
        lista = {}
        lista.setdefault('VAL_BDD',[])
        lista.setdefault('IND',[])
        l = unico_col[0]
        for k in (unicos_bdd):
            #print("unicos_col: ", l)
            #print("unicos_col_bdd: ", k)
            #print(l,k)
            ind, com = diff_ngram(k,l, n_gram)
            #print(n_gram)
            lista["VAL_BDD"].append(k)
            lista["IND"].append(ind)

        indicadores = list(lista["IND"])
        bdd_vals = list(lista["VAL_BDD"])
        max_index = max(indicadores)
        ind_max_index = indicadores.index(max_index)
        #print(indicadores)
        #print(bdd_vals)
        #print("max_index: ", max_index)
        #print("MAX INDICE de similitud: ",max_index)
        #print("INDICE DEL INDICE MAXIMO DE SIMILITUD: ", indicadores.index(max(indicadores)))
        #print(l)
        if(max_index >= IND_MAX_SIM):
        #if(max_index >= 0.6):
            VAR1 = bdd_vals[ind_max_index]
            print("unicos_col: ", l)
            print("unicos_col_bdd: ", VAR1)

            print("{}-grams - REEMPLAZA: {} - {} - {} ".format(n_gram,max_index,bdd_vals[ind_max_index],l))
            #impf.imput_n_grams(df,df_string,col_string_name, l,bdd_vals[ind_max_index])
            #print(df_string.columns)
            #print(df.columns)
            #print(col_string_name)
            df[col_string_name] = df[col_string_name].str.replace(l, VAR1)
            df_string[col_string_name] = df_string[col_string_name].str.replace(l, VAR1)
        elif(max_index < IND_MAX_SIM):
        #elif(max_index < 0.6):
            print("unicos_col: ", l)
            print("Valor único de mayor semejanza: ", bdd_vals[ind_max_index])
            #print("{}-grams - NO REEMPLAZA: {} {} {} ".format(n_gram,ind,k,l))
            print("El valor más aproximado es [{}], con un indice de similitud de [{}], pero no alcanza la similitud necesaria, luego este valor se agrega como único al sistema.".format(bdd_vals[ind_max_index],max_index))
            impf.imput_string_new_val(ID,l)
        else:
            print("ALGO SALIÓ MAL!!!!!!!!!")
            #break
        #print(l)
        print("\n")
        unico_col.remove(unico_col[0])
        aux = len(unico_col)





def similitud_test(unico_col,unicos_bdd,n_gram):
    aux = len(unico_col) #['Resort Htel', 'rsort Hotel', 'Cty otel', 'city hotl', 'CITY HTEL', 'C hoTEL', 'Resort h', 'resort H', 'city H', 'City h.', 'city H.', 'Hotel Resort', 'Hotel city']
    while(aux > 0):
        #print(aux)
        #print(unico_col[0])
        lista = {}
        lista.setdefault('VAL_BDD',[])
        lista.setdefault('IND',[])
        l = unico_col[0]
        for k in (unicos_bdd):
            #print("unicos_col: ", l)
            #print("unicos_col_bdd: ", k)
            ind, com = diff_ngram(k,l, n_gram)
            lista["VAL_BDD"].append(k)
            lista["IND"].append(ind)

        indicadores = list(lista["IND"])
        bdd_vals = list(lista["VAL_BDD"])
        max_index = max(indicadores)
        ind_max_index = indicadores.index(max_index)
        #print(indicadores)
        #print(bdd_vals)
        #print("MAX INDICE de similitud: ",max_index)
        #print("INDICE DEL INDICE MAXIMO DE SIMILITUD: ", indicadores.index(max(indicadores)))
        print(l)
        if(max_index >= IND_MAX_SIM):
            print("unicos_col: ", l)
            print("unicos_col_bdd: ", bdd_vals[ind_max_index])
            print("{}-grams - REEMPLAZA: {} {} {} ".format(n_gram,ind,k,l))
            #impf.imput_n_grams(df,df_string,col_string_name, l,bdd_vals[ind_max_index])

            #df[df_string.columns[col_string_name]] = df[df_string.columns[col_string_name]].replace(to_replace = l,  value = k)
            #df_string[df_string.columns[col_string_name]] = df_string[df_string.columns[col_string_name]].replace(to_replace = l,  value = k)

        elif(max_index < IND_MAX_SIM):
            print("unicos_col: ", l)
            #print("unicos_col_bdd: ", bdd_vals[ind_max_index])
            #print("{}-grams - NO REEMPLAZA: {} {} {} ".format(n_gram,ind,k,l))
            print("El valor más aproximado es {}, pero no alcanza la similitud necesaria, luego este valor se agrega como único al sistema.".format(bdd_vals[ind_max_index]))
            #impf.imput_string_new_val(ID,l)
        else:
            print("RESULTADO INDICE DE COMPARACIÓN INVÁLIDO: ", ind)
            #break
        print(l,aux)
        unico_col.remove(unico_col[0])
        aux = len(unico_col)
        print(l,aux)
        print("\n")


#similitud_test(val1,val2,2)




'''
def guarda_ind_similitud(unico_col,unicos_bdd,n_gram):
    lista = {}
    lista.setdefault('val_bdd',[])
    lista.setdefault('ind_sim',[])
    for k in unicos_bdd:
        ind, com = diff_ngram(k,unico_col, n_gram)
        lista['val_bdd'].append(k)
        lista['ind_sim'].append(ind)
    print(unico_col)
    for item in lista.items():
        print(item) #imprime las lineas key: value
    for key in lista.keys():
        print(key) #imprime solo las key
    for value in lista.values():
        print(value) #imprime los valores, en este caso son lista

#guarda_ind_similitud(val1[0],val2,2)
'''