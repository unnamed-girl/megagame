from dataclasses import dataclass
import random

@dataclass
class CombatantStats:
    name:str
    bonus:int
    attack:int
    max_hp:int
    cost: int
    size: float
    def __post_init__(self):
        self.dice_size =[12,10,8,6,4,3,2,1][min(7,self.bonus)]
        self.average_hits = self._average_hits()
    def roll_hits(self) -> int:
        hits = 0
        for _ in range(self.attack):
            if random.randint(1, self.dice_size) <= 2:
                hits += 1
        return hits
    def _average_hits(self) -> float:
        return 2 * self.attack / self.dice_size
    def modified_copy(self, extra_attack=0, extra_hp=0) -> "CombatantStats":
        return CombatantStats(name = self.name, attack = self.attack + extra_attack, bonus = self.bonus, max_hp= self.max_hp + extra_hp, cost = self.cost, size = self.size)
    def __str__(self) -> str:
        return self.name
    def __mul__(self, other):
        return [self]*other
    def __rmul__(self, other):
        return [self]*other

class Army:
    def __init__(self, *forces) -> None:
        self.forces:list[CombatantStats] = []
        for force in forces:
            if hasattr(force, "__iter__"):
                self.forces.extend(force)
            else:
                self.forces.append(force)
        self.damage_overflow = 0
    def damage(self, damage:float):
            self.damage_overflow += damage
            while len(self.forces) > 0 and self.damage_overflow >= self.forces[0].max_hp:
                self.damage_overflow -= self.forces[0].max_hp
                self.forces.pop(0)
    def is_destroyed(self) -> bool:
        return self.forces.__len__() == 0
    def get_hits(self) -> int:
        return sum([ship.roll_hits() for ship in self.forces])
    def average_hits(self) -> float:
        return sum(ship.average_hits for ship in self.forces)
    def __repr__(self) -> str:
        return str([str(ship) for ship in self.forces])
    def __iter__(self):
        yield from self.forces

def simulate(one, two, roll_dice=True):
    one = Army(one)
    two = Army(two)
    while True:
        if roll_dice:
            one_hits = one.get_hits()
            two_hits = two.get_hits()
        else:
            one_hits = one.average_hits()
            two_hits = two.average_hits()
        one.damage(two_hits)
        two.damage(one_hits)
        if one.is_destroyed() or two.is_destroyed():
            return one, two

# outputs percentage of attacker (first army) wins
SIMS = 1000
def sim(attacker, defender):
    attacker = Army(attacker)
    defender = Army(defender)

    attacker_survivors = []

    for i in range(SIMS):
        attacker_result, _ = simulate(attacker, defender, roll_dice=True)
        attacker_survivors.append(len(attacker_result.forces))

    attacker_wins = sum(min(n, 1) for n in attacker_survivors)/SIMS
    casualties = len(attacker.forces) - sum(attacker_survivors)/SIMS

    return attacker_wins, round(casualties, 2)

def calculate_corvette_equivalent(defence:Army|CombatantStats) -> int:
    corvettes = Army()
    defence = Army(defence)
    
    while True:
        corvettes.forces.append(StandardCombatants.Corvette)
        result = simulate(defence, corvettes, roll_dice=False)
        if not result[1].is_destroyed():
            return corvettes.forces.__len__() - 1

class Dice:
    d12 = 0
    d10 = 1
    d8 = 2
    d6 = 3
    d4 = 4

class StandardCombatants:
    Corvette = CombatantStats("Corvette", Dice.d12, 1, 1, 2, 0.5) # Front
    Destroyer = CombatantStats("Destroyer", Dice.d12, 3, 2, 4, 1) # Front
    Frigate = CombatantStats("Frigate", Dice.d8, 3, 1, 4, 1) # Back
    Cruiser = CombatantStats("Cruiser", Dice.d10, 7, 5, 8, 2) # Front
    BattleCruiser = CombatantStats("BattleCruiser", Dice.d6, 6, 2, 8, 2) # Back
    Battleship = CombatantStats("Battleship", Dice.d8, 9, 9, 12, 3) # Front
    Titan = CombatantStats("Titan", Dice.d4, 7, 3, 12, 3) # Back
class DefenceStation:
    LevelOne = CombatantStats("Defence Station Tier 1", Dice.d12, 2, 2, 1, 1)
    LevelTwo = CombatantStats("Defence Station Tier 2", Dice.d12, 4, 4, 3, 2)
    LevelThree = CombatantStats("Defence Station Tier 3", Dice.d10, 6, 6, 6, 3)
    LevelFour = CombatantStats("Defence Station Tier 4", Dice.d8, 9, 9, 10, 4)
    LevelFive = CombatantStats("Defence Station Tier 5", Dice.d6, 13, 13, 15, 5)
    LevelSix = CombatantStats("Defence Station Tier 6", Dice.d6, 16, 16, 21, 6)
    LevelSeven = CombatantStats("Defence Station Tier 7", Dice.d4, 20, 20, 28, 7)

class UpgradedCombatants:
    Destroyer = StandardCombatants.Destroyer.modified_copy(1,1)
    Frigate = StandardCombatants.Frigate.modified_copy(1,1)
    Cruiser = StandardCombatants.Cruiser.modified_copy(1,1)
    BattleCruiser = StandardCombatants.BattleCruiser.modified_copy(1,1)

print(sim(Army(UpgradedCombatants.Cruiser* 3, UpgradedCombatants.Frigate * 2), Army(UpgradedCombatants.Cruiser *3, UpgradedCombatants.BattleCruiser)))

print(sim(Army(UpgradedCombatants.Destroyer* 2), Army(UpgradedCombatants.Cruiser)))

print(sim(Army(UpgradedCombatants.Destroyer*2, UpgradedCombatants.Cruiser, StandardCombatants.Titan), Army(UpgradedCombatants.Cruiser * 2, StandardCombatants.Titan)))