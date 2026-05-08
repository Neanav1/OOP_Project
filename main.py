from character import Character, Knight, BasicSword, BasicShield
from enemy_ai import enemy_turn
import random

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
        value , target = actions[action_id].action(player.get_rolls()[dice_ID-1])
        if target == "End":
            break
        if target == "Enemy":
            if enemy.get_shield() >= value:
                enemy.add_shield(-value)
            else:
                remaining_damage = enemy.get_shield() - value
                enemy.hp_change(-remaining_damage)
                player.add_action_points(-1)
                player.use_dice(dice_ID-1)
        if target == "Self":
            player.add_shield(value)
            player.add_action_points(-1)    
            player.use_dice(dice_ID-1)

def random_enemy(enemyList,stage):
    enemyID = random.randint(0,len(enemyList)-1)
    enemy = enemyList[enemyID].changeAtributes(stage)
    return enemy

def options():
    print("\n")
    print("1.")

player = Knight(25)
enemy = Knight(25)
player.equipt(BasicSword("Sword",None))
enemy.equipt(BasicSword("Sword",None))
player.equipt(BasicShield("Shield",None))
enemy.equipt(BasicShield("Shield",None))
stage = -1

enemyList = [Knight(25)]

#run the game untill all of the enemies are dead or untill player is dead
while player.get_hp()>0:
    stage+=1
    while player.get_hp() > 0 and enemy.get_hp() > 0:
        player_turn(enemy, player)

        if enemy.get_hp() <= 0:
            break

        enemy_turn(enemy, player)

        if player.get_hp() <= 0:
            break

        player.add_action_points(1)
        player.add_dice_to_roll(1)

        enemy.add_action_points(1)
        enemy.add_dice_to_roll(1)

if player.get_hp()<= 0:
    print("You lost")
if enemy.get_hp()<=0:
    print("You win")
        