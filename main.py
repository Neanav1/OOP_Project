from character import Character, Knight

def enemy_logic(enemy,player):
    """enemy logic with calculating good moves"""
    possibleActions = enemy.get_actions()

    bestAction = None
    bestScore = -9999

    currentState = {"enemyHP" : enemy.get_hp(),
                    "enemyShiled" : enemy.get_shield()
                    "enemyActions" : }

    for name , action in possibleActions:
        future = simulate(action)
        score = scoreState(future)

        if score > bestScore:
            bestScore = score
            bestAction = action

    return bestAction

def simulate():
    pass

def scoreState():
    pass

player = Knight(10)
enemy = Knight(10)

while player.get_hp() > 0 or enemy.get_hp() >0  :
    
    player.greet()
    while player.get_actions() > 0:
        print("you have 2 dices") #need function to show number of dices player got 
        dices = input(int("How many dices would you like to use: "))
        player.roll_dices(dices)
        #loop for player action, ends when player has no more actions
        command_player = input("What would you like to do? ('1' for attack, '2' for heal, '3' for turn) ")
        
        







