from person import Person
from math import floor, ceil
import matplotlib.pyplot as plt
import matplotlib

def ceil_to_multiple(number, multiple):
    return multiple * ceil(number / multiple)

def floor_to_multiple(number, multiple):
    return multiple * floor(number / multiple)

def strToPath(s):
    s = s.lower()
    s = s.replace(" ", "_")
    return s

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

    dist = {
        "M":totalMale,
        "F":totalFemale,
        "Total":totalFemale+totalMale,
        "M_infected":disMale,
        "F_infected":disFemale,
        "Total_infected":disMale+disFemale
    }
    #print(dist)
    return dist

def distAge(people):
    #print("\nDistribuição por faixa etária:")
    ageSmallest = int(people[0].age)
    ageBiggest = int(people[0].age)

    # get the smallest and biggest ages
    for p in people:
        ageSmallest = int(p.age) if int(p.age) < ageSmallest else ageSmallest
        ageBiggest = int(p.age) if int(p.age) > ageBiggest else ageBiggest
    
    #print("Youngest person is:", ageSmallest, "years old")
    #print("Oldest person is:", ageBiggest, "years old")

    ageSmallest = floor_to_multiple(ageSmallest, 5) # se for 28 p.ex, passa para 25
    ageBiggest = ceil_to_multiple(ageBiggest, 5) # se for 77 p.ex, passa para 80

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
    #print(ageGroups)

    return ageGroups

def distColesterol(people):
    #print("\nDistribuição por colesterol:")

    # remove people with 0 colesterol
    people_colesterol = []
    for p in people:
        if int(p.colesterol) > 0: 
            people_colesterol.append(p)
    colSmallest = int(people[0].colesterol)
    colBiggest = int(people[0].colesterol)

    # get the smallest and biggest ages
    for p in people_colesterol:
        colSmallest = int(p.colesterol) if int(p.colesterol) < colSmallest else colSmallest
        colBiggest = int(p.colesterol) if int(p.colesterol) > colBiggest else colBiggest
    
    #print("Person with lowest cholesterol:", colSmallest, "years old")
    #print("Person with highest cholesterol:", colBiggest, "years old")

    colSmallest = floor_to_multiple(colSmallest, 10) # se for 28 p.ex, passa para 25
    colBiggest = ceil_to_multiple(colBiggest, 10) # se for 77 p.ex, passa para 80

    # create the age groups
    colGroups = {}
    for i in range(len(people_colesterol)):
        col = int(people_colesterol[i].colesterol)
        colGroup = floor_to_multiple(col, 10) # get the age group of this person
        colGroup = str(colGroup) + "-" + str(colGroup+9)
        if colGroup in colGroups:
            colGroups[colGroup].append(people_colesterol[i])
        else:
            colGroups[colGroup] = [people_colesterol[i]]

    # count the number of people in each age group with disease
    for colGroup in colGroups:
        count = 0
        for p in colGroups[colGroup]:
            if p.disease == "1":
                count += 1
        colGroups[colGroup] = count

    # sort ageGroups by key
    colGroups = dict(sorted(colGroups.items(), key=lambda item: item[0]))
    #print(colGroups)

    return colGroups

def dictToTable(d_list):
    for d, title in d_list:
        l1 = 0
        l2 = 0
        for k, v in d.items():
            l1 = len(str(k)) if len(str(k)) > l1 else l1
            l2 = len(str(v)) if len(str(v)) > l2 else l2
        
        print(f"\n{title}:")
        print("_"*(l1+l2+9)) # the number 9 was semi random, found it by trial and error
        for p in d:
            print("|", p, " "*(l1-len(str(p))), "|", d[p], " "*(l2-len(str(d[p]))), "|")
        print("-"*(l1+l2+9))

def plotDist(d_list):
    for d, title in d_list:
        plt.close(fig="all") # close all previous plots

        matplotlib.rcParams.update({'font.size': 7}) # i think 10 is the default
        if len(d) > 10: # so we don't shrink the labels on the gender distribution
            plt.xticks(rotation=75) # rotate x axis labels

        plt.bar(d.keys(), d.values())

        plt.title(title)
        fileToSave = f"{strToPath(title)}.png"
        plt.savefig(fileToSave)

def main():
    data = loadData() # 1
    people = loadPeople(data) # 1
    #disMale, disFemale, totalMale, totalFemale = distGender(people) # 3
    genderGroups = distGender(people) # 3
    ageGroups = distAge(people) # 4
    colGroups = distColesterol(people) # 5
    dictToTable([
        (genderGroups, "Gender Distribution"), 
        (ageGroups, "Age Distribution"), 
        (colGroups, "Colesterol Distribution")
    ]) # 6 e 7
    plotDist([
        (genderGroups, "Gender Distribution"), 
        (ageGroups, "Age Distribution"), 
        (colGroups, "Colesterol Distribution")
    ]) # 8, draw the plots

if __name__ == "__main__":
    main()
