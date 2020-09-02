"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it

from time import process_time 




def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos de peliculas")
    print("2- Cargar Datos de elenco")
    print("3- Encontrar buenas peliculas de un director")
    print("4- Ranking de peliculas")
    print("5- Conocer un director")
    print("6- Conocer un actor")
    print("7- Entender un genero")
    print("8- Crear ranking")
    print("0- Salir")

def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1

def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst

def loadMovies(nombre_archivo:str):
    #nombre_archivo= input("Ingrese el nombre del archivo CSV: ")
    lst_movies = loadCSVFile(nombre_archivo,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst_movies)) + " elementos cargados")
    #print(lst_movies)
    return lst_movies

def loadCasting (nombre_archivo:str):
    #nombre_archivo= input("Ingrese el nombre del archivo CSV: ")
    lst_casting = loadCSVFile(nombre_archivo,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst_casting)) + " elementos cargados")
    #print(lst_casting)
    return lst_casting

def buenas_peliculas(lista_pelis:dict,lista_casting:dict,nombre_director:str)-> tuple:
    cuenta= 0
    numero_buenas_peliculas= 0
    suma_votaciones= 0
    promedio_votos= 0
    lista_id= []
    lista_peliculas_buenas= []
    cuenta_elem_1= 1
    cuenta_elem_2= 1
    while cuenta_elem_1<=lt.size(lista_casting):
        info= lt.getElement(lista_casting,cuenta_elem_1)
        if info["director_name"]==nombre_director:
            lista_id.append(info["id"])
        cuenta_elem_1+= 1
    while cuenta_elem_2<=lt.size(lista_pelis):
        datos= lt.getElement(lista_pelis,cuenta_elem_2)
        if float(datos["vote_average"])>=6 and datos["id"]==lista_id[cuenta] and cuenta<(len(lista_id)-1):
            numero_buenas_peliculas+= 1
            suma_votaciones+= float(datos["vote_average"])
            lista_peliculas_buenas.append(datos["original_title"])
            cuenta+= 1
        cuenta_elem_2+= 1
    promedio_votos= round(suma_votaciones/numero_buenas_peliculas,2)
    tupla= (nombre_director,numero_buenas_peliculas,promedio_votos,lista_peliculas_buenas)
    return tupla

def registro_actor(lista_pelis:dict,lista_elenco:dict,nombre_actor:str)->tuple:

    registro_directores= {}
    numero_peliculas= 0
    lista_peliculas_actor= []
    suma_peliculas= 0
    max_directores= 0
    lista_id= []
    cuenta_elem_1= 1
    cuenta_elem_2= 1
    cuenta_lista= 0

    while cuenta_elem_1<=lt.size(lista_elenco):
        datos= lt.getElement(lista_elenco,cuenta_elem_1)
        if datos["actor1_name"]==nombre_actor or datos["actor2_name"]==nombre_actor\
        or datos["actor3_name"]==nombre_actor or datos["actor4_name"]==nombre_actor\
        or datos["actor5_name"]==nombre_actor:
            lista_id.append(datos["id"])
            numero_peliculas+= 1
            if datos["director_name"] not in registro_directores:
                registro_directores[datos["director_name"]]= 0
            registro_directores[datos["director_name"]]+= 1
        cuenta_elem_1+= 1
        
    while cuenta_elem_2<=lt.size(lista_pelis):
        elementos= lt.getElement(lista_pelis,cuenta_elem_2)
        if elementos["id"]==lista_id[cuenta_lista]:
            suma_peliculas+= float(elementos["vote_average"])
            lista_peliculas_actor.append(elementos["original_title"])
            cuenta_lista+= 1
        cuenta_elem_2+= 1

    for directores in registro_directores:
        if registro_directores[directores]>max_directores:
            max_directores= registro_directores[directores]
            director_recurrente= directores
    
    promedio_peliculas= round(suma_peliculas/numero_peliculas,2)

    tupla= (nombre_actor,numero_peliculas,promedio_peliculas,director_recurrente,max_directores,lista_peliculas_actor)

    return  tupla

def conocer_director(director:str,lista_pelis:dict,lista_elenco:dict)->str:
    peli=[]
    lista_id=[]
    cuenta=0
    numerador=0
    promedio=0
    i=0
    j=0
    k=0
    while i<lt.size(lista_elenco):
        if lista_elenco["elements"][i]["director_name"] == director:
            lista_id.append(lista_elenco["elements"][i]["id"])
        i+=1
    while j<lt.size(lista_pelis):
        if lista_pelis["elements"][j]["id"] == lista_id[cuenta]:
            peli.append(lista_pelis["elements"][j]["title"])
            cuenta+=1            
        j+=1     
    cuenta=0
    while k<lt.size(lista_pelis):
        if lista_pelis["elements"][k]["id"] == lista_id[cuenta]:
            numerador+=float(lista_pelis["elements"][k]["vote_average"])
            cuenta+=1            
        k+=1     
    denominador=len(lista_id)
    promedio=round(numerador/denominador,2)
    texto="La cantidad de películas dirigidas por "+director+" son: "+str(denominador)+", " +str(peli)+" y tienen un promedio de calificación de "+str(promedio)
                
    return texto

#print(conocer_director("Jean Renoir",loadMovies("m/DetailsSmall.csv"),loadCasting("m/CastingSmall.csv")))  

def entender_genero(lista_p,genero)->str:

    lista_peliculas_genero = []
    lista_votos = []
    numerador = 0
    promedio = 0
    i=0
    while i<lt.size(lista_p):
        if genero in lista_p["elements"][i]["genres"]:
            lista_peliculas_genero.append(lista_p["elements"][i]["title"])
            numerador += float(lista_p['elements'][i]['vote_count'])
            lista_votos.append(lista_p['elements'][i]['vote_count'])
        i+=1
    #print(numerador)
    promedio = round(numerador/len(lista_votos))
    texto = 'Se encontraron '+str(len(lista_peliculas_genero))+' películas del género '+genero+'\nEsta es una lista de todas las películas asociadas al género '+genero+': '+str(lista_peliculas_genero)+'\nEl promedio de votos del género '+genero+' fue '+str(promedio)
    return texto

#print(entender_genero(loadMovies("m/DetailsSmall.csv"),'Comedy'))  

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    Ricardo Sanchez
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs= input('Seleccione una opción para continuar: \n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs)==1: #opcion 1
                nombre_archivo= input("Ingrese el nombre del archivo CSV: ")
                lstmovies = loadMovies(nombre_archivo)
                print (lstmovies)
            
            elif int(inputs)==2: #opcion 2
                nombre_archivo= input("Ingrese el nombre del archivo CSV: ")
                lstcasting = loadCasting(nombre_archivo)
                print(lstcasting)

            elif int(inputs)==3: #opcion 3
                director= input("Ingrese el nombre del director del que desea obtener información: ")
                buenas_director= buenas_peliculas(lstmovies,lstcasting,director)
                print (buenas_director[0]+" tiene "+str(buenas_director[1])+" peliculas con una calificación por encima de 6, y el promedio de las votaciones es de "+str(buenas_director[2])+". Las siguientes peliculas del director son las que cumplen con el requerimiento de votación: \n")
                print (buenas_director[3])
                pass

            elif int(inputs)==4: #opcion 4
                genero= input("Ingrese el genero del que desea consultar información: ")
                res_genero= entender_genero(lstmovies,genero)
                print(res_genero)
                pass

            elif int(inputs)==5: #opcion 5
                director=input("Ingrese el nombre del director del que desea consultar la información: ")
                informacion_director= conocer_director(director,lstmovies,lstcasting)
                print(informacion_director)
                pass

            elif int(inputs)==6: #opcion 6
                actor= input("Ingrese el nombre del actor del que desea consultar información: ")
                info_actor= registro_actor(lstmovies,lstcasting,actor)
                print(info_actor[0]+" participó en "+str(info_actor[1])+" peliculas, la votación promedio\
                de las peliculas en las que actuó es de "+str(info_actor[2])+" y el director con\
                el que mas colaboró fue "+info_actor[3]+" con "+str(info_actor[4]+" colaboraciones")+". A \
                continuación se encuentra la lista de peliculas en las que apareció "+info_actor[0]+": \n")
                print (info_actor[5])
                pass

            elif int(inputs)==7: #opcion 7
                genero= input("Ingrese el genero del que desea consultar información: ")
                gender= entender_genero(genero, lstmovies)
                print(gender)
                pass

            elif int(inputs)==8: #opcion 8
                pass


            elif int(inputs)==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()