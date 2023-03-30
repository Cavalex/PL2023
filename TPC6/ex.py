import re
import ply.lex as lex

states = (
    ('comment', 'exclusive'),
)

tokens = (
    'OPEN_COMMENT_MULTI_LINE',
    'CLOSE_COMMENT_MULTI_LINE',
    'COMMENT_MULTI_LINE',
    'OPEN_COMMENT_LINE',
    'CLOSE_COMMENT_LINE',
    'COMMENT_LINE',
    'FUNC',
    'FUNC_NAME',
    'PROGRAM',
    'PROGRAM_NAME',
    'IF',
    'WHILE',
    'FOR',
    'IN',
    'OP',
    'COMP',
    'ASSIGN',
    'TYPE',
    'COMMA',
    'SEMICOLON',
    'PAR_OPEN',
    'PAR_CLOSE',
    'BRACKET_OPEN',import sys
from ply.lex import lex

tokens = [
    'LB', 'RB', 'LC', 'RC', 'LP', 'RP', 
    'SUM', 'SUB', 'MUL', 'DIV', 'ASSIGN', 'RANGE', 'MOD',
    'EQUAL', 'DIF', 'NOT', 'LESS', 'GREATER', 'LESS_EQ', 'GREATER_EQ', 'IN',
    'VAR', 'NUMBER', 'SEMICOLON', 'COMMA', 'COMMENT',
    'IF', 'ELSE', 'ELIF',
    'WHILE', 'FOR', 'FOREACH',
    'TYPE',
    'FUNCTION', 'PROGRAM', 'PRINT'
]

t_ignore = f'\t\r'

#parêntesis
t_LB = r'\['
t_RB = r'\]'
t_LC = r'{'
t_RC = r'}'
t_LP = r'\('
t_RP = r'\)'

#ops
t_SUM = r'\+'
t_SUB = r'-'
t_MUL = r'\*' 
t_DIV = r'/'

def t_ASSIGN(t):
    r'='
    return t 

t_RANGE = r'\.\.(?=\d+)'

t_MOD = r'%'

#cond 
t_EQUAL = r'=='
t_DIF = r'!='
t_NOT = r'!'
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQ = r'<='
t_GREATER_EQ = r'>='
t_IN = r'in'

#conditionals
def t_IF(t):
    r'if '
    return t

def t_ELSE(t):
    r'else'
    return t

def t_ELIF(t):
    r'elif'
    return t
    

#loops
def t_WHILE(t):
    r'while'
    return t 
    
def t_FOR(t):
    r'for'
    return t
    
def t_FOREACH(t):
    r'foreach'
    return t

#types
def t_TYPE(t):
    r'int|double|string|char|float'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_PROGRAM(t):
    r'program'
    return t

def t_PRINT(t):
    r'print'
    return t

#id
def t_VAR(t):
    r'[a-z_]\w*'
    return t 

#number
def t_NUMBER(t):
    r'-?\d+'
    return t

t_SEMICOLON = r';'
t_COMMA = r','


#comments
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)' 
    return t

def t_comment(t):
    r'//.*'

def t_ANY_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_ANY_space(t):
    r'\s'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


fileName = sys.argv[1]
print("Opening " + fileName)
file = open(fileName).read()
lexer = lex()
lexer.input(file)
toks = []
for tok in lexer:
    toks.append(tok)
print("Tamanho da lista: " + str(len(toks))) 
print("Tokens: ")
for t in toks:
    print(t)
    'BRACKET_CLOSE',
    'SBRACKET_OPEN',
    'SBRACKET_CLOSE',
    'RETURNS',
    'NUMBER',
    'VAR'
)

t_PAR_OPEN = r'\('
t_PAR_CLOSE = r'\)'
t_BRACKET_OPEN = r'\{'
t_BRACKET_CLOSE = r'\}'
t_SBRACKET_OPEN = r'\['
t_SBRACKET_CLOSE = r'\]'
t_RETURNS = r'\.\.'
t_ASSIGN = r'\='
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_OP = r'[\+\-\*]'
t_TYPE = r'\b(int|boolean|float|double|long|string)\b'
t_FUNC_NAME = r'[a-z_]+\w*(?=\()'
t_PROGRAM_NAME = r'(?<=program\ )[a-z_]+\w*'
t_VAR = r'\w+'
t_NUMBER = r'\d+'

def t_FUNC(t):
    r'\bfunction\b'
    return t

def t_PROGRAM(t):
    r'\bprogram\b'
    return t

def t_WHILE(t):
    r'\bwhile\b'
    return t

def t_IF(t):
    r'\bif\b'
    return t

def t_FOR(t):
    r'\bfor\b'
    return t

def t_IN(t):
    r'\bin\b'
    return t

def t_COMP(t):
    r'<=|>=|<|>'
    return t

def t_OPEN_COMMENT_MULTI_LINE(t):
    r'\/\*'
    t.lexer.begin('comment')
    return t

def t_OPEN_COMMENT_LINE(t):
    r'\/\/'
    t.lexer.begin('comment')
    return t

def t_comment_CLOSE_COMMENT_MULTI_LINE(t):
    r'\*\/'
    t.lexer.begin('INITIAL')
    return t

def t_comment_CLOSE_COMMENT_LINE(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    return t

def t_comment_COMMENT_LINE(t):
    r'(?<=\/\/).*'
    return t

def t_comment_COMMENT_MULTI_LINE(t):
    r'(.|\n)*?(?=\*\/)'
    return t

def t_ANY_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

t_comment_ignore = ''
t_INITIAL_ignore = ' \t\n'

lexer = lex.lex()

data = '''

/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}

'''

lexer.input(data)


while tok := lexer.token():
    print(tok)