from character import *
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
            #player.reduce_action_points(player.get_action_points())
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
    if isinstance(enemy,Knight):
        enemyWeapon = random.choice([BasicSword("Sword", None), Dagger("Dagger", None)])
    if isinstance(enemy,Witch):
        enemyWeapon = random.choice([Firestaff("FireStaff", None),Icestaff("Icestaff", None)])
    enemy.equipt(enemyWeapon)
    enemy.changeAtributes(stage)
    return enemy

def options():
    print("\n")
    print("1. Fight")
    print("2. Shop")
    print("3. Inventory")
    print("4. Exit")

def random_award():
    rewards = [Dagger("Dagger", None),BasicSword("Sword", None),Holy_Strike("HolyStrike",None),Rock("Rock",None)]
    rewardID = random.randint(0, len(rewards)-1)
    return rewards[rewardID]

player = Knight(25)
player.equipt(BasicSword("Sword",None))
stage = 4

enemyList = [Knight(25),Witch(15)]

while player.get_hp()>0 or stage >= 8:
    
    options()
    option = int(input("Select an action: "))
    if option == 1:
        stage+=1
        enemy = random_enemy(enemyList,stage)
        if stage>=1:
            player.levelUp(player.system)
        while player.get_hp() > 0 and enemy.get_hp() > 0:
            player_turn(enemy, player)

            if enemy.get_hp() <= 0:
                break

            enemy_turn(enemy, player)

            if player.get_hp() <= 0:
                break

            player.add_action_points(1+(0.5*stage))
            player.add_dice_to_roll(player.get_rolls_per_turn())

            enemy.add_action_points(1+(0.5*stage))
            enemy.add_dice_to_roll(1)

        player.inventory.append(random_award())

        if player.get_hp()<= 0:
            print("You lost")
            break
        if enemy.get_hp()<=0:
            print("You win")
    elif option == 2:
        print("shop")
    elif option == 3:
        print("Inventory")
        print(f"Player's equipt item: {player.get_equipment()}")
        print(f"Player's inventory: {player.inventory}")
        option = int(input("Would you like to equipt or unequipt an item(0 equipt, 1 unequipt): "))
        if option == 1:
            player.inventory.append(player.get_equipment()[0])
            player.unequipt(player.get_equipment()[0])
        if option == 0:
            id = int(input("type an ID of an Item: "))
            player.equipt(player.inventory[id-1])
            player.inventory.remove(player.get_equipment()[0])
    elif option == 4:
        break
    else:
        print("Incorrect input")