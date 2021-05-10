import team_name.player


def evaluate(my_tokens,opponent_tokens):
    
    utility = 0
    if len(opponent_tokens) == 0:
        utility = 100
        return utility
    if len(my_tokens) == 0:
        return utility

    my_tokens_s = []
    my_tokens_p = []
    my_tokens_r = []
    opponent_tokens_s = []
    opponent_tokens_p = []
    opponent_tokens_r = []

    for my_token in my_tokens:
        if my_token['type'] == 's':
            my_tokens_s.append(my_token)
        if my_token['type'] == 'r':
            my_tokens_r.append(my_token)
        if my_token['type'] == 'p':
            my_tokens_p.append(my_token)
    for opponent_token in opponent_tokens:
        if opponent_token['type'] == 's':
            opponent_tokens_s.append(opponent_token)
        if opponent_token['type'] == 'r':
            opponent_tokens_r.append(opponent_token)
        if opponent_token['type'] == 'p':
            opponent_tokens_p.append(opponent_token)

    if len(my_tokens_s) != 0 and len(opponent_tokens_p) != 0:
        utility += 20
        distance_list = Player.find_all_distance(my_tokens_s,opponent_tokens_p)
        utility -= min(distance_list)
    if len(my_tokens_p) != 0 and len(opponent_tokens_r) != 0:
        utility += 20
        distance_list = Player.find_all_distance(my_tokens_p,opponent_tokens_r)
        utility -= min(distance_list)
    if len(my_tokens_r) != 0 and len(opponent_tokens_s) != 0:
        utility += 20
        distance_list = Player.find_all_distance(my_tokens_r,opponent_tokens_s)
        utility -= min(distance_list)
    
    return utility