import random

PATTERN = ["hammer", "bullish_engulfing", "bearish_engulfing", "piercing", "dark_cloud_cover"]
def createPopulation(pop, steps):
    population = []
    for i in range(pop):
        population.append(createIndividual(steps))
    return population


def createIndividual(steps):
    individual = []
    pattern = ["hammer", "bullish_engulfing", "bearish_engulfing", "piercing", "dark_cloud_cover"]
    for j in range(steps):
        pat = random.randint(0, len(pattern) - 1)
        individual.append(pattern[pat])
    return individual


def mutation(individual, chance):
    if random.random() > chance:
        return individual

    action = random.choice(["replace", "insert", "delete"])

    if action == "replace":
        idx = random.randrange(len(individual))
        individual[idx] = random.choice(PATTERN)

    elif action == "insert":
        idx = random.randrange(len(individual) + 1)
        individual.insert(idx, random.choice(PATTERN))

    elif action == "delete":
        if len(individual) > 1:
            idx = random.randrange(len(individual))
            del individual[idx]

    return individual


def fitness(individual, df):
    BULLISH_PATTERNS = {"hammer", "bullish_engulfing", "piercing"}
    BEARISH_PATTERNS = {"bearish_engulfing", "dark_cloud_cover"}

    if len(individual) == 0:
        return -100000

    profit = 0.0
    position = None
    entry_price = 0.0
    trades = 0

    seq_index = 0        # Position im Individuum

    n = len(df)

    for i in range(n):
        current_pattern_name = individual[seq_index]

        if df.iloc[i][current_pattern_name] == 1:
            seq_index += 1

            if seq_index == len(individual):
                last_pattern = individual[-1]

                if last_pattern in BULLISH_PATTERNS:
                    signal = "BUY"
                elif last_pattern in BEARISH_PATTERNS:
                    signal = "SELL"
                else:
                    signal = None

                price = df.iloc[i]["close"]

                if signal == "BUY":
                    if position is None:
                        position = "LONG"
                        entry_price = price

                elif signal == "SELL":
                    if position == "LONG":
                        profit += price - entry_price
                        trades += 1
                        position = None
                        entry_price = 0.0

                seq_index = 0


    if position == "LONG":
        last_price = df.iloc[-1]["close"]
        profit += last_price - entry_price
        trades += 1

    # Strategien, die nie handeln, hart bestrafen
    if trades == 0:
        return -1000

    return profit

def crossover(p1, p2):
    min_len = min(len(p1), len(p2))
    if min_len < 2:
        return p1.copy()

    cut = random.randint(1, min_len - 1)
    child = p1[:cut] + p2[cut:]

    return child


def tournament_selection(population, df, k=3):
    competitors = random.sample(population, k)
    fitness_values = [(fitness(ind, df), ind) for ind in competitors]
    return max(fitness_values, key=lambda x: x[0])[1]

def run(df, generations_size, population_size, steps, mutation_chance, crossover_chance):
    population = createPopulation(population_size, steps)

    best_global = None
    best_global_fit = float("-inf")

    for gen in range(generations_size):
        new_population = []

        fitness_values = [(fitness(ind, df), ind) for ind in population]

        # Sortiert nach Fitness absteigend
        fitness_values.sort(key=lambda x: x[0], reverse=True)

        best = fitness_values[0][1]
        best_fit = fitness_values[0][0]

        if best_fit > best_global_fit:
            best_global = best.copy()
            best_global_fit = best_fit

        print(f"Generation {gen+1}: Best Fitness = {best_fit:.2f} Strategy = {best}")

        new_population.append(best.copy())

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, df)
            parent2 = tournament_selection(population, df)

            if random.random() <= crossover_chance:
                child = crossover(parent1, parent2)
            else:
                child = parent1.copy()

            child = mutation(child, mutation_chance)
            new_population.append(child)

        population = new_population

    print("BEST STRATEGY EVER:", best_global)
    print("FITNESS:", best_global_fit)

    return best_global, best_global_fit








