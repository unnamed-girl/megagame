from dataclasses import dataclass
import random
from enum import Enum
from copy import deepcopy

@dataclass
class CombatantStats:
    name:str
    attack:int
    bonus:int
    max_hp:int
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
    def modified_copy(self, extra_attack=0, extra_bonus=0, extra_hp=0) -> "CombatantStats":
        return CombatantStats(self.name, self.attack + extra_attack, self.bonus + extra_bonus, self.max_hp + extra_hp)
    def __hash__(self) -> int:
        return hash((self.name, self.attack, self.bonus, self.max_hp))
    def __str__(self) -> str:
        return self.name
    def __mul__(self, other):
        return [self]*other
    def __rmul__(self, other):
        return [self]*other
    
class _CombatantWrapper(CombatantStats):
    def __init__(self, wrapped:CombatantStats) -> None:
        self.__dict__ = wrapped.__dict__
        self.__class__ = wrapped.__class__


class Army:
    def __init__(self, *forces) -> None:
        self.forces:list[CombatantStats] = []
        for force in forces:
            if hasattr(force, "__iter__"):
                self.forces.extend(force)
            else:
                self.forces.append(force)
        self.forces = [ship.modified_copy() for ship in self.forces]
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
def simulate(one:Army, two:Army, roll_dice=True):
    one = deepcopy(one)
    two = deepcopy(two)
    if type(one) != Army:
        one = Army(one)
    if type(two) != Army:
        two = Army(two )
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
def sim(attacker:Army, defender:Army):
    attacker_wins = 0
    for i in range(SIMS):
        result = simulate(attacker, defender, roll_dice=True)
        if not result[0].is_destroyed():
            attacker_wins += 1
    return attacker_wins/SIMS
def sim_count(attacker:Army, defender:Army):
    attacker_survivors = 0
    defender_survivors = 0
    for i in range(SIMS):
        result = simulate(attacker, defender, roll_dice=True)
        attacker_survivors += result[0].forces.__len__()
        defender_survivors += result[1].forces.__len__()
    return attacker_survivors/SIMS, defender_survivors/SIMS

def standard_frigate_defence(defence:Army|CombatantStats) -> int:
    corvettes = Army()
    if type(defence) is CombatantStats:
        defence = Army(defence)
    while True:
        corvettes.forces.append(StandardCombatants.Frigate)
        result = simulate(defence, corvettes, roll_dice=False)
        if result[0].is_destroyed():
            return corvettes.forces.__len__()

class StandardCombatants(_CombatantWrapper, Enum):
    Frigate = CombatantStats("Frigate", 1, 0, 1) # Front
    Subspace = CombatantStats("Subspace", 2, 1, 1) # Back
    Destroyer = CombatantStats("Destroyer", 2, 0, 2) # Front
    Cruiser = CombatantStats("Cruiser", 5, 1, 3) # Front
    BattleCruiser = CombatantStats("BattleCruiser", 3, 3, 2) # Back
    Battleship = CombatantStats("Battleship", 6, 2, 5) # Front
    Titan = CombatantStats("Titan", 4, 4, 3) # Back

class OurCombatants(_CombatantWrapper, Enum):
    Frigate = StandardCombatants.Frigate.modified_copy(1,0,1)

planet_twenty_five = Army(StandardCombatants.Frigate, StandardCombatants.Destroyer, StandardCombatants.Subspace * 2)

planet_fourty_three = Army(StandardCombatants.Frigate * 6)

thirty_two = Army(StandardCombatants.Frigate, StandardCombatants.Battleship, StandardCombatants.BattleCruiser, StandardCombatants.Subspace)

fifty_five = Army( StandardCombatants.BattleCruiser, StandardCombatants.Destroyer,StandardCombatants.Frigate)
thirty_nine = Army(StandardCombatants.Cruiser*2, StandardCombatants.Destroyer, StandardCombatants.Subspace)

print(standard_frigate_defence(Army(StandardCombatants.Cruiser, StandardCombatants.Frigate)))

print(standard_frigate_defence(thirty_nine))

print(sim(Army(OurCombatants.Frigate*28), Army(StandardCombatants.Titan*4)))

your_army = Army(StandardCombatants.Frigate.modified_copy(2,1,1)*37)
their_army = Army(StandardCombatants.Frigate.modified_copy(2,1,1) * 25, CombatantStats("Station Two", 3, 0, 5), 3 * StandardCombatants.Subspace.modified_copy(2,0,0))
print(sim(your_army, their_army))

chris_cruiser = StandardCombatants.Cruiser.modified_copy(1,0,1)
print(simulate(Army(OurCombatants.Frigate*25), Army(chris_cruiser*3, OurCombatants.Frigate*2)))

