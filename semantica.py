#! /usr/bin/python
import Nodo

# Match
def match(nodo1,nodo2):
	#print 'MATCH\n -',nodo1.type,'\n -',nodo2.type
	# Fin de recursion
	if (not isinstance(nodo1,Nodo.Nodo)) and (not isinstance(nodo2,Nodo.Nodo)):
		#print '- ',nodo1,'\n- ',nodo2
		return nodo1 == nodo2

	# Bajar si el nodo es no_terminal
	if nodo1.type == 'no_terminal' or nodo1.type == '' or nodo1.type == 'PATRON' or nodo1.type == 'sub' or nodo1.type == 'LISTAPATRON' or nodo1.type == 'lp': return match(nodo1.izquierdo,nodo2)
	if nodo2.type == 'no_terminal' or nodo2.type == '' or nodo2.type == 'PATRON' or nodo2.type == 'sub' or nodo2.type == 'LISTAPATRON' or nodo2.type == 'lp': return match(nodo2.izquierdo,nodo1)

	# Variables hacen match con todo
	if nodo1.type == 'VARIABLE' or nodo2.type == 'VARIABLE':
		#print '- Variable\n -'
		return True

	# Constantes
	if nodo1.type == 'CONSTANTE' and nodo2.type == 'CONSTANTE':
		print '- Constante\n -'
		print '(',nodo1.type,' ',nodo2.type,')\n'
		return match(nodo1.izquierdo.izquierdo,nodo2.izquierdo.izquierdo)

	# Entero
	if nodo1.type == 'ENTERO' and nodo2.type == 'ENTERO':
		print '- Entero\n -'
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Booleano
	if nodo1.type == 'BOOLEANO' and nodo2.type == 'BOOLEANO':
		print '- Booleano\n -'
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Listavacia
	if nodo1.type == 'CONSTLV' and nodo2.type == 'CONSTLV':
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Listas
	if nodo1.type == 'LISTA' and nodo2.type == 'LISTA':
		print 'BLAH'
		return match(nodo1.izquierdo,nodo2.izquierdo) and  match(nodo1.derecho,nodo2.derecho)

	return False

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
	if clave in diccionario: return diccionario[clave]
	else: raise 'ERROR: variable '+clave+' no definida' 

# Eval
def eval(nodo,env,orientacion):
	if orientacion == 'izquierda': return eval(nodo.izquierdo,env)
	return eval(nodo.derecho,env)

# Valor
def valor(nodo):
	while isinstance(nodo,Nodo.Nodo):
		nodo = nodo.izquierdo
	return nodo

# Apply
def apply(nodo1,nodo2,env):
	#print 'APPLY',nodo1.type,nodo2
	if 'clausura' in env:
		#print 'APPLY',nodo1,nodo2
		#print env
		i=555
		for c in env['clausura']:
			#print '+C0\n +',c[0],'\n +',nodo2,'\n +',env['clausura']
			if match(nodo2,c[0]):
				#print 'Macheo',nodo2,c[0]
				return eval(c[1],extend(env,str(valor(c[0])),valor(nodo2)))
			i+=111
		print 'ERROR',c[0],nodo2
		n = c[0]
		print n.type, nodo2.type
		while isinstance(n,Nodo.Nodo):
			print n.type
			n = n.izquierdo
		raise 'AA'
	else:return apply(eval(nodo1,env),eval(nodo2,env),env)

	

# Eval
def eval(nodo,env):
	if not isinstance(nodo,Nodo.Nodo): return nodo
	if nodo.type == 'lp' or nodo.type == 'arg' or nodo.type == 'arg2': return eval(nodo.izquierdo,env)
	elif nodo.type == 'FUN': return eval(nodo.izquierdo,env)
	elif nodo.type == 'LISTAPATRON': return eval(nodo.izquierdo,env)
	elif nodo.type == 'no_terminal': return eval(nodo.izquierdo,env)
	elif nodo.type == 'sub': return eval(nodo.izquierdo,env)
	elif nodo.type == '': return eval(nodo.izquierdo,env)
	elif nodo.type == 'CONSTANTE': return nodo.izquierdo.izquierdo
	elif nodo.type == 'CONSTLV': 
		#print nodo.izquierdo
		return '[]'
	elif nodo.type == 'MAS' :
		resultado = eval(nodo.izquierdo,env) + eval(nodo.derecho,env)
		print resultado
	elif nodo.type == 'VARIABLE' : return eval(lookup(str(valor(nodo.izquierdo)),env),env)
	elif nodo.type == 'PATRON': return eval(nodo.izquierdo,env)
	elif nodo.type == 'LET':
		valor_patron = str(nodo.izquierdo.izquierdo.izquierdo.izquierdo.izquierdo)
		env = extend(env,valor_patron,nodo.izquierdo.derecho)
		p = nodo.izquierdo.izquierdo
		e1 = nodo.izquierdo.derecho
		e2 = nodo.derecho
		env1 = extend(env,p,'fake')
		v1 = eval(e1,env1)
		return eval(e2,replace(env1,str(valor(p)),v1))
	elif nodo.type == 'lfe':
		#print 'LFE \n ===>', nodo.derecho
		if 'clausura' in env:
			extend(env,'clausura',env['clausura']+[(str(valor(nodo.izquierdo.izquierdo.izquierdo)),nodo.izquierdo.izquierdo.derecho)])
			#print 'a'
		else:
			extend(env,'clausura',[(nodo.izquierdo,nodo.derecho)])
			#print 'b'
	elif nodo.type == 'APLICAR':
		#print 'APLICAR',nodo.izquierdo,nodo.derecho
		apply(nodo.izquierdo,nodo.derecho,env)
		

		

		
