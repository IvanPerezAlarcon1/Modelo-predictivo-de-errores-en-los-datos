import psycopg2

def conectarse():
	try:
		conn = psycopg2.connect(host='localhost', database='TRABAJO_DE_TITULO', user= 'postgres', password='admin', port = 5433)
		cur = conn.cursor()
		return conn, cur
	except Exception as e:
		print( 'Error en getConfiguracion:\nTypeError:{}\nError:{}'.format( type(e), e ) )




#----------------llamada funcion----------------------
c1, cx = conectarse()
cx.execute('SELECT "ID", "NOM_COL", "TIPO_DATO" FROM pruebas."DICCIONARIO_DE_DATOS";')

for i in cx.fetchall():
    print(i[0]," - ",i[1]," - ",i[2])

c1.close()