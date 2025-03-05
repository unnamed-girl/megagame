import random

def iteration(corvettes, station_hp, dice, attacks) -> int:
    count = 0
    while True:
        count += 1
        for _ in range(corvettes):
            if random.randint(1,12) == 1:
                station_hp -= 1

        for _ in range(attacks):
            if random.randint(1,dice) == 1:
                corvettes -= 1
        if corvettes <= 0:
            return station_hp, corvettes, count
        if station_hp <= 0:
            return station_hp, corvettes, count

BONUS_TO_DICE = [12,10,8,6,4,3,2,1,1,1,1,1,1,1,1,1]

STATIONS = [[1,1,2], [2,2,4], [5,3,8], [8,4,16], [13, 6, 25]]
STATION_LEVEL = 1
STATION_ATTACKS, STATION_BONUS, STATION_HP = STATIONS[STATION_LEVEL-1]
living_corvettes = []
station_hp = []
length = []
for i in range(1000):
    CORVETTES = 2
    s, c, l = iteration(CORVETTES, STATION_HP, BONUS_TO_DICE[STATION_BONUS], STATION_ATTACKS)
    living_corvettes.append(c)
    station_hp.append(s)
    length.append(l)

wins = sum([1 if hp>0 else 0 for hp in station_hp])
print("Wins %:", wins/len(station_hp))
print(sum(station_hp)/len(station_hp), sum(living_corvettes)/len(living_corvettes), sum(length)/len(length))