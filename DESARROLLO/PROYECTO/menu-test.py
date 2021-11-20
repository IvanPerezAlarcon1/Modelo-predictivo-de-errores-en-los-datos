import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy

def trae_tabla_bdd(tabla):
	try:
		engine = create_engine('postgresql://postgres:admin@localhost:5433/TRABAJO_DE_TITULO')
		df = pd.read_sql_table(tabla,engine)
		print(df.columns)
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		#print(error)
		print(e,type(e), error)

print("\nBienvenido al prototipo v1 del 'Modelo predictivo de errores en los datos' \n")


ans = True
while ans:
	print("-----------------Menú--------------------------\n")
	print("Seleccione entre las opciones disponibles, el método de ingreso de archivo: \n")
	print("1 - archivo de extensión .csv")
	print("2 - archivo excel de extensión .xlsx")
	print("3 - nombre de tabla base de datos postgresql (la tabla debe estar en la misma bdd que el prototipo, esquema public)")
	print("4 o cualquier otro número para salir.")
	print("\n")
	ans = input("Ingrese la opción requerida: ")
	if(ans == "1"):
		print("Opción 1")
	elif(ans == "2"):
		print("Opción 2")
	elif(ans == "3"):
		print("Opción 3")
	elif(ans == "4"):
		print("Ha salido del programa.")
		ans = False
	elif (ans != ""):
		print("Opción no válida, ingrese una opción válida")
