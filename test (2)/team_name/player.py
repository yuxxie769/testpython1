import random


class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        self.my_tokens = []
        self.opponent_tokens = []
        self.player = player
        self.allow_row = 1
        self.is9throwed = False

    
    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        if self.allow_row == 1:
            action = Player.random_throw(self)
        elif len(self.tokens) == 9 or self.is9throwed == True:
            action = Player.find_move(self)
            self.is9throwed = True
        else:
            action = Player.chose_action(self)

        if self.allow_row != 9:
                self.allow_row += 1
        
        return action
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        x,y,z = player_action
        if x ==  "THROW":
            newToken = {'index':len(self.my_tokens),'type':y,'position':z}
            self.my_tokens.append(newToken)
        else:
            for token in self.my_tokens:
                if token['position'] == y: token['position'] = z
        
        x,y,z = opponent_action
        if x ==  "THROW":
            newToken = {'index':len(self.opponent_tokens),'type':y,'position':z}
            self.opponent_tokens.append(newToken)
        else:
            for token in self.opponent_tokens:
                if token['position'] == y: token['position'] = z


    def random_throw(self):
        token_type = random.choice(['s','r','p'])
        if self.player == "upper":
            token_colPos = random.randint(-4,0)
            token_rowPos = 4
        if self.player == "lower":
            token_colPos = random.randint(0,4)
            token_rowPos = -4
        token = {'index':0,'type':token_type,'position':(token_rowPos,token_colPos)}
        action = ("THROW",token_type, (token_rowPos,token_colPos))
        return action

    def find_move(self):
        TempTokens = algorithm(self)
        return TempTokens
    
    def chose_action(self):
        TempTokens = self.my_tokens
        TempTokens = algorithm_with_throw(TempTokens)
        return TempTokens
    
    def minimax_decision(self):
        utilityList = []
        Temptokens_list = Player.find_new_movement_list(self.my_tokens)
        currMax = 0
        for Temptokens in Temptokens_list:
            deepth = 0
            utility = Player.min_value(Temptokens,self.opponent_tokens,deepth,currMax)
            utilityList.append(utility)
            if currMax < utility: currMax = utility
            
        dicided_tokens = Temptokens_list[utilityList.index(max(utilityList))]
        dicided_action_orgPos = list(set(self.my_tokens) - set(dicided_tokens))[0].get('positon')
        dicided_action_nowPos = list(set(dicided_tokens) - set(self.my_tokens))[0].get('positon')
        dicided_action = ("SLIDE",dicided_action_orgPos,dicided_action_nowPos)
        return dicided_action

    def min_value(my_tokens,opponent_tokens,deepth,currMax):
        deepth += 1
        if Player.isEnd(my_tokens,opponent_tokens,deepth):
            utility = Player.evaluate(my_tokens,opponent_tokens)
            return utility
        else:            
            utilityList = []
            Temptokens_list = Player.find_new_movement_list(opponent_tokens)
            currMin = 101
            for Temptokens in Temptokens_list:
                utility = Player.max_value(my_tokens,Temptokens,deepth,currMin)
                utilityList.append(utility)
                if currMin > utility: currMin = utility
                if currMax > utility: break
            utility = min(utilityList)
            return utility
    
    def max_value(my_tokens,opponent_tokens,deepth,currMin):
        deepth += 1
        if Player.isEnd(my_tokens,opponent_tokens,deepth):
            utility = Player.evaluate(my_tokens,opponent_tokens)
            return utility
        else:
            Temptokens_list = Player.find_new_movement_list(my_tokens)
            utilityList = []
            currMax = 0
            for Temptokens in Temptokens_list:
                utility = Player.min_value(Temptokens,opponent_tokens,deepth,currMax)
                utilityList.append(utility)
                if currMax < utility: currMax = utility
                if currMin < utility: break
            utility = max(utilityList)

            return utility
    def isEnd(my_tokens,opponent_tokens,deepth):
        if len(my_tokens) == 0 or len(opponent_tokens) == 0 or deepth == 4 or Player.isDraw(my_tokens,opponent_tokens):
            return True
        else: return False
    
    def isDraw(my_tokens,opponent_tokens):
        my_tokens_type = []
        opponent_tokens_type = []
        for my_token in my_tokens:
            my_tokens_type.append(my_token['type'])
        for opponent_token in opponent_tokens:
            opponent_tokens_type.append(opponent_token['type'])
        my_tokens_type = set(my_tokens_type)
        opponent_tokens_type = set(opponent_tokens_type)
        if len(my_tokens_type) == 1 and len(opponent_tokens_type) == 1 and len(my_tokens_type - opponent_tokens_type) == 0:
            return True
        if len(my_tokens_type) == 2 and len(opponent_tokens_type) == 2 and len(my_tokens_type - opponent_tokens_type) == 0:
            return True
        if (my_tokens_type == {'s','r'} and opponent_tokens_type == {'r'}) or (my_tokens_type == {'r'} and opponent_tokens_type == {'s','r'}):
            return True
        if (my_tokens_type == {'p','r'} and opponent_tokens_type == {'p'}) or (my_tokens_type == {'p'} and opponent_tokens_type == {'p','r'}):
            return True
        if (my_tokens_type == {'s','p'} and opponent_tokens_type == {'s'}) or (my_tokens_type == {'s'} and opponent_tokens_type == {'s','p'}):
            return True
        return False

    def evaluate(self, my_tokens,opponent_tokens):
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
    ##################################################################

    def juduge_releation(self, my_token, opponent_token):
        releation = -1
        if my_token['type'] == opponent_token['type']:
            releation = 0
        elif (my_token['type'] == 's' and opponent_token['type'] == 'p') or (my_token['type'] == 'p' and opponent_token['type'] == 'r') or (my_token['type'] == 'r' and opponent_token['type'] == 's'):
            releation = 1
        elif (my_token['type'] == 's' and opponent_token['type'] == 'r') or (my_token['type'] == 'p' and opponent_token['type'] == 's') or (my_token['type'] == 'r' and opponent_token['type'] == 'p'):
            releation = 2
        return releation


    def new_evaluate(self, my_tokens,opponent_tokens):

        utility = 0
        # 我的每一个手势与敌人每一个手势的优劣，如果手势一样，对分数无影响，如果是压制关系，距离越近，分数越大，如果是被压制关系，距离越远，分数越大
        for my_token in my_tokens:
            for opponent_token in opponent_tokens:
                releation = self.juduge_releation(my_token, opponent_token)
                if releation == 0:
                    continue
                elif releation == 1:
                    distance = self.cal_distance(my_token['position'], opponent_token['position'])
                    if distance == 0:
                        return float('inf')
                    utility += 1/distance
                elif releation == 2:
                    distance = self.cal_distance(my_token['position'], opponent_token['position'])
                    if distance == 0:
                        return -float('inf')
                    utility -= 1/distance
                else:
                    print("judge_releation return wrong result")

        return utility



        ####################################################





    def find_all_distance(self, my_tokens_type,opponent_tokens_type):
        distance_list = []
        for my_token_type in my_tokens_type:
            for opponent_token_type in opponent_tokens_type:
                distance_list.append(Player.cal_distance(my_token_type['position'],opponent_token_type['position']))
        return distance_list

    def cal_distance(my_token_pos,opponent_token_pos):
        r,q = my_token_pos
        i,j = opponent_token_pos
        if (r<0 and i>0) or (r>0 and i<0):
            row_dist = abs(r) + abs(i)
        else:
            row_dist = abs(r - i)
        dist = row_dist
        if r <= i:
            if q - row_dist > j:
                dist += q - row_dist - j
            elif q < j:
                dist += j - q
        else:
            if q + row_dist < j:
                dist += j - q + row_dist
            elif q > j:
                dist += q - j
        return dist

    def find_new_movement_list(self, org_tokens):
        tokens = org_tokens
        Temptokens_list = []
        for token in tokens:
            i,j = token['position']
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1),(i+1,j-1),(i-1,j+1)]:
                if not Player.isOutBound(ni, nj):
                    Temptokens = tokens
                    Temptokens[token['index']].set('position') = (ni, nj)
                    Temptokens_list.append(Temptokens)
        return Temptokens_list

    def isOutBound(r,q) -> bool:
        if q > 4 or q < -4 or r > 4 or r < -4 : return True
        if q == -4 and r < 0 : return True
        if q == -3 and r < -1 : return True
        if q == -2 and r < -2 : return True
        if q == -1 and r < -3 : return True
        if q == 1 and r > 3 : return True
        if q == 2 and r > 2 : return True
        if q == 3 and r > 1 : return True
        if q == 4 and r > 0 : return True
        else : return False

    def isOutBound_throw (pos,self) -> bool:
        r,q = pos
        if self.player == "upper":
            row_lower_bound = 4 - self.allow_row -1
            row_upper_bound = 4
        if self.player == "lower":
            row_lower_bound = -4
            row_upper_bound = -4 + self.allow_row -1
        if q > 4 or q < -4 or r > row_upper_bound or r < row_lower_bound : return True
        if q == -4 and r < 0 : return True
        if q == -3 and r < -1 : return True
        if q == -2 and r < -2 : return True
        if q == -1 and r < -3 : return True
        if q == 1 and r > 3 : return True
        if q == 2 and r > 2 : return True
        if q == 3 and r > 1 : return True
        if q == 4 and r > 0 : return True
        else : return False

