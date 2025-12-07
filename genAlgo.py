import random


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


def mutation(population, chance, pattern):
    for i in population:
        for j in range(len(i)):
            if random.random() <= chance:
                i[j] = random.choice(pattern)
    return population


def fitness(individual, df):
    BULLISH_PATTERNS = {"hammer", "bullish_engulfing", "piercing"}
    BEARISH_PATTERNS = {"bearish_engulfing", "dark_cloud_cover"}

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









