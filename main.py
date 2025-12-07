import cleandata
import genAlgo

GENERATION_SIZE = 100
POPULATION_SIZE = 10
STEPS = 10
MUTATION_CHANCE = 0.4
CROSSOVER_CHANCE = 0.7

class Main():
    df = cleandata.getDf()
    print(df.head())
    cleandata.showDf(df)


    pop = genAlgo.createPopulation(5,3)
    print(pop)

    genAlgo.run(df, GENERATION_SIZE, POPULATION_SIZE, STEPS, MUTATION_CHANCE, CROSSOVER_CHANCE)

