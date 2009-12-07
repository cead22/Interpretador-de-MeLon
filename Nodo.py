#! /usr/bin/python
# estructura para crear arbol
# campos: tipo, hijo izquierdo (izquierdo), hijo derecho (derecho)
class Nodo:
	def __init__(self,type,izquierdo='',derecho=''):
		self.type = type
		#if izquierdo:
		self.izquierdo = izquierdo
		#else:
			#self.izquierdo = [ ]
		self.derecho = derecho
	def tostring(self):
		if (self.type == "sub" or self.type == "arg2" or self.type == "lp" or self.type == "lfe" or self.type == "arg"):
			return str(self.izquierdo)+' '+str(self.derecho)
		else:
			if (self.type == "no_terminal" or self.type == "CONSTANTE" or self.type == 'CONSTLV'):
				#return Nodo.tostring(self.izquierdo), Nodo.tostring(self.derecho)
				return Nodo.tostring(self.izquierdo)
			else:
				if(self.derecho == ''):
					if (self.type == ''):
						return '('+str(self.izquierdo)+')'
					else:
						return '('+str(self.type)+' '+str(self.izquierdo)+')'
				else:
					return '('+str(self.type)+' '+str(self.izquierdo)+' '+str(self.derecho)+')'
			
	def __str__(self):
		return str(Nodo.tostring(self))
