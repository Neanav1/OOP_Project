import random


class Character:
    def __init__(self, hp, action_points=1, dice_to_roll=2):
        self._hp = hp
        self._shield = 0
        self._action_points = action_points
        self._dice_to_roll = dice_to_roll
        self._rolls = []
        self._available_actions = {
            "Basic_Strike": BasicStrike("Basic Strike"),
            "Shield": Shield("Shield"),
            "End_turn": EndTurn("End Turn")
        }
        self._equipment = []
    
    def equipt(self,item):
        self._equipment.append(item)

    def unequipt(self,item):
        self._equipment.remove(item)


    def roll_dices(self, number=1):
        """Rolls a number of dice and stores the results."""
        if number > self._dice_to_roll:
            number = self._dice_to_roll

        for i in range(number):
            self._rolls.append(random.randint(1, 6))

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
        self._hp -= number

        if self._hp < 0:
            self._hp = 0

    def reduce_action_points(self, number=1):
        self._action_points -= number

        if self._action_points < 0:
            self._action_points = 0

    def add_action_points(self, number=1):
        self._action_points += number

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

    def greet(self):
        print("------------------------------------------")
        print(f"HP: {self._hp}")
        print(f"Shield: {self._shield}")
        print(f"Action points: {self._action_points}")
        print(f"Dice left to roll: {self._dice_to_roll}")
        print(f"Rolled dice: {self._rolls}")
        print("------------------------------------------")


class Knight(Character):
    def __init__(self, hp, action_points=1, dice_to_roll=2):
        super().__init__(hp, action_points, dice_to_roll)

class Item:
    
    def __init__(self,name,requirement):
        self.name = name
        self.requirement = requirement
        self.action_name = ""
        self.action = None

    def get_action(self):
        return self.action_name , self.action

class BasicSword(Item):

    def __init__(self, name, requirement):
        super().__init__(name, requirement)

   
    

class Action:
    def __init__(self, name):
        self.name = name

    def action(self, dice):
        return 0, "None"


class BasicStrike(Action):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dice):
        return dice, "Enemy"


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