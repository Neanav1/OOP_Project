import random

class Character(object):
    def __init__(self,hp,n_dice_to_use=1,action = 1,n_dice = 2):
        self._hp = hp
        self._action = action
        self._n_dice = n_dice
        self._n_dice_to_use = n_dice_to_use
        self._rolls = []
        self._actions = {}
        self._action_avalable = {"Basic Strike" : Actions("basic strike")}

    def roll_dices(self):
        for i in range(self._n_dice-self._n_dice_to_use):
            self._rolls.append(random.randint(1,6))
        self._n_dice-=self._n_dice_to_use

    def use_dices(self):
        pass

    def get_n_dice(self,number):
        self._n_dice+=number

    def end_turn(self):
        return True
    
    def hp_change(self,number):
        if self._hp - number >0:
            self._hp -= number
        else:
            self._hp  = 0
    
    def greet(self):
        print(f"HP: {self._hp} Dices available: {self._n_dice} Actions available: {self._actions}")

    def get_hp(self):
        return self._hp

class Knight(Character):

    def __init__(self, hp, n_dice_to_use=1, action=1, n_dice=2):
        super().__init__(hp, n_dice_to_use, action, n_dice)


class Actions(object):

    def __init__(self,name):
        self.name = name

    