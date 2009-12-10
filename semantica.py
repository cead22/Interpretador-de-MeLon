#! /usr/bin/python
import Nodo,CLS,copy,sys
from excepcion import *
sys.setrecursionlimit(3000)
# Match
def match(nodo1,nodo2):
	print 'matching'
	print nodo1
	print nodo2
	# Fin de recursion
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

# Lookup
def lookup(clave,diccionario):
	try:
		if clave in diccionario:
			return diccionario[clave]
		#else: raise ParametrosError('Variable '+str(clave)+' no declarada')
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

# Cantidad de patrones de una Funcion
def cantidad_patrones(nodo):
	while (nodo.type != 'lp'):
		nodo = nodo.izquierdo
	global suma
	suma = 0
	tam_listapatron(nodo)
	return suma
	
# Apply
def apply(cls,nodo):
	for c in cls.clausura:
		comparar = match(c[0],nodo)
		if comparar:
			if isinstance(comparar,list):
				nuevo_env = copy.deepcopy(cls.env)
				for n in comparar:				
					extend(nuevo_env,valor(n[0]),n[1])
				return eval(c[1],extend(nuevo_env,str(valor(c[0])),nodo))
			else : return eval(c[1],extend(copy.deepcopy(cls.env),str(valor(c[0])),nodo))
	raise ParametrosError(' De matching')

	
# Obtener clausura de una funcion
def clausura(nodo,env,temp):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'lfe':
			temp.append((nodo.izquierdo,nodo.derecho))
		clausura(nodo.izquierdo,env,temp)
		clausura(nodo.derecho,env,temp)
	return CLS.CLS(env,temp)


# Obtener patrones de una lista de patrones
def patrones(nodo,listap):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'PATRON':

			listap.append(nodo)
		if isinstance(nodo.izquierdo,Nodo.Nodo):
			patrones(nodo.izquierdo,listap)
		if isinstance(nodo.derecho,Nodo.Nodo):
			patrones(nodo.derecho,listap)
	return listap

# Obtener cuerpo (listas de patrones y expresiones)
# de una funcion
def cuerpo(nodo,body):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'lfe':
			body.append((patrones(nodo.izquierdo,[]),nodo.derecho))
		cuerpo(nodo.izquierdo,body)
		cuerpo(nodo.derecho,body)
	return body


# Factorizar funcion
def factorizar(body):
	conjunto = []
	particion = {}
	clave = {}
	exp = {}
	p = 0
	q = 1
	for b in body:
		print b[0][0]
		conjunto.append(b[0][0])
	p = 0
	q = 1
	print 'len' ,len(conjunto)
	while p < len(conjunto):
		while q < len(conjunto):
			if match(conjunto[p],conjunto[q]) and match (conjunto[q],conjunto[p]):
				print 'conjunto',conjunto[p],conjunto[q],p,q
				if p in clave:
					if clave[p] in particion:
						particion[clave[p]].append(conjunto[q])
						
					else:
						particion[clave[p]] = [conjunto[q]]
					if clave[p] in exp:
						exp[clave[p]].append(body[p][1])
						exp[clave[p]].append(body[q][1])
					else:
						exp[clave[p]] = [body[p][1]]
						exp[clave[p]].append(body[q][1])
					clave[q] = p
					clave[p] = q

				elif q in clave:
					if clave[q] in particion:
						particion[clave[q]].append(conjunto[p])
					else:
						particion[clave[q]] = [conjunto[p]]
					if clave[q] in exp:
						exp[clave[q]].append(body[p][1])
						exp[clave[q]].append(body[q][1])
					else:
						exp[clave[q]] = [body[p][1]]
						exp[clave[q]].append(body[q][1])
					clave[p] = q
					clave[q] = p
  				else:
					particion[q] = [conjunto[q]]
					
					clave[q] = p
					clave[p] = p
			else:
				if p not in clave:
					clave[p] = p
					particion[p] = [conjunto[p]]
				if q not in clave:
					clave[q] = q
					particion[q] = [conjunto[q]]
			q += 1
		p +=1
	print particion , exp 
					
# Eval
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
				#factorizado = factorizar(cuerpo_fun)
			
				#fun_factorizada = factorizar(nodo)
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
			resultado = i + d
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
		
		elif nodo.type == 'MENOS' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = i - d
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado)) 

		elif nodo.type == 'NEGATIVO' :
			i = valor(eval(nodo.izquierdo,env))
			#if es_entero(i,1):		
			resultado = -i
			return Nodo.Nodo('NEGATIVO',resultado)
		
		elif nodo.type == 'PRODUCTO' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = i * d
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
		elif nodo.type == 'COCIENTE' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			if (d == 0):
				raise ParametrosError('Division por CERO') 
			else:				
				resultado = i / d
				return Nodo.Nodo('CONSTANTE',Nodo.Nodo('ENTERO',resultado))
		elif nodo.type == 'MENOR' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = (i<d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		
		elif nodo.type == 'MENOROIGUAL' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = (i <= d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'MAYOR' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			#if es_entero(i,d):
			resultado = (i > d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'MAYOROIGUAL' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = i >= d
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'IGUAL' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = (i == d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		
		elif nodo.type == 'DISTINTO' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = (i != d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'NO' :
			i = valor(eval(nodo.izquierdo,env))
			resultado = not(i)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'OR' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			resultado = (i or d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'AND' :
			i = valor(eval(nodo.izquierdo,env))
			d = valor(eval(nodo.derecho,env))
			#if es_booleano(i,d):
			resultado = (i and d)
			return Nodo.Nodo('CONSTANTE',Nodo.Nodo('BOOLEANO',str(resultado).upper()))
		elif nodo.type == 'VARIABLE':
			return lookup(str(valor(nodo.izquierdo)),env)
		elif nodo.type == 'LISTA':
			return Nodo.Nodo('LISTA',eval(nodo.izquierdo,env),eval(nodo.derecho,env))
	
		elif nodo.type == 'PATRON': return nodo
		elif nodo.type == 'LET':
			p = nodo.izquierdo.izquierdo
			e1 = nodo.izquierdo.derecho
			e2 = nodo.derecho
			env1 = extend(env,p,'fake')
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



		
