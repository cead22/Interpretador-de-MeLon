#! /usr/bin/python
import lex	# herramienta para construir el lexer (PLY)
import sys

# palabras reservadas
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'fi' : 'FI',
    'let' : 'LET',
    'tel' : 'TEL',
    'fun' : 'FUN',
    'nuf' : 'NUF',
    'in' : 'IN',
    'true' : 'TRUE',
    'false' : 'FALSE'
    }

# tokens
tokens = ['VARIABLE','ENTERO','CORCHETEI',
	'CORCHETED','PARENTESISI','PARENTESISD','DDOSPUNTOS','MENOS',
	'MAS','PRODUCTO','COCIENTE','MENOROIGUAL','MENOR',
	'MAYOROIGUAL','MAYOR','IGUAL','DISTINTO','NOT',
	'OR','AND','FLECHA','PIPE'] + list(reserved.values())

# definicion de tokens
t_CORCHETEI  = r'\['
t_CORCHETED = r'\]'
t_PARENTESISI = r'\('
t_PARENTESISD = r'\)'
t_DDOSPUNTOS = r'::'
t_MENOS = r'-'
t_MAS = r'\+'
t_PRODUCTO = r'\*'
t_COCIENTE = r'/'
t_MENOROIGUAL = r'<='
t_MENOR = r'<'
t_MAYOROIGUAL = r'>='
t_MAYOR = r'>'
t_IGUAL = r'='
t_DISTINTO = r'<>'
t_NOT = r'!'
t_OR = r'\\/'
t_AND = r'/\\'
t_FLECHA = r'->'
t_PIPE = r'\|'

# definicion de ENTERO
def t_ENTERO(t):
	'[0-9][0-9]*'
	t.value = int(t.value)
	return t

# definicion de VARIABLE
def t_VARIABLE(t):
	'[a-zA-Z][a-zA-Z0-9_]*'
	# revisar palabras reservadas
	t.type = reserved.get(t.value,'VARIABLE')
	return t

# conteo de linea (error)
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# ignorar espacios y tabulaciones
t_ignore = ' \t\n'


# manejo de errores
def t_error(t):
	print "Error Lexicografico '%s' (linea" % t.value[0]+" %s" % t.lexer.lineno +", columna %s)" % t.lexpos
	sys.exit(-1)

# contruir lexer
melonlexer = lex.lex()
