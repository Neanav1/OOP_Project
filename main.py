from character import Character, Knight

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
        if command_player == '1':
            player.get_action("attack")
        elif command_player == '2':
            player.get_action("heal")
        elif command_player == '3':
            player.get_action("turn")
        else:
            print("invalid input, try again")
        
        







