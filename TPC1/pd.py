import pandas as pd
import numpy as np # for the nan
from math import floor, ceil # for the rounding function

def ceil_to_multiple(number, multiple):
    return multiple * ceil(number / multiple)

def floor_to_multiple(number, multiple):
    return multiple * floor(number / multiple)

# load the dataset
def loadData():
    df = pd.read_csv("myheart.csv")
    return df

# distribution of having disease according to gender
def distSexo(df):

    doencaSexo = df.groupby(["sexo"])["temDoença"].sum().reset_index() # reset_index transforms from series into df
    soma = df.groupby(["sexo"])["temDoença"].count().reset_index()
    soma.rename(columns={"temDoença": "total"}, inplace=True)
    doencaSexo = pd.merge(doencaSexo, soma, on="sexo") # we merge them together
    doencaSexo["percentagem"] = round(doencaSexo.temDoença / doencaSexo.total * 100, 1) # percentage of infected people

    return doencaSexo

# distribution of having disease according to idade
def distIdade(df):
    df_idade = df[df.temDoença == 1] # only lines where there's disease
    minAge = df_idade.idade.min() # 28 -> 25
    maxAge = df_idade.idade.max() # 77 -> 80
    ageRange = 5
    doencaIdade = pd.cut(df_idade.idade, range(floor_to_multiple(minAge, ageRange), ceil_to_multiple(maxAge, ageRange)+1, ageRange)).value_counts()
    
    return doencaIdade

# distribution of having disease according to colesterol levels
def distColesterol(df):
    df_col = df[df.temDoença == 1] # only lines where there's disease
    df_col = df_col[df_col.colesterol != 0] # remove lines where colesterol is 0
    minCol = df_col.colesterol.min() # 100 -> 100
    maxCol = df_col.colesterol.max() # 610 -> 610
    colRange = 10
    doencaColesterol = pd.cut(df_col.colesterol, range(floor_to_multiple(minCol, colRange), ceil_to_multiple(maxCol, colRange)+1, colRange)).value_counts()
    
    return doencaColesterol

def main():
    df = loadData()
    doencaSexo = distSexo(df)
    print(doencaSexo)
    
    doencaIdade = distIdade(df)
    #print(doencaIdade)
    
    doencaColesterol = distColesterol(df)
    #print(doencaColesterol)

if __name__ == "__main__":
    main()


