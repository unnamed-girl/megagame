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
    # def combat_ratio(self): # defunct smart targetting
    #     return (self.attack + self.bonus/2)/(self.max_hp-self._damage_taken)
    def roll_hits(self) -> int:
        hits = 0
        for _ in range(self.attack):
            if random.randint(1, self.dice_size) <= 1:
                hits += 1
        return hits
    def _average_hits(self) -> float:
        return self.attack / self.dice_size
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
        # else: # defunct smart targetting:
        #     damage_overflow = damage
        #     target_indices:list[int] = [i for i in range(len(self.forces))]
        #     target_indices.sort(key=lambda i: self.forces[i].combat_ratio(), reverse=False)
        #     to_remove = []
        #     for i in target_indices:
        #         target = self.forces[i]
        #         if target.max_hp - target._damage_taken <= damage_overflow:
        #             to_remove.append(i)
        #             damage_overflow -= (target.max_hp - target._damage_taken)
        #             target._damage_taken += (target.max_hp - target._damage_taken)
        #     if damage_overflow > 0:
        #         for i in target_indices:
        #             target = self.forces[i]
        #             if target.max_hp > target._damage_taken:
        #                 target._damage_taken += damage_overflow
        #                 break
        #     to_remove.sort()
        #     to_remove = [to_remove[i]-i for i in range(len(to_remove))]
            # for i in to_remove:
            #     self.forces.pop(i)
                    
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

def standard_corvette_defence(defence:Army|CombatantStats) -> int:
    corvettes = Army()
    if type(defence) is CombatantStats:
        defence = Army(defence)
    while True:
        corvettes.forces.append(StandardCombatants.Frigate)
        result = simulate(defence, corvettes, roll_dice=False)
        if result[0].is_destroyed():
            return corvettes.forces.__len__()

class StandardCombatants(_CombatantWrapper, Enum):
    Corvette = CombatantStats("Corvette", 1,0,1)
    Frigate = CombatantStats("Frigate", 1, 3, 1)
    Destroyer = CombatantStats("Destroyer", 3, 0, 2)
    Cruiser = CombatantStats("Cruiser", 3, 3, 3)
    Battleship = CombatantStats("Battleship", 4, 2, 7)
    Titan = CombatantStats("Titan", 6, 5, 4)
    Planet = CombatantStats("Planet", 1, 2, 5)

    StationOne = CombatantStats("Station 1", 1,1,2)
    StationTwo = CombatantStats("Station 2", 2,2,4)
    StationThree = CombatantStats("Station 3", 5,3,8)
    StationFour = CombatantStats("Station 4", 8,4,16)
    StationFive = CombatantStats("Station 5", 13,6,25)
class OurCombatants(_CombatantWrapper, Enum):
    Corvette = StandardCombatants.Corvette.modified_copy(2,1,1)
    Destroyer = StandardCombatants.Destroyer.modified_copy(1,1,0)
    Cruiser = StandardCombatants.Cruiser.modified_copy(0,1,1)
    Battleship = StandardCombatants.Battleship.modified_copy(0,2,2)
    Titan = StandardCombatants.Titan.modified_copy(1)
    
    LevelOneStation = StandardCombatants.StationOne.modified_copy()
    LevelTwoStation = StandardCombatants.StationTwo.modified_copy()   

alloy = Army(StandardCombatants.Frigate*2, StandardCombatants.Destroyer*3)

alloy_2 = Army(StandardCombatants.Frigate*3, StandardCombatants.Corvette*10)

unity = Army(StandardCombatants.Frigate, StandardCombatants.Cruiser, StandardCombatants.Corvette * 5)

green_research = Army(StandardCombatants.Destroyer*4)

planet_thirteen = Army(StandardCombatants.Titan, StandardCombatants.Destroyer * 2, StandardCombatants.Corvette * 2, StandardCombatants.Cruiser)
robot_planet = Army(StandardCombatants.Titan, StandardCombatants.Battleship*2, StandardCombatants.Cruiser*3, StandardCombatants.Destroyer*2, StandardCombatants.Frigate*2, StandardCombatants.Corvette)