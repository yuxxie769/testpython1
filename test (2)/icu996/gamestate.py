

INVALID_POSITION = (-100, -100) # Set the tokens to this position after death


# Gamestate class：
# saving gamestate,upper or lower, turn, throw times，
# our tokens and opponent's tokens ,how many tokens dead,
# how many s,p,r do I have and how many s,p,r the opponent has and positions
class GameState:
    def __init__(self, player):
        self.isDone = False
        self.identity = player
        self.turnnum = 0

        self.mytokens_on_num = 0
        self.mythrownum = 0
        self.mytokens = {}  
        # for i in range(9):
        #     tokens = Tokens(False, INVALID_POSITION)
        #     self.mytokens.append(tokens)
        self.mytokens_death_num = 0
        self.mytokens_s = 0
        self.mytokens_p = 0
        self.mytokens_r = 0
        # A mapping relationship between positions and pieces, 
        # so that we can quickly get whether there are pieces in a certain position 
        # return a list of pieces
        self.my_pos_tokens = {}

        self.optokens_on_num = 0
        self.opthrownum = 0
        self.optokens = {}
        # for i in range(9):
        #     tokens = Tokens(False, INVALID_POSITION)
        #     self.optokens.append(tokens)
        self.optokens_death_num = 0
        self.optokens_s = 0
        self.optokens_p = 0
        self.optokens_r = 0
        self.op_pos_tokens = {}

    # Maintain the board based on the input actions and game rules
    def update(self,player_action,opponent_action):
        #print(player_action,opponent_action)
        
         # update the gamestate according to op-action
        if len(opponent_action) != 3:
            raise Exception("action is invalid", opponent_action)

        if opponent_action[0] == "THROW":
            # if len(self.optokens) >= 9:
            #     raise Exception("throw num >9", opponent_action)
            # new a token object
            tokens = Tokens(True, opponent_action[1], opponent_action[2])
            # update opponent token dictionary
            self.optokens[self.optokens_on_num] = tokens
            
            if opponent_action[2] in self.op_pos_tokens:
                self.op_pos_tokens[opponent_action[2]].append(self.optokens_on_num)
            
            else:
                index_list = [self.optokens_on_num]
                self.op_pos_tokens[opponent_action[2]] = index_list

             # update information
            self.optokens_on_num += 1
            self.opthrownum += 1
            if opponent_action[1] == "s":
                self.optokens_s += 1
            elif opponent_action[1] == "p":
                self.optokens_p += 1
            elif opponent_action[1] == "r":
                self.optokens_r += 1

        elif opponent_action[0] == "SLIDE":
            if opponent_action[1] in self.op_pos_tokens:
                # Move enemy tokens
                origin_index_list = self.op_pos_tokens[opponent_action[1]] 
                # get a list of index which located in this position
                # all item in this list has a same type so pick the first alive one 
                for k in range(len(origin_index_list)): 
                    origin_index = origin_index_list[k]
                    if self.optokens[origin_index].state:
                        self.op_pos_tokens[opponent_action[1]].pop(k)  #delete this token from list
                        if len(self.op_pos_tokens[opponent_action[1]]) == 0:
                            self.op_pos_tokens.pop(opponent_action[1])  # delete invalid mapping

                        if opponent_action[2] in self.op_pos_tokens:
                            
                            self.optokens[origin_index].position = opponent_action[2]  # update the position of token
                            self.op_pos_tokens[opponent_action[2]].append(origin_index)  

                        # if there is no op-token in this position, new a list to save the index
                        else:
                            self.optokens[origin_index].position = opponent_action[2]  #update position
                            index_list = [origin_index]
                            self.op_pos_tokens[opponent_action[2]] = index_list
                        break
            else:
                raise Exception("something wrong during update op-action", opponent_action)

        elif opponent_action[0] == "SWING":
            if opponent_action[1] in self.op_pos_tokens:
                 # move op token
                origin_index_list = self.op_pos_tokens[opponent_action[1]]  
                # get a list of index which located in this position
                # all item in this list has a same type so pick the first alive one 
                for k in range(len(origin_index_list)):
                    origin_index = origin_index_list[k]
                    if self.optokens[origin_index].state:
                        self.op_pos_tokens[opponent_action[1]].pop(k)  #delete this token from list
                        if len(self.op_pos_tokens[opponent_action[1]]) == 0:
                            self.op_pos_tokens.pop(opponent_action[1])  # delete invalid mapping

                         # if there is a op-token in this position
                        if opponent_action[2] in self.op_pos_tokens:
                                        self.optokens[origin_index].position = opponent_action[2]  
                                        self.op_pos_tokens[opponent_action[2]].append(origin_index)  
                        # if there is no op-token in this position, new a list to save the index
                        else:
                            self.optokens[origin_index].position = opponent_action[2]  
                            index_list = [origin_index]
                            self.op_pos_tokens[opponent_action[2]] = index_list
                        break
            else:
                raise Exception("something wrong during update op-action", opponent_action)

        # update gamestate according to my actions
        # Same logic as update op-actions
        if len(player_action) != 3:
            raise Exception("invalid action", player_action)

        if player_action[0] == "THROW":

            tokens = Tokens(True, player_action[1], player_action[2])
            self.mytokens[self.mytokens_on_num] = tokens
            
            if player_action[2] in self.my_pos_tokens:              
                self.my_pos_tokens[player_action[2]].append(self.mytokens_on_num)
            
            else:
                index_list = [self.mytokens_on_num]
                self.my_pos_tokens[player_action[2]] = index_list

            # update information
            self.mytokens_on_num += 1
            self.mythrownum += 1
            if player_action[1] == "s":
                self.mytokens_s += 1
            elif player_action[1] == "p":
                self.mytokens_p += 1
            elif player_action[1] == "r":
                self.mytokens_r += 1

        elif player_action[0] == "SLIDE":
            #print(self.my_pos_tokens)
            if player_action[1] in self.my_pos_tokens:

                origin_index_list = self.my_pos_tokens[player_action[1]]  
                for k in range(len(origin_index_list)):
                    origin_index = origin_index_list[k]
                    if self.mytokens[origin_index].state:
                        self.my_pos_tokens[player_action[1]].pop(k)  
                        if len(self.my_pos_tokens[player_action[1]]) == 0:
                            self.my_pos_tokens.pop(player_action[1])  

                        if player_action[2] in self.my_pos_tokens:
                                        self.mytokens[origin_index].position = player_action[2]  
                                        self.my_pos_tokens[player_action[2]].append(origin_index)  
                     
                        else:
                            self.mytokens[origin_index].position = player_action[2]  
                            index_list = [origin_index]
                            self.my_pos_tokens[player_action[2]] = index_list
                        break
            else:
                raise Exception("some error happend during update my action", player_action)

        elif player_action[0] == "SWING":
            if player_action[1] in self.my_pos_tokens:
                origin_index_list = self.my_pos_tokens[player_action[1]]  
                for k in range(len(origin_index_list)):
                    origin_index = origin_index_list[k]
                    if self.mytokens[origin_index].state:
                        self.my_pos_tokens[player_action[1]].pop(k)  
                        if len(self.my_pos_tokens[player_action[1]]) == 0:
                            self.my_pos_tokens.pop(player_action[1])  

                        if player_action[2] in self.my_pos_tokens:
                                        self.mytokens[origin_index].position = player_action[2]  
                                        self.my_pos_tokens[player_action[2]].append(origin_index)  
                       
                        else:
                            self.mytokens[origin_index].position = player_action[2]  
                            index_list = [origin_index]
                            self.my_pos_tokens[player_action[2]] = index_list
                        break
            else:
                raise Exception("some error happend during update my action", player_action)

        # pk according to the game rules
        self.pk()

        return

    # get the relation of two tokens, 0 is same,1 is token1 can win,2 is token 2 can win
    def get_relation(self, token1, token2):
        relation = -1
        if token1.type == token2.type:
            relation = 0
        elif (token1.type == 's' and token2.type == 'p') or (
                token1.type == 'p' and token2.type == 'r') or (
                token1.type == 'r' and token2.type == 's') or (
                not token2.state):
            relation = 1
        elif (token1.type == 's' and token2.type == 'r') or (
                token1.type == 'p' and token2.type == 's') or (
                token1.type == 'r' and token2.type == 'p') or (
                not token1.state):
            relation = 2
        return relation

    # pk rules if more than one tokens at one position, start battle and find out which tokens will be defeated
    def pk(self):
        pk_pos = {}
        for pos in self.op_pos_tokens:
            if len(self.op_pos_tokens[pos]) > 1:
                for tonken_index in self.op_pos_tokens[pos]:
                    if pos in pk_pos:
                        pk_pos[pos].append(("op",self.optokens[tonken_index],tonken_index))
                    else:
                        pk_pos[pos]=[("op",self.optokens[tonken_index],tonken_index)]
        for pos in self.my_pos_tokens:
            if len(self.my_pos_tokens[pos]) > 1:
                for tonken_index in self.my_pos_tokens[pos]:
                    if pos in pk_pos:
                        pk_pos[pos].append(("my",self.mytokens[tonken_index],tonken_index))
                    else:
                        pk_pos[pos]=[("my",self.mytokens[tonken_index],tonken_index)]
        for my_pos in self.my_pos_tokens:
            for op_pos in self.op_pos_tokens:
                if my_pos == op_pos:
                    for tonken_index in self.my_pos_tokens[my_pos]:
                        if my_pos in pk_pos:
                            pk_pos[my_pos].append(("my",self.mytokens[tonken_index],tonken_index))
                        else:
                            pk_pos[my_pos]=[("my",self.mytokens[tonken_index],tonken_index)]
                    for tonken_index in self.op_pos_tokens[op_pos]:
                        if op_pos in pk_pos:
                            pk_pos[op_pos].append(("op",self.optokens[tonken_index],tonken_index))
                        else:
                            pk_pos[op_pos]=[("op",self.optokens[tonken_index],tonken_index)]

        for pk_list in list(pk_pos.values()):
            pk_list = list(set(pk_list))
            type_list = []
            for el in pk_list:
                type_list.append(el[1].type)
            if len(list(set(type_list))) == 3:
                for el in pk_list:
                    self.kill_token(el[2],el[0])
            elif len(list(set(type_list))) == 2:
                type1_el = pk_list[0]
                type2_el = None
                for el in pk_list:
                    if el[1].type != type1_el[1].type:
                        type2_el = el
                        break
                if type2_el != None:
                    side1t = type1_el[1]
                    side2t = type2_el[1]
                    relation = self.get_relation(side1t, side2t)
                    if relation == 0:
                        continue
                
                    if relation == 1:
                        for el in pk_list:
                            if el[1].type == type2_el[1].type:
                                self.kill_token(el[2],el[0])

                    if relation == 2:
                        for el in pk_list:
                            if el[1].type == type1_el[1].type:
                                self.kill_token(el[2],el[0])
            else:
                continue
        
        return

    #update tokens which are defeated
    def kill_token(self, index, side):
        if side == "op":
            self.death_update(self.optokens[index].type, True)
            self.optokens_death_num += 1
            self.op_pos_tokens[self.optokens[index].position].remove(index)
            if len(self.op_pos_tokens[self.optokens[index].position]) == 0:
                self.op_pos_tokens.pop(self.optokens[index].position)
            self.optokens[index].state = False
            self.optokens[index].position = INVALID_POSITION
        else:
            self.death_update(self.mytokens[index].type, False)
            self.mytokens_death_num += 1
            self.my_pos_tokens[self.mytokens[index].position].remove(index)
            if len(self.my_pos_tokens[self.mytokens[index].position]) == 0:
                self.my_pos_tokens.pop(self.mytokens[index].position)
            self.mytokens[index].state = False
            self.mytokens[index].position = INVALID_POSITION
    #   update the death number
    def death_update(self, token_type, isopponent):
        if isopponent:
            if token_type == "s":
                self.optokens_s -= 1
            elif token_type == "p":
                self.optokens_p -= 1
            elif token_type == "r":
                self.optokens_r -= 1
        else:
            if token_type == "s":
                self.mytokens_s -= 1
            elif token_type == "p":
                self.mytokens_p -= 1
            elif token_type == "r":
                self.mytokens_r -= 1

# token class:
# state: alive or dead
# type: s,r,p
# position
class Tokens:
    def __init__(self, state, type, position):
        self.state = state
        self.type = type
        self.position = position

