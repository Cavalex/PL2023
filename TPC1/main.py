from person import Person
from math import floor, ceil

def ceil_to_multiple(number, multiple):
    return multiple * ceil(number / multiple)

def floor_to_multiple(number, multiple):
    return multiple * floor(number / multiple)

def loadData():
    with open("myheart.csv", "r", encoding="utf8") as f:
        data = f.readlines()
        data_parsed = []

        for l in data:
            l = l.strip()
            l = l.split(",")
            data_parsed.append(l)
    
    return data_parsed

def loadPeople(data):
    people = []
    for i in range(1, len(data)):
        p = Person(i, data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5])
        people.append(p)

    return people

def distGender(people):
    disMale = 0
    disFemale = 0
    totalMale = 0
    totalFemale = 0
    for p in people:
        totalMale = totalMale+1 if p.gender == "M" else totalMale
        totalFemale = totalFemale+1 if p.gender == "F" else totalFemale
        if p.disease == "1":
            if p.gender == "M":
                disMale += 1
            else:
                disFemale += 1

    print("\nH com doença:", disMale, "de um total de", totalMale)
    print("com uma percentagem de", round(disMale/totalMale*100, 1), "% homens infetados")
    print("para um total de homens infetados sobre a a população total de", round(disMale/(totalMale+totalFemale)*100, 1), "%")
    print("\nM com doença:", disFemale, "de um total de", totalFemale)
    print("com uma percentagem de", round(disFemale/totalFemale*100, 1), "% mulheres infetadas")
    print("para um total de mulheres infetadas sobre a a população total de", round(disFemale/(totalMale+totalFemale)*100, 1), "%")

    return (disMale, disFemale, totalMale, totalFemale)

def distAge(people):
    pass

def main():
    data = loadData()
    people = loadPeople(data)
    disMale, disFemale, totalMale, totalFemale = distGender(people)

if __name__ == "__main__":
    main()
