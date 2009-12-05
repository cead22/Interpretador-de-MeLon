#! /usr/bin/python
import Nodo

# incrementa en 1 el valor del elemento del diccionario indicado
def sumar(dicc,key,value):
	if (key in dicc):
		dicc[key] += value
	else:
		dicc[key] = value

# devuelve true si todos los elementos de la lista son iguales
# devuelve false en otro caso
def iguales(lista):
	if len(lista) == 1:
		return True
	for i in range(0,len(lista)-1):
		if lista[i] != lista[i+1]:
			return False
	return True

def revisar_patrones(dicc):
	for i in range(0,len(dicc.values())):
		if not (iguales(dicc[i].values())):
			return False
	return True

def recorrer_fun(nodo,dicc,index):
	if nodo.type == "lp": 
		if index in dicc: dicc[index] += 1
		else: dicc[index] = 1
	elif nodo.type == "arg2": index += 1
	if (nodo.izquierdo.__class__ == Nodo.Nodo):
		recorrer_recursivo(nodo.izquierdo,dicc,index)
	if (nodo.derecho.__class__ == Nodo.Nodo):
		recorrer_recursivo(nodo.derecho,dicc,index)
	return dicc

def recorrer_recursivo(nodo,dicc,index):
	if nodo.type == "FUN":
		return
	if nodo.type == "lp": 
		if index in dicc: dicc[index] += 1
		else: dicc[index] = 1
	elif nodo.type == "arg2": index += 1
	if (nodo.izquierdo.__class__ == Nodo.Nodo):
		recorrer_recursivo(nodo.izquierdo,dicc,index)
	if (nodo.derecho.__class__ == Nodo.Nodo):
		recorrer_recursivo(nodo.derecho,dicc,index)
	return dicc