from dataclasses import dataclass
import random

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

def standard_frigate_defence(defence:Army|CombatantStats) -> int:
    corvettes = Army()
    defence = Army(defence)
    
    while True:
        corvettes.forces.append(StandardCombatants.Frigate)
        result = simulate(defence, corvettes, roll_dice=False)
        if result[0].is_destroyed():
            return corvettes.forces.__len__()

class StandardCombatants:
    Frigate = CombatantStats("Frigate", 1, 0, 1) # Front
    Subspace = CombatantStats("Subspace", 2, 1, 1) # Back
    Destroyer = CombatantStats("Destroyer", 2, 0, 2) # Front
    Cruiser = CombatantStats("Cruiser", 5, 1, 3) # Front
    BattleCruiser = CombatantStats("BattleCruiser", 3, 3, 2) # Back
    Battleship = CombatantStats("Battleship", 6, 2, 5) # Front
    Titan = CombatantStats("Titan", 4, 4, 3) # Back

print(sim(StandardCombatants.Frigate*200, StandardCombatants.Titan*25))