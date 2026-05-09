from character import Character, Knight, BasicSword, BasicShield
from enemy_ai import enemy_turn
import random
from character import Dagger

def player_turn(enemy,player):
    player.greet()
    dices = int(input("How many dices would you like to use: "))
    while player.get_action_points() > 0:
        player.roll_dices(dices)
        print("--- Players Turn ---")
        player.greet()
        count = 0
        actions = {}
        for name,action in player.get_available_actions().items():
             count += 1
             actions[count] = action
             print(f"{count}: {name} ")
        action_id = int(input("Enter action which you want to use: "))
        dice_ID = int(input("Which dice do you want to use: "))
        if dice_ID - 1 < 0 or dice_ID - 1 >= len(player.get_rolls()):
            print("Invalid dice selection.")
            continue

        dice_value = player.get_rolls()[dice_ID-1]
        value, target = actions[action_id].action(dice_value)

        if target == "End":
            player.reduce_action_points(player.get_action_points())
            break

        if target == "Enemy":
            enemy.take_damage(value)

        elif target == "Self":
            player.add_shield(value)

        player.reduce_action_points(1)
        player.use_dice(dice_ID-1)

def random_enemy(enemyList,stage):
    enemyID = random.randint(0, len(enemyList)-1)
    enemy = enemyList[enemyID]
    enemyWeapon = random.choice([BasicSword("Sword", None), Dagger("Dagger", None)])
    enemy.equipt(enemyWeapon)
    enemy.changeAtributes(stage)
    return enemy

def options():
    print("\n")
    print("1.Fight")
    print("2. Shop")
    print("3. Inventory")
    print("4. Exit")

player = Knight(250)
player.equipt(BasicSword("Sword",None))
stage = -1

enemyList = [Knight(25,4)]

while player.get_hp()>0 or stage >= 8:
    
    options()
    option = int(input("Select an action: "))
    if option == 1:
        stage+=1
        enemy = random_enemy(enemyList,stage)
        while player.get_hp() > 0 and enemy.get_hp() > 0:
            player_turn(enemy, player)

            if enemy.get_hp() <= 0:
                break

            enemy_turn(enemy, player)

            if player.get_hp() <= 0:
                break

            player.add_action_points(1)
            player.add_dice_to_roll(1)

            enemy.add_action_points(1+(0.5*stage))
            enemy.add_dice_to_roll(1)

    if player.get_hp()<= 0:
        print("You lost")
        break
    if enemy.get_hp()<=0:
        print("You win")
    elif option == 2:
        print("shop")
    elif option == 3:
        print("Inventory")
    elif option == 4:
        break
    else:
        print("Incorrect input")