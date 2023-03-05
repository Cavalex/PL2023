def loadData():
    with open("processos.txt", "r", encoding="utf8") as f:
        data = f.readlines()
        data_parsed = []

        for l in data:
            l = l.strip()
            l = l.split("::")
            while "" in l:
                l.remove("")
            data_parsed.append(l)

    
    return data_parsed


def main():
    data = loadData()
    for d in data:
        print(d)

if __name__ == "__main__":
    main()
