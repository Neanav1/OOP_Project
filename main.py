from character import Character, Knight

player = Knight(10)
enemy = Knight(10)

while player.get_hp() > 0 or enemy.get_hp() >0  :
    
    player.greet()
    player.get_hp()
    player.get_actions()
    while player.get_actions() > 0:
        #loop for player action, ends when player has no more actions
        command_player = input("What would you like to do? ('1' for attack, '2' for heal, '3' for turn) ")
        
        







