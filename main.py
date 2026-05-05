from character import Character, Knight
from enemy_ai import enemy_turn
def player_turn(enemy,player):
    player.greet()
    while player.get_action_points() > 0:
        dices = int(input("How many dices would you like to use: "))
        player.roll_dices(dices)
        #loop for player action, ends when player has no more actions
        print(player.get_available_actions)
        
    

    



player = Knight(10)
enemy = Knight(10)

#this will do the ai_turns
enemy_turn(enemy,player)


while player.get_hp() > 0 or enemy.get_hp() >0  :
      player_turn(enemy,player)

        
        







