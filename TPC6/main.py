import re
import ply.lex as lex


tokens = (
    "M_COMMENT",
    "S_COMMENT",
    "L_B",
    "R_B",
    "L_C",
    "R_C",
    "L_P",
    "R_P",
    "TYPE",
    "VAR",
    "NUMBER",
    "EQUALS",
    "OPERATION",
    "GT",
    "LT",
    "GTE",
    "LTE",
    "NOT",
    "COMMA",
    "SEMICOLON",
    "FUNC",
    "PROGRAM",
    "PRINT",
    "IF",
    "ELSE",
    "ELIF",
    "WHILE",
    "FOR",
)
t_L_B = r"\["
t_R_B = r"\]"
t_L_C = r"\{"
t_R_C = r"\}"
t_L_P = r"\("
t_R_P = r"\)"
t_EQUALS = r"="
t_GT = r">"
t_LT = r"<"
t_GTE = r">="
t_LTE = r"<="
t_NOT = r"!"
t_COMMA = r","
t_SEMICOLON = r";"




def t_FUNC(t):
    r"function"
    return t

def t_PROGRAM(t):
    r"program"
    return t

def t_PRINT(t):
    r"print"
    return t

def t_IF(t):
    r"if"
    return t

def t_ELSE(t):
    r"else"
    return t

def t_ELIF(t):
    r"elif"
    return t

def t_WHILE(t):
    r"while"
    return t

def t_FOR(t):
    r"for"
    return t




def t_TYPE(t):
    r"int|bool|double|string|char|float"
    return t

def t_VAR(t):
    r'[a-z_]\w*'
    return t 

def t_NUMBER(t):
    r'-?\d+'
    return t

def t_OPERATION(t):
    r"\+|-|\*|%|\*\*"
    return t




def t_M_COMMENT(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")
    return t

def t_S_COMMENT(t):
    r"//.*"
    t.lexer.lineno += 1
    return t


# A Regular Expression to ignore spaces, commas and points
def t_ignore_SPACE_POINT_COMMA(t):
    r"[ ,.\t]+"
    pass

# Track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    #probably should handle this better
    print(f"Command not recognized: {t.value}")
    t.lexer.skip(len(t.value))

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
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
