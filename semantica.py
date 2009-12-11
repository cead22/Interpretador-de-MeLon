#! /usr/bin/python
import Nodo,CLS,copy,sys
from excepcion import *
sys.setrecursionlimit(3000)
# Match
def match(nodo1,nodo2,tuplas):
	print 'matching'
	print '  -',nodo1
	print '  -',nodo2
	# Fin de recursion
	if (not isinstance(nodo1,Nodo.Nodo)) and (not isinstance(nodo2,Nodo.Nodo)):
		return nodo1 == nodo2

	# Bajar si el nodo es no_terminal
	if nodo1.type == 'no_terminal' or nodo1.type == '' or nodo1.type == 'PATRON' or nodo1.type == 'sub' or (nodo1.type == 'LISTAPATRON' and tam_listapatron(Nodo.Nodo('lfe',nodo1)) == 1 ) or nodo1.type == 'lp': return match(nodo1.izquierdo,nodo2,tuplas)
	if nodo2.type == 'no_terminal' or nodo2.type == '' or nodo2.type == 'PATRON' or nodo2.type == 'sub' or (nodo2.type == 'LISTAPATRON' and tam_listapatron(Nodo.Nodo('lfe',nodo2)) == 1) or nodo2.type == 'lp': return match(nodo2.izquierdo,nodo1,tuplas)

	# Variables hacen match con todo
	if nodo1.type == 'VARIABLE' or nodo2.type == 'VARIABLE':
		return True

	# Constantes
	if nodo1.type == 'CONSTANTE' and nodo2.type == 'CONSTANTE':
		return match(nodo1.izquierdo.izquierdo,nodo2.izquierdo.izquierdo,tuplas)

	# Entero
	if nodo1.type == 'ENTERO' and nodo2.type == 'ENTERO':
		return match(nodo1.izquierdo,nodo2.izquierdo,tuplas)

	# Booleano
	if nodo1.type == 'BOOLEANO' and nodo2.type == 'BOOLEANO':
		return match(nodo1.izquierdo,nodo2.izquierdo,tuplas)

	# Listavacia
	if nodo1.type == 'CONSTLV' and nodo2.type == 'CONSTLV':
		return True

	# Listas
	if nodo1.type == 'LISTA' and nodo2.type == 'LISTA':
		return comparar_listas(nodo1,nodo2,tuplas)

	return False
	
# Comparar Listas
def comparar_listas(lista1,lista2,tuplas):
	if match(lista1.izquierdo,lista2.izquierdo,tuplas):
		tuplas.append((lista1.izquierdo,lista2.izquierdo))
		d1 = lista1.derecho
		d2 = lista2.derecho
		print 'listas \n  +',lista1,'\n  +',lista2,'\n  +',tuplas,'\n  +',d1.type,'\n  +',d2.type
		if d1.type == 'LISTA':
			if d2.type == 'LISTA':
				print 'tuplas internas', comp
				comp = comparar_listas(d1,d2,tuplas)
				if not comp:
					tuplas = []
				else:
					#tuplas += comp
					for c in comp:
						tuplas.append(comp[c])
					#return tuplas
			else: 
				if match(d1,d2,tuplas): tuplas.append((d1,d2))
				else:
					tuplas = []
					return False
		elif d2.type == 'LISTA':
				if match(d1,d2,tuplas): tuplas.append((d1,d2))
				else:
					tuplas = []
					return False
		else:
			if match(d1,d2,tuplas):
				tuplas.append((d1,d2))
			else:
				tuplas =[]
				return False
		if tuplas == []: 
			return False
		print tuplas#[0][0],tuplas[0][1],tuplas[1][0],tuplas[1][1]
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
			raise ParametrosError('De lookup ('+clave+')')
	except ParametrosError, messag:
		messag = messag.messg
		print 'Error : ' + messag
		sys.exit(-1)

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
			comparar = match(c[0],nodo,[])
			if comparar:
				print 'MATCHEO\n  =',c[0],'\n  =',nodo,isinstance(comparar,list)
				if isinstance(comparar,list):
					nuevo_env = copy.deepcopy(cls.env)
					for n in comparar:				
						extend(nuevo_env,valor(n[0]),n[1])
					return eval(c[1],extend(nuevo_env,str(valor(c[0])),nodo))
				else : 
					print 'here'
					return eval(c[1],extend(copy.deepcopy(cls.env),str(valor(c[0])),nodo))
	#Error de aplicar una No funcion
	#else: raise ParametrosError('De aplicacion') 
	#Error de matching
	#raise ParametrosError(' De matching')

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
		if nodo.izquierdo.izquierdo.type == 'PATRON':
			primer_patron =  copy.deepcopy(nodo.izquierdo.izquierdo) #copy.deepcopy(nodo.izquierdo.izquierdo)
			nodo.izquierdo =  nodo.derecho #copy.deepcopy(nodo.derecho)
			nodo.derecho = ''
			return (primer_patron, nodo)
		else:
			abuelo = nodo
			papa =  abuelo.izquierdo
			hijo = papa.izquierdo
			while hijo.type != 'PATRON':
				abuelo = papa
				papa = hijo
				hijo = hijo.izquierdo
			primer_patron = copy.deepcopy(hijo)
			hijo = ''
			papa.izquierdo = ''
			abuelo.izquierdo = ''
			papa = ''
			abuelo.izquierdo = abuelo.derecho
			abuelo.derecho = ''

			return (primer_patron,nodo)
	return

def tam_listapatron(nodo):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'lfe':
			res = tlp(nodo.izquierdo,[])
			return res
		else:
			return tam_listapatron(nodo.izquierdo)

def tlp(nodo,t):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'LISTAPATRON':
			nodo = nodo.izquierdo
			print nodo.izquierdo.type
		if nodo.type == 'lp':
			if nodo.izquierdo.type == 'PATRON':
				t.append(1)
			else :
				tlp(nodo.izquierdo,t)
				if isinstance(nodo.derecho,Nodo.Nodo) and nodo.derecho.type == 'PATRON':
					t.append(1)
				else:
					tlp(nodo.izquierdo,t)
	return len(t)
			


# Obtener cuerpo (listas de patrones y expresiones)
# de una funcion
def cuerpo(nodo,body):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'lfe':
			body.append((patrones(copy.deepcopy(nodo.izquierdo),[]),copy.deepcopy(nodo.derecho)))
		cuerpo(nodo.izquierdo,body)
		cuerpo(nodo.derecho,body)
	return body

#Lista de patrones sin el primero
def resto_de_patrones(nodo):
	if nodo.izquierdo.izquierdo.type == 'PATRON':
		nodo.izquierdo.izquierdo = copy.deepcopy(nodo.derecho)
		nodo.derecho = ''
		return nodo
	else:
		abuelo,papa,hijo = nodo,nodo.izquierdo,nodo.izquierdo.izquierdo
		while hijo.izquierdo != 'PATRON':
			abuelo = papa
			papa = hijo
			hijo = hijo.izquierdo
		papa.izquierdo = copy.deepcopy(papa.derecho)
		papa.derecho = ''
		return nodo

# Factorizar funcion
def factorizar(body):
	conjunto = []
	particion = {}
	clave = {}
	exp = {}
	pat = {}
	p,q,i,j,k = 0,1,0,0,0
	for b in body:
		conjunto.append(b[0][0])
	clave[0] = 0
	if len(conjunto) == 1:
		particion[0] = [conjunto[0]]
		exp[0] = [body[0][1]]
		pat[0] = [body[0][0][1]]
	while p < len(conjunto):
		q = p + 1
	       	while q < len(conjunto):
	       		if match(conjunto[p],conjunto[q],[]) and match (conjunto[q],conjunto[p],[]):
	       			clave[q] = p
	       			if p in particion and conjunto[q] not in particion[p]:
	       				particion[p].append(conjunto[q])
					pat[p].append(body[q][0][1])
	       			else:
	       				particion[p] = [conjunto[q]]
					pat[p] = [body[p][0][1]]
	       			if p in exp and body[q][1] not in exp[p]:
	       				print 'abcdefg'
	       				exp[p].append(body[q][1])
					if len(body[q][0]) == 1:
						pat[p].append(body[q][0][1])
					else:
						pat[p].append(body[q][0][1])
	       			else:
	       				exp[p] = [body[q][1]]
					if len(body[q][0]) == 1:
						pat[p] = [body[q][0][1]]
					else:
						pat[p] = [body[q][0][1]]
	       			exp[p].append(body[p][1])
				if len(body[p][0]) == 1:
					pat[p].append(body[p][0][1])
				else:
					pat[p].append(body[p][0][1])
#			else:
# 				if q not in clave:
# 					clave[q] = max(clave.keys())+1
# 					particion[clave[q]] = [conjunto[q]]
# 					pat[clave[q]] = [body[q][0][1]]
# 					exp[clave[q]] = [body[q][1]]
	       		q += 1
		p += 1
	
	p = 0
	print 'CJTO',conjunto
	while p < len(conjunto):
		if p not in clave:
			print ' keys', exp.keys()
			if len(exp.keys()) == 0:
				cl = 0
			else:
				cl = max(exp.keys())+1
			print 'cl', cl
			particion[cl] = [conjunto[p]]
			exp[cl] = [body[p][1]]
			pat[cl] = [body[p][0][1]]
			print 'lllll',len(exp)
		p +=1
			
	
	#print 'PARTICION\n *',particion, '\nEXP\n *',exp, '\nPAT\n *',pat
	#print 'PARTICION\n *',particion,'\n *',particion[0][0] ,'\n *', particion[1][0],'\n *', particion[2][0]# ,'\nEXP\n *',exp,'\n *', exp[0][0],'\n *', exp[0][1],'\n *', exp[1][0],'\n *', exp[1][1]#,'\n *', exp[2][0]
	#print 'PARTICION\n *',particion,'\n *',particion[0][0],'\n *', particion[1][0]# ,'\n *','\nEXP\n *',exp,'\n *', exp[0][0],'\n *', exp[0][1] ,'\n *', exp[1][0]#,'\n *', exp[1][1]
	#i = 0
	#j = 0
	#k = 0
	#print '\nPAT\n *',pat,'\n *', pat[0][0],'\n *', pat[0][1],'\n *', pat[1][0],'\n *', pat[2][0]
	#print 'EXP\n *', exp, '\n *',exp[0][0],'\n *', exp[0][1],'\n *', exp[1][0],'\n *', exp[2][0]
	#print 'ccc',conjunto,'\n *',conjunto[0],'\n *', conjunto[1],'\n *', conjunto[2],'\n *', conjunto[3],'\n * BODY',body[0][0][1]
	factorizada = Nodo.Nodo('FUN',0)
	arboles = []
	temp = 0
	while i < len(particion):
		j = 0
		print 'iii', i
		while j < len(exp[i]):
			print 'i,j', i,j
			if j == 0:
				temp = Nodo.Nodo('FUN',Nodo.Nodo('arg',Nodo.Nodo('arg2',Nodo.Nodo('lfe',pat[i][j],exp[i][j]))))
				arg = temp.izquierdo
				#print 'tttt', temp
			else:
				arg.derecho = Nodo.Nodo('arg',Nodo.Nodo('arg2',Nodo.Nodo('lfe',pat[i][j],exp[i][j])))
				arg = arg.derecho
				#print 'tttt', temp
			j += 1
		arboles.append(temp)
		#print 'TEMP' , temp
		i += 1
	
	
	while k < len(particion):
		if k == 0:
			temp = Nodo.Nodo('FUN',Nodo.Nodo('arg',Nodo.Nodo('arg2',Nodo.Nodo('lfe',Nodo.Nodo('LISTAPATRON',Nodo.Nodo('lp',particion[k][0])),arboles[k]))))
			arg = temp.izquierdo
		else:
			print 'arg' ,arg
			arg.derecho = Nodo.Nodo('arg',Nodo.Nodo('arg2',Nodo.Nodo('lfe',Nodo.Nodo('LISTAPATRON',Nodo.Nodo('lp',particion[k][0])),arboles[k])))
			arg = arg.derecho
			print 'arg',arg
		k += 1
	#print 'DEF',temp
	return temp
				    

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
			#print 'In-Fun\n', nodo
			cuerpo_fun = cuerpo(nodo,[])
			#print 'CUERPO','\n',cuerpo_fun,'\n^^^','\n',cuerpo_fun[0][0][1]
			#if len(cuerpo_fun[0][0]) != 1:
			#print 'AQUI' ,nodo
			t = tam_listapatron(nodo)
			print 'tamano',t
			if t != 1:
				factorizada = factorizar(cuerpo_fun)
				#print 'tamano body', len(cuerpo_fun)
				#if len(cuerpo
				#print 'CUERPO',cuerpo_fun[0][0]
				#print 'CLAUSURA REYNA',  clausura(factorizada,env,[])
				print 'FACTORIZADA\n >>>',factorizada
				# c =  clausura(copy.deepcopy(factorizada),copy.deepcopy(env),[])
# 				print c
#  				print '\n',c.clausura[0][0],'  ---  ',c.clausura[0][1],'\n'
#  				print '\n',c.clausura[1][0],'  ---  ',c.clausura[1][1],'\n'
#  				print '\n',c.clausura[2][0],'  ---  ',c.clausura[2][1],'\n'
#  				print '\n',c.clausura[3][0],'  ---  ',c.clausura[3][1],'\n'
				return clausura(factorizada,env,[])
				#fun_factorizada = factorizar(nodo)
			else:
				#print 'FUNCION QUE QUEDO' ,nodo
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
			if p.izquierdo.type == 'LISTA':
				print 'sup duc quad'
				tuplas_look = match(p.izquierdo,e1,[])
				print 'look', tuplas_look
				print '  -',tuplas_look[0][0]
				print '  -',tuplas_look[0][1]
				print '  -',tuplas_look[1][0]
				print '  -',tuplas_look[1][1]
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
		print 'Error : ' + messag
		sys.exit(-1)



		
