import re

RELATIONSHIPS = [
    "pai",
    "mãe",
    "filho",
    "filha",
    "irmão",
    "irmã",
    "tio",
    "tia",
    "primo",
    "prima",
    "avô",
    "avó",
    "neto",
    "neta",
    "cunhado",
    "cunhada",
    "sobrinho",
    "sobrinha",
    "sogro",
    "sogra",
    "genro",
    "nora",
    "padrasto",
    "madrasta",
    "enteado",
    "enteada",
]

def loadData():
    with open("processos.txt", "r", encoding="utf8") as f:
        data = f.readlines()
        data_parsed = []

        for l in data:
            l = l.strip()
            l = l.split("::")
            while "" in l:
                l.remove("")
            if l != []:
                data_parsed.append(l)

    return data_parsed

def getProcessosAno(data):
    processos = {}
    for d in data:
        year = int(d[1].split("-")[0]) # we want the year in an int
        if year in processos:
            processos[year] += 1
        else:
            processos[year] = 1

    print("\nAnos com mais processos:")
    for i in sorted(processos.items(), key=lambda item: item[1], reverse=True)[:5]:
        print("Ano:", str(i[0]) + "; processos:", i[1])


    return dict(sorted(processos.items())) # sorting it

def getNomesSec(data):
    dataNomes = {}
    dataApelidos = {}
    for d in data:
        l = len(d) if len(d) < 5 else 5
        century = (int(d[1].split("-")[0][:2])+1) # for example, 1653 -> 16+1 = 17 * 100 = 1700s
        if century not in dataNomes:
            dataNomes[century] = {}
        if century not in dataApelidos:
            dataApelidos[century] = {}
        for name in d[2:l]:
            name = name.split(" ")

            for n in name: # remove any digit
                if re.search(r"\d", n):
                    name.remove(n)
            
            for n in name: # remove any dot, for example "doc.danificado"
                if "." in n:
                    name.remove(n)

            try:
                name = [n.lower() for n in name] # lower case

                firstName = name[0]
                if "," in firstName:
                    firstName = firstName.split(",")[0] # remove the relationship part
                if firstName not in dataNomes[century]:
                    dataNomes[century][firstName] = 1
                dataNomes[century][firstName] += 1
                
                if len(name) > 1: # if they have a last name
                    lastName = name[-1]
                    if "," in lastName:
                        lastName = lastName.split(",")[0] # remove the relationship part
                    if lastName not in dataApelidos[century]:
                        dataApelidos[century][lastName] = 1
                    dataApelidos[century][lastName] += 1
            except:
                pass

    # get the 5 most used common names in each dict for century
    print("\nNomes mais comuns:")
    for d in dataNomes:
        print(d, sorted(dataNomes[d].items(), key=lambda item: item[1], reverse=True)[:5])
    print("\nApelidos mais comuns:")
    for d in dataApelidos:
        print(d, sorted(dataApelidos[d].items(), key=lambda item: item[1], reverse=True)[:5])



    for d in dataNomes:
        dataNomes[d] = dict(sorted(dataNomes[d].items()))
    for d in dataNomes:
        dataApelidos[d] = dict(sorted(dataApelidos[d].items()))

    return dict(sorted(dataNomes.items())),  dict(sorted(dataApelidos.items()))# sorting it

def main():
    data = loadData()
    processosAno = getProcessosAno(data) # a
    nomesSec = getNomesSec(data) # b

    #for i in nomesSec[0]: # first Name
    #    for j in nomesSec[0][i]:
    #        print(i, j, nomesSec[0][i][j])

    


if __name__ == "__main__":
    main()
