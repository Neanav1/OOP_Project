import random

class Character(object):
    def __init__(self,hp,action = 1,n_dice = 2):
        self._hp = hp
        self._shield = 0
        self._action = action
        self._n_dice = n_dice
        self._rolls = []
        self._actions = {"End_turn": EndTurn("End Turn")}
        self._action_avalable = {"Basic_Strike" : BasicStrike("basic strike"),
                                 "Shield":Shield("Shield"),
                                 "End_turn": EndTurn("End Turn")}

    #rolls number of dices
    def roll_dices(self,number =1):
        """rolls number of dices"""
        for i in range(self._n_dice-number):
            self._rolls.append(random.randint(1,6))
        self._n_dice-=self._n_dice_to_use

    #uses dice out of available list of dices
    def use_dices(self,index):
        """uses dice out of available list of dices"""
        pass

    #add more dices
    def add_n_dice(self,number):
        """add more dices"""
        self._n_dice+=number

    def get_n_dice(self):
        """returns number of dices avalable"""
        return self._n_dice

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

    def add_action(self,action):
        """adds an action to list of actions which player can use"""
        if action in self._action_avalable:
            self._action.append()

    def get_rolls(self):
        """return rolls"""
        return self._rolls
    
    def get_n_dices_avalable(self):
        """returns number of avalable dices to roll"""
        return self._n_dice
    
    def get_avalable_actions(self):
        """returns avalable actions"""
        return self._action_avalable
    
    def add_avalable_actions(self,name,action):
        """Adds an action to dictionary of avalable actions"""
        self._action_avalable[name] = action

    def get_shield(self):
        """returns shield value"""
        return self._shield
    
    def add_shield(self,number):
        """Adds shield"""
        self._shield += number

class Knight(Character):

    def __init__(self, hp, n_dice_to_use=1, action=1, n_dice=2):
        super().__init__(hp, n_dice_to_use, action, n_dice)

class Actions(object):

    def __init__(self,name):
        self.name = name 

    def action():
        return None    

class BasicStrike(Actions):
    def __init__(self, name):
        super().__init__(name)

    def action(self,dice):
        return 1*dice

class Shield(Actions):
    def __init__(self, name):
        super().__init__(name)

    def action(self,dice):
        return 1*dice

class EndTurn(Actions):

    def __init__(self, name):
        super().__init__(name)

    def endTurn(self):
        return -1
