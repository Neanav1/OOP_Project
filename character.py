import random

class Character(object):
    def __init__(self,hp,action = 1,n_dice = 2):
        self._hp = hp
        self._action = action
        self._n_dice = n_dice
        self._rolls = []
        self._actions = {"End_turn": EndTurn("End Turn")}
        self._action_avalable = {"Basic_Strike" : BasicStrike("basic strike"),
                                 "End_turn": EndTurn("End Turn")}

    #rolls number of dices
    def roll_dices(self,number =1):
        """rolls number of dices"""
        for i in range(self._n_dice-number):
            self._rolls.append(random.randint(1,6))
        self._n_dice-=self._n_dice_to_use

    #uses dice out of available list of dices
    def use_dices(self):
        """uses dice out of available list of dices"""
        pass

    #geting more dices
    def get_n_dice(self,number):
        """geting more dices"""
        self._n_dice+=number

    #change health positive int is damaging and negative int is healing
    def hp_change(self,number):
        """change health positive int is damaging and negative int is healing"""
        if self._hp - number >0:
            self._hp -= number
        else:
            self._hp  = 0
    
    def greet(self):
        print(f"HP: {self._hp} Dices available: {self._n_dice} Actions available: {self._actions}")

    #returns hp
    def get_hp(self):
        """returns hp"""
        return self._hp

    #returns number of actions
    def get_actions(self):
        """returns number of actions"""
        return self._action
    
    #recuces number of actions available
    def reduce_actions(self,number = 1):
        """recuces number of actions available"""
        if self._action - number >= 0:
            self._action -= number

    def get_action(self,action):
        if action in self._action_avalable:
            self._action.append()

class Knight(Character):

    def __init__(self, hp, n_dice_to_use=1, action=1, n_dice=2):
        super().__init__(hp, n_dice_to_use, action, n_dice)


class Actions(object):

    def __init__(self,name):
        self.name = name

class BasicStrike(Actions):
    def __init__(self, name):
        super().__init__(name)

    def damage(self,dice):
        return 1*dice

class EndTurn(Actions):

    def __init__(self, name):
        super().__init__(name)

    def endTurn(self):
        return -1

    