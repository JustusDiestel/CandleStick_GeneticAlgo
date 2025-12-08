import cleandata
import genAlgo
import matplotlib.pyplot as plt

GENERATION_SIZE = 100
POPULATION_SIZE = 10
STEPS = 10
MUTATION_CHANCE = 0.4
CROSSOVER_CHANCE = 0.7

df = cleandata.getDf()
print(df.head())

pop = genAlgo.createPopulation(POPULATION_SIZE, STEPS)
print(pop)

best, best_fit, history = genAlgo.run(
    df,
    GENERATION_SIZE,
    POPULATION_SIZE,
    STEPS,
    MUTATION_CHANCE,
    CROSSOVER_CHANCE,
)

print("BEST:", best)
print("FITNESS:", best_fit)
