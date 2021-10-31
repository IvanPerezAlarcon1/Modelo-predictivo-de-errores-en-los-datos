import numpy as np
import pandas as pd
import scipy.stats as stats

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
            outliers_prob.append(index)
    for index, x in enumerate(df[variable]):
        if x <= inner_fence_le or x >= inner_fence_ue:
            outliers_poss.append(index)
    return outliers_prob, outliers_poss



def sep_casos(df, df_num_col):
    for i in range(len(df_num_col.columns)):
        cur_col = round(df_num_col[df_num_col.columns[i]].kurt(),1) #curtosis
        cont_null = df_num_col[df_num_col.columns[i]].isna().sum() #cant.nulos columna
        cant_filas_df = df_num_col.shape[0] #CANT. DE FILAS DEL DATAFRAME
        cant_col_df = df_num_col.shape[1] #CANT. DE COLUMNAS DEL DATAFRAME
        #PARA DETECTAR OUTLIERS, LA CONDICION ES QUE LA COL TENGA DISTRIB NORMAL, LUEGO PRIMERO SE TOMAN SOLO ESTAS FILAS
        if(cur_col >= -3.0 and cur_col <=3.0):
            if(cant_filas_df <=200):
                print("Se debería usar Prueba de Dixon para buscar outliers en este conjunto, dado que su nro de registros es: {}".format(cant_filas_df))
                break
            else:
                #CALCULAR EL RANGO INTERCUARTIL Y EN BASE A ESO GENERAR LOS CASOS PARA GRUBBS Y TUKEY





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