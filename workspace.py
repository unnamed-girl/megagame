from battle_sim import *

for ship_type in [StandardCombatants.Corvette, StandardCombatants.Frigate, StandardCombatants.Destroyer, StandardCombatants.Cruiser, StandardCombatants.BattleCruiser, StandardCombatants.Battleship, StandardCombatants.Titan]:
#for ship_type in [StandardCombatants.LevelOneStation, StandardCombatants.LevelTwoStation, StandardCombatants.LevelThreeStation, StandardCombatants.LevelFourStation, StandardCombatants.LevelFiveStation, StandardCombatants.LevelSixStation, StandardCombatants.LevelSevenStation]:
    ship_type = ship_type.modified_copy(1, 1)
    brick = Army(StandardCombatants.Frigate * 5)
    frigate_equivalent = calculate_corvette_equivalent(Army(brick, ship_type * 2))
    print("Brick " + ship_type.name, frigate_equivalent, round(frigate_equivalent/(ship_type.cost * 2 + 10),2))

upgraded_battleship = StandardCombatants.Battleship.modified_copy(1, 1)
upgraded_titan = StandardCombatants.Titan.modified_copy()

upgraded_frigate = StandardCombatants.Frigate.modified_copy(1,1)
upgraded_cruiser = StandardCombatants.Cruiser.modified_copy()

print(sim(Army(StandardCombatants.Frigate.modified_copy(0,1) * 3, StandardCombatants.Subspace*2), Army(StandardCombatants.Frigate * 2, DefenceStation.LevelTwo.modified_copy(3,3))))