import re
import json

RELATIONSHIPS_NORMAL = [
    "pai",
    "mãe",
    "mae",
    "pais",
    "parentes",
    "filho",
    "filha",
    "irmão",
    "irmao",
    "irmã",
    "irma",
    "irmãos",
    "irmaos",
    "irmãs",
]

RELATIONSHIPS_PATERNO_MATERNO = [
    "tio",
    "tia",
    "primo",
    "prima",
    "avô",
    "avó",
    "avo",
    "bisavô",
    "bisavó",
    "bisavo",
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

# para ter a certeza que não foge nada...
pm = [" paterno", " materno", " paterna", " materna"]
rel = [x + y for x in RELATIONSHIPS_PATERNO_MATERNO for y in pm]
rel += RELATIONSHIPS_PATERNO_MATERNO
rel += RELATIONSHIPS_NORMAL

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

    # sort before the print
    dataNomes = dict(sorted(dataNomes.items()))
    dataApelidos = dict(sorted(dataApelidos.items()))

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

    return dataNomes, dataApelidos

def getFreqRelacoes(data):
    freqRelacoes = {}
    for d in data:
        l = len(d) if len(d) < 3 else 3 # tudo o que não for id, data e nome
        for name in d[l:]:
            name = name.lower()

            for r in rel:
                if r in name:
                    if r not in freqRelacoes:
                        freqRelacoes[r] = 1
                    freqRelacoes[r] += 1
                else:
                    pass

    print("\nRelações mais comuns:")
    for i in sorted(freqRelacoes.items(), key=lambda item: item[1], reverse=True):
        print(str(i[0]) + ":", i[1])

    return dict(sorted(freqRelacoes.items())) # sorting it

def toJSON(data, n):
    with open("processos.json", "w", encoding="utf8") as f:
        f.write("{\n")
        f.write("\t\"processos\": [\n")
        for i, d in enumerate(data):
            f.write("\t\t{\n")
            f.write("\t\t\t\"id\": " + str(d[0]) + ",\n")
            f.write("\t\t\t\"data\": \"" + str(d[1]) + "\",\n")
            f.write("\t\t\t\"nome\": \"" + str(d[2]) + "\",\n")
            f.write("\t\t\t\"relacoes\": [\n")
            for j, r in enumerate(d[3:5]):
                f.write("\t\t\t\t\"" + str(r) + "\"")
                if j != len(d[3:5]) - 1:
                    f.write(",")
                f.write("\n")

            f.write("\t\t\t]\n")
            # if there are observations, write them too
            if len(d) > 5:
                f.write(",\t\t\t\"observacoes\": [\n")
                for j, o in enumerate(d[5:]):
                    f.write("\t\t\t\t\"" + str(o) + "\"")
                    if j != len(d[5:]) - 1:
                        f.write(",")
                    f.write("\n")
                f.write("\t\t\t]\n")

            f.write("\t\t}")
            if i != len(data) - 1 and i < n:
                f.write(",")
            f.write("\n")
            if i >= n:
                break
        f.write("\t]\n")
        f.write("}\n")

def main():
    data = loadData()
    processosAno = getProcessosAno(data) # a
    nomesSec = getNomesSec(data) # b
    freqRelacoes = getFreqRelacoes(data) # c
    toJSON(data, 20) # d

    # test the created file
    #with open("processos.json", "r", encoding="utf8") as f:
        #data = json.load(f)
        #print(data)

if __name__ == "__main__":
    main()
