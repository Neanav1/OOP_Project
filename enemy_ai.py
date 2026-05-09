from copy import deepcopy
import random

def enemy_logic(enemy, player):
    current_state = {
        "enemyHP": enemy.get_hp(),
        "enemyShield": enemy.get_shield(),
        "enemyActionPoints": enemy.get_action_points(),
        "enemyDiceToRoll": enemy.get_dice_to_roll(),

        "enemyRolls": enemy.get_rolls().copy(),

        "playerHP": player.get_hp(),
        "playerShield": player.get_shield(),
        "playerActionPoints": player.get_action_points(),
        "playerDiceToRoll": player.get_dice_to_roll(),

        "playerRolls": player.get_rolls().copy()
    }

    possible_actions = enemy.get_available_actions()
    original_state = deepcopy(current_state)

    def evaluate(state):
        """Return (best_score, best_action_name, best_dice_index) from this state"""
        best_score = float("-inf")
        best_choice = (None, None)

        actions = enemy.get_available_actions()

        for action_name, action_object in actions.items():
            if action_name == "End_turn":
                fut = simulate(state, action_object, None)
                score = score_state(original_state, fut)
                if score > best_score:
                    best_score = score
                    best_choice = (action_name, None)
                continue

            for dice_index in range(len(state["enemyRolls"])):
                fut = simulate(state, action_object, dice_index)

                if fut["enemyActionPoints"] > 0 and len(fut["enemyRolls"]) > 0:
                    sub_score, _, _ = evaluate(fut)
                    score = sub_score
                else:
                    score = score_state(original_state, fut)

                if score > best_score:
                    best_score = score
                    best_choice = (action_name, dice_index)

        return best_score, best_choice[0], best_choice[1]

    _, action_name, dice_index = evaluate(current_state)
    return action_name, dice_index


def simulate(current_state, action_object, dice_index):
    future_state = deepcopy(current_state)

    if action_object.name == "End Turn":
        future_state["enemyActionPoints"] = 0
        return future_state

    dice = future_state["enemyRolls"][dice_index]

    result, target = action_object.expected(dice)

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
    if future_state["playerHP"] <= 0:
        return 10000

    score = 0.0

    damage_done = current_state["playerHP"] - future_state["playerHP"]
    score += damage_done * 50.0

    shield_damage = current_state["playerShield"] - future_state["playerShield"]
    score += shield_damage * 12.0

    shield_gained = future_state["enemyShield"] - current_state["enemyShield"]
    enemy_hp = current_state.get("enemyHP", 0)
    player_hp = current_state.get("playerHP", 0)

    if enemy_hp <= max(1, player_hp * 0.5):
        score += shield_gained * 25.0
    else:
        score += shield_gained * 10.0

    score += future_state.get("enemyShield", 0) * 2.0

    score += random.uniform(-2.0, 2.0)

    return score


def perform_enemy_action(enemy, player, action_name, dice_index):
    actions = enemy.get_available_actions()
    action_object = actions[action_name]

    if action_name == "End_turn":
        print("Enemy ends the turn.")
        enemy.reduce_action_points(enemy.get_action_points())
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