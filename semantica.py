#! /usr/bin/python
import Nodo

# Match
def match(nodo1,nodo2):
	print 'MATCH\n -',nodo1,'\n -',nodo2
	# Fin de recursion
	if (not isinstance(nodo1,Nodo.Nodo)) and (not isinstance(nodo2,Nodo.Nodo)):
		print '- ',nodo1,'\n- ',nodo2
		return nodo1 == nodo2

	# Bajar si el nodo es no_terminal
	if nodo1.type == 'no_terminal' or nodo1.type == '' or nodo1.type == 'PATRON': return match(nodo1.izquierdo,nodo2)
	if nodo2.type == 'no_terminal' or nodo2.type == '' or nodo2.type == 'PATRON': return match(nodo2.izquierdo,nodo1)

	# Variables hacen match con todo
	if nodo1.type == 'VARIABLE' or nodo2.type == 'VARIABLE':
		print '- Variable\n -'
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
	#print 'CLAVE: ',clave
	#print 'DICCIONARIO',diccionario
	if clave in diccionario: return diccionario[clave]
	else: return False

# Eval
def eval(nodo,env,orientacion):
	if orientacion == 'izquierda': return eval(nodo.izquierdo,env)
	return eval(nodo.derecho,env)

# Apply
def apply(nodo1,nodo2,env):
	print env
	if 'clausura' in env:
		for c in env['clausura']:
			print '+C0\n +',c
			if match(nodo2,c[0]):
				return eval(c[1],extend(env,c[0],nodo2))
		print 'ERROR',env['clausura'],nodo2
		raise 'error'
	else:return apply(eval(nodo1,env),eval(nodo2,env),env)

	

# Eval
def eval(nodo,env):
	if isinstance(nodo,Nodo.Nodo):
		if isinstance(nodo.izquierdo,Nodo.Nodo):
			print nodo.type#,' -- ', nodo.izquierdo.type
	if not isinstance(nodo,Nodo.Nodo): return nodo
	if nodo.type == 'lp' or nodo.type == 'arg' : return eval(nodo.izquierdo,env)
	if nodo.type == 'FUN': return eval(nodo.izquierdo,env)
	if nodo.type == 'LISTAPATRON': return eval(nodo.izquierdo,env)
	if nodo.type == 'no_terminal': return eval(nodo.izquierdo,env)
	if nodo.type == 'sub': return eval(nodo.izquierdo,env)
	if nodo.type == '': return eval(nodo.izquierdo,env)
	if nodo.type == 'CONSTANTE': return nodo.izquierdo.izquierdo
	if nodo.type == 'MAS' : return eval(nodo.izquierdo,env) + eval(nodo.derecho,env)
	if nodo.type == 'VARIABLE' : return eval(lookup(str(eval(nodo.izquierdo,env)),env),env)
	if nodo.type == 'PATRON': return eval(nodo.izquierdo,env)
	if nodo.type == 'LET':
		valor_patron = str(nodo.izquierdo.izquierdo.izquierdo.izquierdo.izquierdo)
		env = extend(env,valor_patron,eval(nodo.izquierdo.derecho,env))
		#env = extend(env,valor_patron,nodo.izquierdo.derecho)
		p = eval(nodo.izquierdo.izquierdo,env)
		e1 = eval(nodo.izquierdo.derecho,env)
		e2 = eval(nodo.derecho,env)
		env1 = extend(env,str(p),'fake')
		v1 = eval(e1,env1)
		return eval(e2,replace(env1,str(p),v1))
	if nodo.type == 'arg2':
		if 'clausura' in env:
			extend(env,'clausura',env['clausura']+[(nodo.izquierdo,nodo.derecho)])
			print 'a\n    ',env['clausura']
		else:
			extend(env,'clausura',[(nodo.izquierdo.izquierdo.izquierdo,nodo.izquierdo.derecho)])
			print 'b\n    ',env['clausura'],'\n',nodo.izquierdo.izquierdo.izquierdo,'\n',nodo.izquierdo.derecho
	if nodo.type == 'APLICAR':
		apply(nodo.izquierdo,nodo.derecho,env)
		

		

		
