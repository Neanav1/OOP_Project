import random


class Character:
    def __init__(self, hp, action_points=1, dice_to_roll=2, d =6 ):
        self._hp = hp
        self._d = d
        self._shield = 0
        self._action_points = action_points
        self._dice_to_roll = dice_to_roll 
        self._rolls = []
        self._available_actions = {
            "Shield": Shield("Shield"),
            "End_turn": EndTurn("End Turn")
        }
        self._equipment = []
        self.inventory = []
        self._level = 1
        self._rolls_per_turn = 1
        self._buffs = []
        self._debuffs = []
        self._stun_turns = 0
    
    def levelUp(self,system):
        self._level +=1
        self._hp += round(self._hp*self._level*system[0]) - self._hp
        self._rolls_per_turn += round(self._level*system[1])

    def changeAtributes(self,stage):
        self._hp += round(self._hp*self._level*1.3) - self._hp
        self.add_dice_to_roll(1*stage)
        self._rolls_per_turn = 1*stage

    def get_rolls_per_turn(self):
        return self._rolls_per_turn

    def equipt(self,item):
        self._equipment.append(item)
        name , action = item.get_action()
        self.add_avalable_action(name,action)

    def unequipt(self,item):
        self._equipment.remove(item)

    def roll_dices(self, number=1):
        """Rolls a number of dice and stores the results."""
        if number > self._dice_to_roll:
            number = self._dice_to_roll

        for i in range(number):
            self._rolls.append(random.randint(1, self._d))

        self._dice_to_roll -= number

    def use_dice(self, index):
        """Removes and returns a dice from the rolled dice list."""
        if 0 <= index < len(self._rolls):
            return self._rolls.pop(index)

        return None

    def take_damage(self, damage):
        """Damage shield first, then HP."""
        if int(self._shield) >= int(damage):
            self._shield -= damage
        else:
            remaining_damage = damage - self._shield
            self._shield = 0
            self._hp -= remaining_damage

            if self._hp < 0:
                self._hp = 0

    def add_shield(self, number):
        self._shield += number

    def hp_change(self, number):
        """Positive number damages, negative number heals."""
        self._hp -= round(number)

        if self._hp < 0:
            self._hp = 0

    def reduce_action_points(self, number=1):
        self._action_points -= number

        if self._action_points < 0:
            self._action_points = 0

    def add_action_points(self, number=1):
        self._action_points += number

    
    def get_equipment(self):
        return self._equipment


    def add_dice_to_roll(self, number=1):
        self._dice_to_roll += number

    def get_hp(self):
        return self._hp

    def get_shield(self):
        return self._shield

    def get_action_points(self):
        return self._action_points

    def get_dice_to_roll(self):
        return self._dice_to_roll

    def get_rolls(self):
        return self._rolls

    def get_available_actions(self):
        return self._available_actions

    def add_avalable_action(self,name,action):
        self._available_actions[name] = action

    def greet(self):
        print("------------------------------------------")
        print(f"HP: {self._hp}")
        print(f"Shield: {self._shield}")
        print(f"Action points: {self._action_points}")
        print(f"Dice left to roll: {self._dice_to_roll}")
        print(f"Rolled dice: {self._rolls}")
        print("------------------------------------------")

    def process_debuffs(self):
        """Apply active debuffs at the start of a turn. Returns True if stunned."""
        stunned = False

        remaining = []
        for d in self._debuffs:
            name = d.get("name")
            value = d.get("value", 0)
            turns = d.get("turns", 0)

            if name == "Burn":
                self.hp_change(value)

            if turns - 1 > 0:
                d["turns"] = turns - 1
                remaining.append(d)

        self._debuffs = remaining

        if getattr(self, "_stun_turns", 0) > 0:
            stunned = True
            self._stun_turns -= 1

        return stunned

    def add_debuff(self, name, value=0, turns=1):
        """Add a debuff to this character. Stun is tracked as turns on the character."""
        if name == "Stun":
            self._stun_turns = getattr(self, "_stun_turns", 0) + turns
            return
        self._debuffs.append({"name": name, "value": value, "turns": turns})

    def is_stunned(self):
        return getattr(self, "_stun_turns", 0) > 0


class Knight(Character):
    def __init__(self, hp, action_points=1, dice_to_roll=2):
        super().__init__(hp, action_points, dice_to_roll)
        self.system = [1.3,1.5]
class Tank(Character):
    def __init__(self, hp, action_points=1, dice_to_roll=2):
        super().__init__(hp, action_points, dice_to_roll)
        self.system = [1.5,1.5]
    
    def changeAtributes(self, stage):
        self._hp += round(self._hp*self._level*1.5) - self._hp
        self.add_dice_to_roll(1*stage)
        self._rolls_per_turn = 1*stage

class Witch(Character):
    def __init__(self, hp, action_points=1, dice_to_roll=3, d=4):
        super().__init__(hp, action_points, dice_to_roll, d)
        self._rolls_per_turn = 2

    def changeAtributes(self, stage):
        self._hp += round(self._hp*self._level*1.15) - self._hp
        self.add_dice_to_roll(1*stage)
        self._rolls_per_turn = 1*stage
    
    
#Items
class Item:
    
    def __init__(self,name,requirement = None ):
        self.name = name
        self.requirement = requirement
        self.action_name = ""
        self.action = None
        self.rarity = "" 

    def get_action(self):
        return self.action_name , self.action

class BasicSword(Item):

    def __init__(self, name, requirement):
        super().__init__(name, requirement)
        self.action_name = "Basic_Strike"
        self.action = BasicStrike("Basic Strike")
        self.rarity = "Common"

class HolySword(Item):
    def __init__(self, name, requirement):
        super().__init__(name, requirement)
        self.action_name = "Holy_Strike"
        self.action = Holy_Strike("Holy Strike") 
        self.rarity = "Rare"
class Dagger(Item):
    def __init__(self, name, requirement):
        super().__init__(name, requirement)
        self.action_name = "QuickStab"
        self.action = QuickStab("Quick Stab")
        self.rarity = "Common"

class Icestaff(Item):
    def __init__(self, name, requirement=None):
        super().__init__(name, requirement)
        self.action_name = "Iceslash"
        self.action = Iceslash("Iceslash")
        self.rarity = "Common"

class Firestaff(Item):
    def __init__(self, name, requirement):
        super().__init__(name, requirement)
        self.action_name = "Fireball"
        self.action = Fireball("Fireball")
        self.rarity = "Common"

class Knuckle_Dusters(Item):
    def __init__(self, name, requirement):
        super().__init__(name, requirement)
        self.action_name = "Metal fist"
        self.action = Metal_fist("Metal Fist")
        self.rarity = "Common"
class BasicShield(Item):
    def __init__(self, name, requirement, ):
        super().__init__(name, requirement)
        self.action_name = "Shield"
        self.action = Shield("Shield")
        self.rarity = "Common"

#Actions
class Action:
    def __init__(self, name, damagetype = "None"):
        self.name = name
        self.damagetype = damagetype

    def action(self, dice):
        return dice, self.damagetype
    
    def expected(self, dice):
        return self.action(dice)
    



class Holy_Strike(Action):
      def __init__(self, name):
          super().__init__(name, damagetype= "Physical")

      def action(self, dice):
          return dice, "Enemy+Self"
         
class Metal_fist(Action):
     def __init__(self, name):
        super().__init__(name, damagetype= "Physical")

     def action(self, dice):
        return dice, "Enemy"
class Fireball(Action):
    def __init__(self, name):
        super().__init__(name, damagetype= "Fire")

    def action(self, dice):
        return round(dice * 1.5), "Enemy+Burn"
class BasicStrike(Action):
    def __init__(self, name):
        super().__init__(name, damagetype= "Physical")

    def action(self, dice):
        return dice, "Enemy"


class Fireslash(Action):
    def __init__(self, name):
        super().__init__(name, damagetype=  "Fire")

    def action(self, dice):
        return dice , "Enemy"

class Iceslash(Action):
    def __init__(self, name):
        super().__init__(name, damagetype="ice")

    def action(self, dice):
       
        if random.random() < 0.25:
            return 1, "Stun"
        return round(dice*0.75), "Enemy"

    
class QuickStab(Action): #(50% chance to do 2x damage)
    def __init__(self, name):
        super().__init__(name, damagetype = "Physical")

    def action(self, dice):
        if random.random() < 0.5:
            return dice * 2, "Enemy"
        return dice, "Enemy"

    def expected(self, dice):
        return dice * 1.5, "Enemy"

class Stun(Action):
    def __init__(self, name, damagetype="None"):
        super().__init__(name, damagetype)
    def action(self, dice=None):
        return 1, "Stun"
            

class Shield(Action):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dice):
        return dice, "Self"


class EndTurn(Action):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dice=None):
        return 0, "End"
    
class Rock(Action):
    def __init__(self, name, damagetype="None"):
        super().__init__(name, damagetype)
    
    def action(self, dice=None):
        # very small damage rock
        return 1, "Enemy"