#! /usr/bin/python
import Nodo,CLS,copy,sys
from excepcion import *
sys.setrecursionlimit(3000)
# Match
def match(nodo1,nodo2):
	if (not isinstance(nodo1,Nodo.Nodo)) and (not isinstance(nodo2,Nodo.Nodo)):
		return nodo1 == nodo2

	# Bajar si el nodo es no_terminal
	if nodo1.type == 'no_terminal' or nodo1.type == '' or nodo1.type == 'PATRON' or nodo1.type == 'sub' or nodo1.type == 'LISTAPATRON' or nodo1.type == 'lp': return match(nodo1.izquierdo,nodo2)
	if nodo2.type == 'no_terminal' or nodo2.type == '' or nodo2.type == 'PATRON' or nodo2.type == 'sub' or nodo2.type == 'LISTAPATRON' or nodo2.type == 'lp': return match(nodo2.izquierdo,nodo1)

	# Variables hacen match con todo
	if nodo1.type == 'VARIABLE' or nodo2.type == 'VARIABLE':
		return True

	# Constantes
	if nodo1.type == 'CONSTANTE' and nodo2.type == 'CONSTANTE':
		return match(nodo1.izquierdo.izquierdo,nodo2.izquierdo.izquierdo)

	# Entero
	if nodo1.type == 'ENTERO' and nodo2.type == 'ENTERO':
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Booleano
	if nodo1.type == 'BOOLEANO' and nodo2.type == 'BOOLEANO':
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Listavacia
	if nodo1.type == 'CONSTLV' and nodo2.type == 'CONSTLV':
		return True

	# Listas
	if nodo1.type == 'LISTA' and nodo2.type == 'LISTA':
		return comparar_listas(nodo1,nodo2,[])

	return False
def pa(nodo,env):
	a= []
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'LISTAPATRON':
			pa(nodo.izquierdo,env)
		if nodo.type == 'lp':
			if isinstance(nodo.derecho,Nodo.Nodo):
				print valor(eval(nodo.derecho,env))
				a.append(valor(eval(nodo.derecho,env)))
				if isinstance(nodo.izquierdo,Nodo.Nodo):
					pa(nodo.izquierdo,env)
				else: 
					print (valor(eval(nodo.derecho)))
			else:
				print valor(eval(nodo,env))
		else: print a
			
	
# Comparar Listas
def comparar_listas(lista1,lista2,tuplas):
	if match(lista1.izquierdo,lista2.izquierdo):
		tuplas.append((lista1.izquierdo,lista2.izquierdo))
		d1 = lista1.derecho
		d2 = lista2.derecho
		if d1.type == 'LISTA':
			if d2.type == 'LISTA':
				if not comparar_listas(lista1.derecho,lista2.derecho,tuplas):
					tuplas = []
			else: 
				if match(d1,d2): tuplas.append((d1,d2))
				else:
					tuplas = []
					return False
		elif d2.type == 'LISTA':
				if match(d1,d2): tuplas.append((d1,d2))
				else:
					tuplas = []
					return False
		else:
			if match(d1,d2): tuplas.append((d1,d2))
			else:
				tuplas =[]
				return False
		if tuplas == []: return False
		return tuplas
	else: return False
	
# Replace
def replace(diccionario,clave,valor):
	diccionario[clave] = valor
	return diccionario

# Extend
def extend(diccionario,clave,valor):
	diccionario[clave] = valor
	return diccionario

# lookup
def lookup(clave,diccionario):
	try:
		if clave in diccionario:
			if diccionario[clave]=='fake':
				raise ParametrosError('De recursion')
			else: return diccionario[clave]
		else:
			raise ParametrosError('De lookup')
	except ParametrosError, messag:
		messag = messag.messg
		print 'Error : ' + messag
			
# Eval
def eval(nodo,env,orientacion):
	if orientacion == 'izquierda': return eval(nodo.izquierdo,env)
	return eval(nodo.derecho,env)

# Valor
def valor(nodo):
	while isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'BOOLEANO':
			if nodo.izquierdo == 'TRUE': return True
			else: return False
		elif nodo.type != 'LISTA':
			nodo = nodo.izquierdo
		else:
			return str(valor(nodo.izquierdo))+'::'+str(valor(nodo.derecho))
	return nodo


	
# Apply
def apply(cls,nodo): 
	if isinstance(cls,CLS.CLS):
		for c in cls.clausura:
			comparar = match(c[0],nodo)
			if comparar:
				if isinstance(comparar,list):
					nuevo_env = copy.deepcopy(cls.env)
					for n in comparar:				
						extend(nuevo_env,valor(n[0]),n[1])
					return eval(c[1],extend(nuevo_env,str(valor(c[0])),nodo))
				else : return eval(c[1],extend(copy.deepcopy(cls.env),str(valor(c[0])),nodo))
	#Error de aplicar una No funcion
	else: raise ParametrosError('De aplicacion') 
	#Error de matching
	raise ParametrosError(' De matching')

	
# Obtener clausura de una funcion
def clausura(nodo,env,temp):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'lfe':
			temp.append((nodo.izquierdo,nodo.derecho))
		clausura(nodo.izquierdo,env,temp)
		clausura(nodo.derecho,env,temp)
	return CLS.CLS(env,temp)


def es_entero(x,y):
	if isinstance(x,int) and isinstance(y,int) and not(isinstance(x,bool)) and not(isinstance(y,bool)):
		return True
	else:
		return False 
def es_booleano(x,y):
	if isinstance(x,bool) and isinstance(y,bool):
		return True
	else:
		return False

def eval(nodo,env):
	try:
		if not isinstance(nodo,Nodo.Nodo): return nodo
		if nodo.type == 'arg': 
			eval(nodo.izquierdo,env)
			eval(nodo.derecho,env)
		if nodo.type == 'arg2': return eval(nodo.izquierdo,env)
		if nodo.type == 'lp':return nodo
		elif nodo.type == 'FUN': 
			
			#print 'In-Fun\n', cuerpo(nodo,[])
			#cuerpo_fun = cuerpo(nodo,[])
			#if len(cuerpo_fun[0][0]) != 1:
			#	print 'CUERPO',cuerpo_fun[0][0]
			#	factorizada = factorizar(cuerpo_fun)
			#	return eval(factorizada,env)
			#	fun_factorizada = factorizar(nodo)
			#else:
			return clausura(nodo,env,[])
			
			#return eval(nodo.izquierdo,env)
		elif nodo.type == 'LISTAPATRON': return nodo
		elif nodo.type == 'no_terminal': return eval(nodo.izquierdo,env)
		elif nodo.type == 'sub': return eval(nodo.izquierdo,env)
		elif nodo.type == '': return eval(nodo.izquierdo,env)
		elif nodo.type == 'CONSTANTE' or nodo.type == 'ENTERO':
			return nodo
		elif nodo.type == 'CONSTLV': 
			return nodo
		elif nodo.type == 'MAS' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = i + d
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
			else: raise ParametrosError('De tipo en los parametros de la suma') 
		
		elif nodo.type == 'MENOS' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = i - d
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
			else: raise ParametrosError('De tipo en los parametros de la resta') 

		elif nodo.type == 'NEGATIVO' :
			i = valor(eval(nodo.izquierdo,env))
			if es_entero(i,1):		
				resultado = -i
				return Nodo.Nodo('NEGATIVO',resultado)
			else: raise ParametrosError('De tipo en el parametro de NEGATIVO')
		
		elif nodo.type == 'PRODUCTO' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = i * d
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
			else: raise ParametrosError('De tipo en los parametros del PRODUCTO')
 
		elif nodo.type == 'COCIENTE' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				if (d == 0):
					raise ParametrosError('Division por CERO') 
				else:				
					resultado = i / d
					return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
			else: raise ParametrosError('De tipo de los parametros de la DIVISION')

		elif nodo.type == 'MENOR' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = (i<d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del <') 
		
		elif nodo.type == 'MENOROIGUAL' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = (i <= d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del =<')

		elif nodo.type == 'MAYOR' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = (i > d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del >')

		elif nodo.type == 'MAYOROIGUAL' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d):
				resultado = i >= d
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del >=')

		elif nodo.type == 'IGUAL' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
		
			if es_entero(i,d) or es_booleano(i,d):
				resultado = (i == d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del =')
		elif nodo.type == 'DISTINTO' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_entero(i,d) or es_booleano(i,d):
				resultado = (i != d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del <>')
		elif nodo.type == 'NO' :
			i = valor(eval(nodo.izquierdo,env))
			if es_booleano(i,True):
				resultado = not(i)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en la Negacion')
		elif nodo.type == 'OR' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_booleano(i,d):
				resultado = (i or d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del OR')
		elif nodo.type == 'AND' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if es_booleano(i,d):
				resultado = (i and d)
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
			else: raise ParametrosError('De tipo en los parametros del AND')
		elif nodo.type == 'VARIABLE':
			return lookup(str(valor(nodo.izquierdo)),env)
		elif nodo.type == 'LISTA':
			return Nodo.Nodo('LISTA',eval(nodo.izquierdo,env),eval(nodo.derecho,env))
	
		elif nodo.type == 'PATRON': return nodo
		elif nodo.type == 'LET':
			p = nodo.izquierdo.izquierdo
			e1 = nodo.izquierdo.derecho
			e2 = nodo.derecho
			env1 = extend(copy.deepcopy(env),str(valor(p)),'fake')
			v1 = eval(e1,env1)
			return eval(e2,replace(env1,str(valor(p)),v1))
		
		elif nodo.type == 'IF':
			if valor(eval(nodo.izquierdo.izquierdo ,env)) == True:
				return eval(nodo.izquierdo.derecho,env)
			else:
				return eval(nodo.derecho,env)
		elif nodo.type == 'lfe':
			return
		elif nodo.type == 'APLICAR':
				return apply(eval(nodo.izquierdo,env),eval(nodo.derecho,env))
			
	# Manejador de excepciones
	except ParametrosError, messag:
		messag = messag.messg
		print 'ERROR : ' + messag



		
