from copy import deepcopy
import random

def enemy_logic(enemy, player):
    current_state = {
        "enemyHP": enemy.get_hp(),
        "enemyShield": enemy.get_shield(),
        "enemyActionPoints": enemy.get_action_points(),
        "enemyDiceToRoll": enemy.get_dice_to_roll(),

        # IMPORTANT: use .copy() so simulate does not delete real dice
        "enemyRolls": enemy.get_rolls().copy(),

        "playerHP": player.get_hp(),
        "playerShield": player.get_shield(),
        "playerActionPoints": player.get_action_points(),
        "playerDiceToRoll": player.get_dice_to_roll(),

        # IMPORTANT: copy player rolls too
        "playerRolls": player.get_rolls().copy()
    }

    possible_actions = enemy.get_available_actions()

    best_score = float("-inf")
    best_action_name = None
    best_dice_index = None

    for action_name, action_object in possible_actions.items():

        if action_name == "End_turn":
            future_state = simulate(current_state, action_object, None)
            score = score_state(current_state, future_state)

            if score > best_score:
                best_score = score
                best_action_name = action_name
                best_dice_index = None

        else:
            for dice_index in range(len(current_state["enemyRolls"])):

                # IMPORTANT: use dice_index, not 0
                future_state = simulate(current_state, action_object, dice_index)

                score = score_state(current_state, future_state)

                if score > best_score:
                    best_score = score
                    best_action_name = action_name
                    best_dice_index = dice_index

    return best_action_name, best_dice_index


def simulate(current_state, action_object, dice_index):
    # IMPORTANT: deepcopy protects lists inside the dictionary
    future_state = deepcopy(current_state)

    if action_object.name == "End Turn":
        future_state["enemyActionPoints"] = 0
        future_state["enemyDiceToRoll"] += 1
        return future_state

    dice = future_state["enemyRolls"][dice_index]

    result, target = action_object.action(dice)

    if target == "Enemy":
        damage = result

        if future_state["playerShield"] >= damage:
            future_state["playerShield"] -= damage
        else:
            remaining_damage = damage - future_state["playerShield"]
            future_state["playerShield"] = 0
            future_state["playerHP"] -= remaining_damage

            if future_state["playerHP"] < 0:
                future_state["playerHP"] = 0

    elif target == "Self":
        future_state["enemyShield"] += result

    future_state["enemyRolls"].pop(dice_index)
    future_state["enemyActionPoints"] -= 1

    return future_state


def score_state(current_state, future_state):
    characters = ["defensive","agressive"]
    char = random.randint(0,len(characters)-1)
    current_char = characters[char]
    if current_char == "defensive":
        values = [0.8,1,2]
    elif current_char == "agressive":
        values = [1.2,0.8]

    score = 0

    if future_state["playerHP"] <= 0:
        score += 1000

    damage_done = current_state["playerHP"] - future_state["playerHP"]
    score += damage_done * 20 * values[0]

    shield_damage = current_state["playerShield"] - future_state["playerShield"]
    score += shield_damage * 5 * values[0]

    shield_gained = future_state["enemyShield"] - current_state["enemyShield"]
    score += shield_gained * 10 * values[1]

    score += future_state["enemyShield"] * 2 * values[0]

    return score


def perform_enemy_action(enemy, player, action_name, dice_index):
    actions = enemy.get_available_actions()
    action_object = actions[action_name]

    if action_name == "End_turn":
        print("Enemy ends the turn.")
        enemy.reduce_action_points(enemy.get_action_points())
        enemy.add_action_points(1)
        enemy.add_dice_to_roll(1)
        return

    if dice_index is None:
        print("Enemy tried to use an action without a dice.")
        return

    dice = enemy.use_dice(dice_index)

    if dice is None:
        print("Enemy tried to use an invalid dice.")
        return

    result, target = action_object.action(dice)

    if target == "Enemy":
        print(f"Enemy uses {action_name} with dice {dice}. It deals {result} damage.")
        player.take_damage(result)

    elif target == "Self":
        print(f"Enemy uses {action_name} with dice {dice}. It gains {result} shield.")
        enemy.add_shield(result)

    enemy.reduce_action_points(1)


def enemy_turn(enemy, player):
    print("\n--- Enemy Turn ---")

    if len(enemy.get_rolls()) == 0 and enemy.get_dice_to_roll() > 0:
        enemy.roll_dices(enemy.get_dice_to_roll())

    print("Enemy rolls before choosing:", enemy.get_rolls())

    if len(enemy.get_rolls()) == 0:
        print("Enemy has no dice, ending turn.")
        enemy.reduce_action_points(enemy.get_action_points())
        return

    while enemy.get_action_points() > 0 and len(enemy.get_rolls()) > 0:
        action_name, dice_index = enemy_logic(enemy, player)
        perform_enemy_action(enemy, player, action_name, dice_index)

        if action_name == "End_turn":
            break
    
    enemy.greet()
    print("\n")