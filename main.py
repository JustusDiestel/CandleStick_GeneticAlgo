import cleandata
import genAlgo


class Main():
    df = cleandata.getDf()
    print(df.head())
    cleandata.showDf(df)


    pop = genAlgo.createPopulation(5,3)
    print(pop)

