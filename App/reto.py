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

import App.config as cf
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
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
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

def loadMovies():
    nombre_archivo= input("Ingrese el nombre del archivo CSV: ")
    lst_movies = loadCSVFile(nombre_archivo,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst_movies)) + " elementos cargados")
    return lst_movies

def loadCasting ():
    nombre_archivo= input("Ingrese el nombre del archivo CSV: ")
    lst_casting = loadCSVFile(nombre_archivo,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst_casting)) + " elementos cargados")
    return lst_casting

def registro_actor(lista_pelis:dict,lista_elenco:dict,nombre_actor:str)->str:

    registro_directores: {}
    numero_peliculas= 0
    lista_peliculas_actor= []
    suma_peliculas= 0
    max_directores= 0
    lista_id= []

    for elementos in lista_elenco["elements"]:
        if elementos[1]==nombre_actor or elementos[3]==nombre_actor or elementos[5]==nombre_actor or\
            elementos[7]==nombre_actor or elementos[9]==nombre_actor:
            lista_id.append(elementos[0])
            numero_peliculas+= 1
            if elementos[12] not in registro_directores:
                registro_directores[elementos][12]= 0
            registro_directores[elementos][12]+= 1

    cuenta_lista= 0

    for elementos in lista_pelis["elements"]:
        if elementos[0]==lista_id[cuenta_lista]:
            suma_peliculas+= elementos[17]
            lista_peliculas_actor.append(elementos[5])
            cuenta_lista+= 1

    for directores in registro_directores:
        if registro_directores[directores]>max_directores:
            max_directores= registro_directores[directores]
            director_recurrente= directores
    
    promedio_peliculas= round(suma_peliculas/numero_peliculas,2)
    texto=  nombre_actor+" participó en "+str(numero_peliculas)+" peliculas, la votación promedio\
            de las peliculas en las que actuó es de "+str(promedio_peliculas)+" y el director con\
            el que mas colaboró fue "+director_recurrente+" con "+str(max_directores)+". A \
            continuación se encuentra la lista de peliculas en las que apareció "+nombre_actor+": \n"

    return  texto + str(lista_peliculas_actor)


def conocer_director(director:str,lista_pelis:dict,lista_elenco:dict)->str:
    peli=[]
    lista_id=[]
    numero_peliculas=0
    cuenta=0
    numerador=0
    promedio=0
    for elementos in lista_elenco["elements"]:
        if elementos[12]==director:
            lista_id.append(elementos[0])
            numero_peliculas+=1
    for elementos in lista_pelis["elements"]:
        if elementos[0]== lista_id[cuenta]:
            peli.append(elementos[16])
            cuenta+=1
    cuenta=0
    for elementos in lista_pelis["elements"]:
        if elementos[0] == lista_id[cuenta]:
            numerador+=elementos[17]
    promedio=round(numerador/numero_peliculas,2)
    texto="Las películas dirigidas por "+director+"son:"+peli+",la cantidad de peliculas dirigidas son"+numero_peliculas+"y tiene un promedio de calificación de"+promedio
                
    return texto



def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs= input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()
            
            if int(inputs[0])==2: #opcion 2
                lstcasting = loadCasting()

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                pass

            elif int(inputs[0])==5: #opcion 5
                pass

            elif int(inputs[0])==6: #opcion 6
                actor= input("Ingrese el nombre del actor del que desea consultar la información")
                registro_actor(lstmovies,lstcasting,actor)
                pass

            elif int(inputs[0])==7: #opcion 7
                pass


            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()