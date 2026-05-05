
def enemy_logic(enemy, player):
    current_state = {
        "enemyHP": enemy.get_hp(),
        "enemyShield": enemy.get_shield(),
        "enemyActionPoints": enemy.get_action_points(),
        "enemyDiceToRoll": enemy.get_dice_to_roll(),
        "enemyRolls": enemy.get_rolls(),

        "playerHP": player.get_hp(),
        "playerShield": player.get_shield(),
        "playerActionPoints": player.get_action_points(),
        "playerDiceToRoll": player.get_dice_to_roll(),
        "playerRolls": player.get_rolls()
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
                future_state = simulate(current_state, action_object, 0)
                score = score_state(current_state, future_state)

                if score > best_score:
                    best_score = score
                    best_action_name = action_name
                    best_dice_index = dice_index

    return best_action_name, best_dice_index


def simulate(current_state, action_object, dice_index):
    future_state = current_state.copy()

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
    score = 0

    if future_state["playerHP"] <= 0:
        score += 1000

    damage_done = current_state["playerHP"] - future_state["playerHP"]
    score += damage_done * 20

    shield_damage = current_state["playerShield"] - future_state["playerShield"]
    score += shield_damage * 5

    shield_gained = future_state["enemyShield"] - current_state["enemyShield"]
    score += shield_gained * 10

    score += future_state["enemyShield"] * 2

    if len(current_state["enemyRolls"]) == 0:
        score += 20

    return score


def perform_enemy_action(enemy, player, action_name, dice_index):
    actions = enemy.get_available_actions()
    action_object = actions[action_name]

    if action_name == "End_turn":
        print("Enemy ends the turn.")
        enemy.reduce_action_points(enemy.get_action_points())
        enemy.add_dice_to_roll(1)
        return

    dice = enemy.use_dice(dice_index)

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

    print("Enemy state before move:")
    enemy.greet()

    while enemy.get_action_points() > 0:
        if len(enemy.get_rolls()) == 0:
            break

        action_name, dice_index = enemy_logic(enemy, player)
        perform_enemy_action(enemy, player, action_name, dice_index)

        if action_name == "End_turn":
            break