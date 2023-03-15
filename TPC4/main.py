import re
#import json # não é usado, só para testes

def cleanHeader(data):
    parsedList = []
    for t in data:
        parsedTuple = []
        for d in t:
            if not d:
                continue
            parsedTuple.append(d)
        parsedList.append(parsedTuple)
    return parsedList

def loadData(file):
    data = []
    with open("data/" + file, "r", encoding="utf8") as f:
        for line in f:
            data.append(line)
    return data

def parseData(data):
    dataParsed = []
    for i in range(len(data)):
        if i == 0:
            header = re.findall(r"([\w ]+)({\d+}|{\d+,\d+})?(::\w+)?", data[i])
            dataParsed.append(cleanHeader(header))
        else:
            result = re.findall(r"([\w ]+)", data[i])
            dataParsed.append(result)
    return dataParsed

def processData(data):
    nAlunos = len(data) - 1
    dataProcessed = []
    for i in range(1, nAlunos + 1):
        dataProcessed.append({})
        for j in range(len(data[0])):
            field = data[0][j]
            if len(field) >= 2: # then there's a range
                dataProcessed[-1][field[0]] = []
                lim = 0
                r = 0
                try: # to check if the field has a range or is just a number
                    fieldRange = field[1].split(",") 
                    lim = int(fieldRange[1][:-1])
                except IndexError: # if it's just a number
                    lim = int(field[1][1:-1])
                while r < int(lim):
                    try: # this way we can add until the end of the range without any problems
                        dataProcessed[-1][field[0]].append(int(data[i][j+r])) # doesnt work with A-F grades, obviously
                        r += 1
                    except IndexError: # since I already know the error that's gonna happen
                        break
            else:
                dataProcessed[-1][field[0]] = data[i][j] # because it's a list we have to select the last [0] of it
            if len(field) == 3: # now we modify the list we created above on len == 2
                func = field[2][2:]
                values = dataProcessed[-1][field[0]]
                fieldName = field[0] + "_" + func[0].upper() + func[1:]
                del dataProcessed[-1][field[0]] # to change the name of the field witht the func name
                if func == "sum" or func == "soma": # meti pt e en porque tem ambas as versões em alunos4 e 5...
                    dataProcessed[-1][fieldName] = sum(values)
                elif func == "avg" or func == "media":
                    dataProcessed[-1][fieldName] = sum(values)/len(values)
    return dataProcessed

def toJSON(data, file):
    if file[-3:] == "csv":
        file = file[:-4] + ".json"
    #with open("data/" + file, "w", encoding="utf8") as f:
    #    json.dump(data, f, indent=4, ensure_ascii=False)

    with open("out/" + file, "w+", encoding="utf8") as f:
        f.write("[\n")
        i = 0
        for a in data:
            f.write("\t{\n")
            j = 0
            for k, v in a.items():
                if "notas" in k.lower() and "_" not in k:
                    f.write(f"\t\t\"{k}\": {v}")
                else:
                    f.write(f"\t\t\"{k}\": \"{v}\"")
                j += 1
                if j < len(a):
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("\t}")
            i += 1
            if i < len(data):
                f.write(",\n")
            else:
                f.write("\n")
        f.write("]")

def main():
    fileList = [
        "alunos.csv",
        "alunos2.csv",
        "alunos3.csv",
        "alunos4.csv",
        "alunos5.csv",
    ]
    for file in fileList:
        file = file
        data = loadData(file)
        dataParsed = parseData(data)
        dataProcessed = processData(dataParsed) # from lists to dict here, ready to convert to json
        #print(dataProcessed)
        toJSON(dataProcessed, file)

if __name__ == "__main__":
    main()
