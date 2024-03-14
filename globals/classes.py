## CLASSES
# cell, HQ and terrain classes
class Cell:
    def __init__(self, resources, HP, damage, comms, naval, spec_ops, air_attack, air_defense, controlled_by):
        self.resources = resources
        self.HP = HP
        self.damage = damage
        self.comms = comms
        self.naval = naval
        self.spec_ops = spec_ops
        self.air_attack = air_attack
        self.air_defense = air_defense
        self.controlled_by = controlled_by

    def __str__(self):
        return f'Cell: R: {self.resources}, HP: {self.HP}, damage: {self.damage}, comms: {self.comms}, naval: {self.naval}, spec_ops: {self.spec_ops}, air_attack: {self.air_attack}, air_defense = {self.air_defense}, controlled by: {self.controlled_by}'
    
    
class HQ (Cell):
    def __init__(self, resources, controlled_by, captured=False):
        super().__init__(resources, HP=3, damage=3, comms=0, naval=0, spec_ops=0, air_attack=0, air_defense=3, controlled_by=controlled_by) 
        self.captured = captured

    def __str__(self):
        return f'HQ: captured: {self.captured} R: {self.resources}, HP: {self.HP}, damage: {self.damage}, comms: {self.comms}, naval: {self.naval}, spec_ops: {self.spec_ops}, air_attack: {self.air_attack}, air_defense = {self.air_defense}, controlled by: {self.controlled_by}'
    

class Terrain (Cell):
    def __init__(self, resources, controlled_by, type, color, advantage):
        super().__init__(resources, HP=1, damage=1, comms=0, naval=1, spec_ops=1, air_attack=1, air_defense=1, controlled_by=controlled_by)
        self.type = type
        self.color = color
        self.advantage = advantage
    
    def __str__(self):
        return f'Terrain: type: {self.type} advantage: {self.advantage} R: {self.resources}, HP: {self.HP}, damage: {self.damage}, comms: {self.comms}, naval: {self.naval}, spec_ops: {self.spec_ops}, air_attack: {self.air_attack}, air_defense = {self.air_defense}, controlled by: {self.controlled_by}'
    

# player classes
class Player:
    def __init__(self, name, color, wins, score=500, turns=3):
        self.name = name
        self.wins = wins
        self.color = color
        self.score = score
        self.turns = turns
        self.defeated = False
    
    def turn(self):
        if self.turns == 0:
            pass
        else:
            self.turns -= 1
