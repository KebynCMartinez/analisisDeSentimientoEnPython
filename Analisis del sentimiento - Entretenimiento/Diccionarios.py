import csv
import time

limpieza=['http']

# Se inicializan las variables en 0 o vacio
diccionario=[]
cuenta =0
contador=[]

# Revisa si en la carpeta donde se ubica este archivo .py si 
# existe diccionarios.csv, si no existe lo crea pero si esta existiendo
# lo ocupa

dic = open("diccionario.csv", "w")

# Se introduce los archivos donde tengamos nuestras descargas
# y solo pueden ser de tipo .csv
tweets=["result1.csv","result2.csv","result3.csv"]
for t in tweets:
	
	# Abre todos esos archivos
	f = open(t)

	# Realiza lectura completa de todos los tweets
	r = csv.reader(f, delimiter=',')

	# Lee el documento por filas y celdas
	for fila in r:
		for pal in fila[1].split(" "):
			print pal
			if not pal.split(":")[0]=='https' or pal[-1:-3]=="...":
				if len(pal)>3:
				
					if pal in diccionario:
						print 'existe'
						num=diccionario.index(pal)
						contador[num]=contador[num]+1
					else:
						contador.append(1)
						diccionario.append(pal)

		# Cuenta el numero de veces que se repite una palabra
		cuenta=cuenta+1
		print cuenta
f.close()  
for final in range(len(diccionario)):
	print diccionario[final]
	print contador[final]
	arr=[]
	arr.append(diccionario[final])
	arr.append(contador[final])

	# Guarda todas las palabras en el archivo
	writer = csv.writer(dic)
	writer.writerow(arr)
	#time.sleep(1)
	
print diccionario
print contador