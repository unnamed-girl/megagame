import random
from dataclasses import dataclass

@dataclass
class Tradition:
    id: str
    needed: int

distribution = [1, 6, 4]
pool:list[Tradition] = []

drawn:list[Tradition] = []

completed = []

for i in range(len(distribution)):
    for b in range(distribution[i]):
        pool.append(Tradition((b,i+1), i+1))

def iteration():
    drawn = []
    for count in range(100):
        choice = random.choice(pool)
        drawn.append(choice)
        # print(choice)
        if sum([1 if d.id == choice.id else 0 for d in drawn]) == choice.needed:
            return count + 1, choice.needed

TEST = 100000
time = []
quality = []
for tests in range(TEST):
    result = iteration()
    time.append(result[0])
    quality.append(result[1])
print(sum(time)/TEST, sum(quality)/TEST)