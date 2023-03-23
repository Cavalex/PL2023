import re
import ply.lex as lex

# List of token names.   This is always required
tokens = ("LEVANTAR", "POUSAR", "MOEDA", "NUMERO", "ABORTAR")

# Regular expression rules for simple tokens
t_LEVANTAR= r"(?i)levantar"
t_POUSAR= r"(?i)pousar"
t_ABORTAR = r"(?i)abortar"

# A Regular Expression for phone numbers
def t_NUMERO(t):
    r"(?i)t=(\d+)"
    t.value = t.value[2:].strip()
    return t

# A Regular Expression for coins
def t_MOEDA(t):
    r"(?i)(moeda)(\s\d+[c|e],*)+"
    t.value = t.value.strip()
    t.value = re.sub(r"(?i)moeda ", "", t.value)
    t.value = re.sub(r",","", t.value)
    t.value = re.split(r"\s", t.value)
    return t

# A Regular Expression to ignore spaces, commas and points
def t_ignore_SPACE_POINT_COMMA(t):
    r"[ ,.]+"
    pass
    # No return value. Token discarded 

# Track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    #probably should handle this better
    print(f"Command not recognized: {t.value}")
    t.lexer.skip(len(t.value))

# Build the lexer
lexer: lex.lexer = lex.lex()

def getCoinTotalValue(coins):
    total = 0
    for coin in coins:
        if coin == "1c":
            total += 0.01
        elif coin == "2c":
            total += 0.02
        elif coin == "5c":
            total += 0.05
        elif coin == "10c":
            total += 0.10
        elif coin == "20c":
            total += 0.20
        elif coin == "50c":
            total += 0.50
        elif coin == "1e":
            total += 1
        elif coin == "2e":
            total += 2
    return total

def getTroco(saldo):
    troco = []
    while saldo > 0:
        if saldo >= 2:
            troco.append("2e")
            saldo -= 2
        elif saldo >= 1:
            troco.append("1e")
            saldo -= 1
        elif saldo >= 0.5:
            troco.append("50c")
            saldo -= 0.5
        elif saldo >= 0.2:
            troco.append("20c")
            saldo -= 0.2
        elif saldo >= 0.1:
            troco.append("10c")
            saldo -= 0.1
        elif saldo >= 0.05:
            troco.append("5c")
            saldo -= 0.05
        elif saldo >= 0.02:
            troco.append("2c")
            saldo -= 0.02
        elif saldo >= 0.01:
            troco.append("1c")
            saldo -= 0.01
        saldo = round(saldo, 2) # para não ficar com saldo = 0.0000999999 -_-
    return troco

def main():
    on = False # phone is on/off
    phoneFlag = False
    saldo = 0 # available money

    while phoneFlag == False:
        try:
            text = input(">")
        except EOFError:
            break
        lexer.input(text)
        while True:
            result = ""
            tok = lexer.token()
            if not tok:
                break
            if tok.type == "LEVANTAR":
                result = "Erro, Telefone já está ligado!" if on else "Telefone ligou-se."
                on = True
            elif tok.type == "POUSAR":
                result = "Erro, Telefone já está desligado!" if not on else "Telefone desligou-se."
                on = False
                phoneFlag = True
            elif tok.type == "MOEDA":
                if not on:
                    result = "Erro, Telefone está desligado!"
                else:
                    coins = []
                    for coin in tok.value:
                        if coin in ["1c", "2c", "5c", "10c", "20c", "50c", "1e", "2e"]:
                            coins.append(coin)
                            result += f"Moeda {coin} aceite com sucesso! "
                        else:
                            result += f"Moeda {coin} não aceite! "
                    #print(coins)
                    saldo += getCoinTotalValue(coins)
                    result += f"Saldo disponível: {saldo}€"
            elif tok.type == "NUMERO":
                if not on:
                    result = "Erro, Telefone está desligado!"
                else:
                    number = tok.value
                    if len(number) == 9 and number[:2] != "00": # chamadas nacionais
                        if number[:3] in ["601", "641"]:
                            result = f"Número bloquado! {number}"
                        if number[0] == "2": # chamadas nacionais
                            if saldo >= 0.25:
                                saldo -= 0.25
                                result = f"Chamada efetuada com sucesso para {number}! Saldo disponível: {saldo}€"
                            else:
                                result = f"Saldo insuficiente para efetuar chamada para {number}! Saldo disponível: {saldo}€"
                        elif number[:3] == "800": # chamadas verdes, gratuitas
                            result = f"Chamada efetuada com sucesso para {number}! Saldo disponível: {saldo}€"
                        elif number[:3] == "808": # chamdas azuis, 10c
                            if saldo >= 0.10:
                                saldo -= 0.10
                                result = f"Chamada efetuada com sucesso para {number}! Saldo disponível: {saldo}€"
                            else:
                                result = f"Saldo insuficiente para efetuar chamada para {number}! Saldo disponível: {saldo}€"
                    elif number[:2] == "00":
                        if saldo >= 1.5:
                            saldo -= 1.5
                            result = f"Chamada efetuada com sucesso para {number}! Saldo disponível: {saldo}€"
                        else:
                            result = f"Saldo insuficiente para efetuar chamada para {number}! Saldo disponível: {saldo}€"
                    else:
                        result = f"Número inválido! {number}"
            elif tok.type == "ABORTAR":
                troco = getTroco(saldo)
                result = f"Troco = {troco} ; Volte Sempre! "
                saldo = 0 # why not xD
                phoneFlag = True
            print("maq: \"", result + "\"")
            if phoneFlag:
                break

if __name__ == "__main__":
    main()
