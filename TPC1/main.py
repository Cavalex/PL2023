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

    # count everything
    for p in people:
        totalMale = totalMale+1 if p.gender == "M" else totalMale
        totalFemale = totalFemale+1 if p.gender == "F" else totalFemale
        if p.disease == "1":
            if p.gender == "M":
                disMale += 1
            else:
                disFemale += 1

    print("\nDistribuição por género:")
    print("H com doença:", disMale, "de um total de", totalMale)
    print("com uma percentagem de", round(disMale/totalMale*100, 1), "% homens infetados")
    print("para um total de homens infetados sobre a a população total de", round(disMale/(totalMale+totalFemale)*100, 1), "%")
    print("M com doença:", disFemale, "de um total de", totalFemale)
    print("com uma percentagem de", round(disFemale/totalFemale*100, 1), "% mulheres infetadas")
    print("para um total de mulheres infetadas sobre a a população total de", round(disFemale/(totalMale+totalFemale)*100, 1), "%")

    return (disMale, disFemale, totalMale, totalFemale)

def distAge(people):
    ageSmallest = int(people[0].age)
    ageBiggest = int(people[0].age)

    # get the smallest and biggest ages
    for p in people:
        ageSmallest = int(p.age) if int(p.age) < ageSmallest else ageSmallest
        ageBiggest = int(p.age) if int(p.age) > ageBiggest else ageBiggest
    
    print(type(ageSmallest))
    print(type(ageBiggest))

    ageSmallest = floor_to_multiple(ageSmallest, 5) # se for 26 p.ex, passa para 25
    ageBiggest = ceil_to_multiple(ageBiggest, 5) # se for 76 p.ex, passa para 80

    # create the age groups
    ageGroups = {}
    for i in range(len(people)):
        age = int(people[i].age)
        ageGroup = floor_to_multiple(age, 5) # get the age group of this person
        ageGroup = str(ageGroup) + "-" + str(ageGroup+4)
        if ageGroup in ageGroups:
            ageGroups[ageGroup].append(people[i])
        else:
            ageGroups[ageGroup] = [people[i]]

    # count the number of people in each age group with disease
    for ageGroup in ageGroups:
        count = 0
        for p in ageGroups[ageGroup]:
            if p.disease == "1":
                count += 1
        ageGroups[ageGroup] = count

    # sort ageGroups by key
    ageGroups = dict(sorted(ageGroups.items(), key=lambda item: item[0]))

    print("\nDistribuição por faixa etária:")
    print(ageGroups)


def main():
    data = loadData() # 1
    people = loadPeople(data) # 1
    disMale, disFemale, totalMale, totalFemale = distGender(people) # 2
    distAge(people) # 3



if __name__ == "__main__":
    main()
