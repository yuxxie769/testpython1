from typing import Coroutine
import icu996.gamestate
import copy
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
        self.gamestate = icu996.gamestate.GameState(player)
    
    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here

        action = self.minimax_decision()

        return action

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        self.gamestate.turnnum += 1
        self.gamestate.update(player_action, opponent_action)

    # Determine whether the point is out of bounds
    def isOutBound(self, r, q) -> bool:
        if q > 4 or q < -4 or r > 4 or r < -4: return True
        if q == -4 and r < 0: return True
        if q == -3 and r < -1: return True
        if q == -2 and r < -2: return True
        if q == -1 and r < -3: return True
        if q == 1 and r > 3: return True
        if q == 2 and r > 2: return True
        if q == 3 and r > 1: return True
        if q == 4 and r > 0:
            return True
        else:
            return False

    #find legal throw actions for player
    def find_possible_throw(self,gamestate):
        possible_pos = []
        if gamestate.mythrownum in range(0, 9):
            if gamestate.identity == "lower":
                for i in range(0, gamestate.mythrownum + 1):
                    for j in range(-4,5):
                        if  not self.isOutBound(i-4,j):
                            possible_pos.append((i - 4, j))
            elif gamestate.identity == "upper":
                for i in range(0, gamestate.mythrownum + 1):
                    for j in range(-4,5):
                        if not self.isOutBound(4-i,j):
                            possible_pos.append((4-i,j))
        return possible_pos

    #find legal throw actions for opponent
    def find_op_possible_throw(self,gamestate):
        possible_pos = []
        if gamestate.opthrownum in range(0, 9):
            if gamestate.identity == "lower":
                for i in range(0, gamestate.opthrownum + 1):
                    for j in range(-4,5):
                        if not self.isOutBound(4-i,j):
                            possible_pos.append((4-i,j))
            elif gamestate.identity == "upper":
                for i in range(0, gamestate.opthrownum + 1):
                    for j in range(-4,5):
                        if not self.isOutBound(i - 4, j):
                            possible_pos.append((i - 4, j))
        return possible_pos

    #find legal slide actions for player or opponent
    def find_possible_slide(self,isopponent,position,type,gamestate):
        possible_pos = []
        final_pos = []
        i = position[0]
        j = position[1]
        for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
            if not self.isOutBound(ni, nj):
                possible_pos.append((ni, nj))

        if len(possible_pos) == 6:
            if isopponent:
                tokenlist = list(gamestate.mytokens.values())
            else:
                tokenlist = list(gamestate.optokens.values())
            for token in tokenlist:
                if token.state == False:
                    tokenlist.remove(token)

            nearest_distance = float('inf')
            nearest_pos = None
            for pos in possible_pos:
                    for token in tokenlist:
                        if type == "s":
                            if token.type == "p":
                                tempDistance = self.cal_distance(pos,token.position)
                                if tempDistance < nearest_distance:
                                    nearest_distance = tempDistance
                                    nearest_pos = pos
                        if type == "p":
                            if token.type == "r":
                                tempDistance = self.cal_distance(pos,token.position)
                                if tempDistance < nearest_distance:
                                    nearest_distance = tempDistance
                                    nearest_pos = pos
                        if type == "r":
                            if token.type == "s":
                                tempDistance = self.cal_distance(pos,token.position)
                                if tempDistance < nearest_distance:
                                    nearest_distance = tempDistance
                                    nearest_pos = pos
            if nearest_pos != None:
                final_pos.append(nearest_pos)
                possible_pos.remove(nearest_pos)
                resultList=random.sample(range(0,5),2)
                for i in resultList:
                    final_pos.append(possible_pos[i])
            else:
                resultList=random.sample(range(0,6),3)
                for i in resultList:
                    final_pos.append(possible_pos[i])

            return final_pos
        return possible_pos

    #find legal swing actions for player or opponent
    def find_possible_swing(self, position, center_pos):
        possible_pos = []
        finnal_pos = []
        r, q = position
        for center in center_pos:
            i, j = center
            deltaR = r - i
            deltaQ = q - j
            if deltaR == 1 and deltaQ == 0:
                possible_pos.append(self.find_pos_by_direction(center, "rightDown"))
                possible_pos.append(self.find_pos_by_direction(center, "leftDown"))
                possible_pos.append(self.find_pos_by_direction(center, "left"))
            elif deltaR == 0 and deltaQ == 1:
                possible_pos.append(self.find_pos_by_direction(center, "leftUp"))
                possible_pos.append(self.find_pos_by_direction(center, "leftDown"))
                possible_pos.append(self.find_pos_by_direction(center, "left"))
            elif deltaR == -1 and deltaQ == 1:
                possible_pos.append(self.find_pos_by_direction(center, "rightUp"))
                possible_pos.append(self.find_pos_by_direction(center, "leftUp"))
                possible_pos.append(self.find_pos_by_direction(center, "left"))
            elif deltaR == -1 and deltaQ == 0:
                possible_pos.append(self.find_pos_by_direction(center, "leftUp"))
                possible_pos.append(self.find_pos_by_direction(center, "rightUp"))
                possible_pos.append(self.find_pos_by_direction(center, "right"))
            elif deltaR == 0 and deltaQ == -1:
                possible_pos.append(self.find_pos_by_direction(center, "rightUp"))
                possible_pos.append(self.find_pos_by_direction(center, "rightDown"))
                possible_pos.append(self.find_pos_by_direction(center, "right"))
            elif deltaR == 1 and deltaQ == -1:
                possible_pos.append(self.find_pos_by_direction(center, "rightDown"))
                possible_pos.append(self.find_pos_by_direction(center, "leftDown"))
                possible_pos.append(self.find_pos_by_direction(center, "right"))
            if len(possible_pos) != 0:
                finnal_pos.append(random.choice(possible_pos))
                possible_pos = []
        return finnal_pos

    #return the position of a token's next step
    def find_pos_by_direction(self, position, direction):
        r, q = position
        if direction == "right" and not self.isOutBound(r, q + 1):
            possible_pos = (r, q + 1)
        elif direction == "rightUp" and not self.isOutBound(r + 1, q):
            possible_pos = (r + 1, q)
        elif direction == "rightDown" and not self.isOutBound(r - 1, q + 1):
            possible_pos = (r - 1, q + 1)
        elif direction == "left" and not self.isOutBound(r, q - 1):
            possible_pos = (r, q - 1)
        elif direction == "leftUp" and not self.isOutBound(r + 1, q - 1):
            possible_pos = (r + 1, q - 1)
        elif direction == "leftDown" and not self.isOutBound(r - 1, q):
            possible_pos = (r - 1, q)
        else:
            return None
        return possible_pos

    # find player's token is swingable or not
    def is_my_swingable(self, my_position,gamestate):
        
        swingable = False
        center_pos = []
        i = my_position[0]
        j = my_position[1]
        for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
            if not self.isOutBound(ni, nj) and gamestate.my_pos_tokens.get((ni, nj)) != None:
                center_pos.append((ni, nj))
        if len(center_pos) > 0:
            swingable = True
        return swingable, center_pos

    # find opponent's token is swingable or not
    def is_op_swingable(self, op_position,gamestate):
        swingable = False
        center_pos = []
        i = op_position[0]
        j = op_position[1]
        for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
            if not self.isOutBound(ni, nj) and gamestate.op_pos_tokens.get((ni, nj)) != None:
                center_pos.append((ni, nj))
        if len(center_pos) > 0:
            swingable = True
        return swingable, center_pos

    #simplify the actions list before take the list as branch factors
    def preEval(self,actions_list,isopponent,gamestate):
        if gamestate.mythrownum == 0 or gamestate.opthrownum == 0:
            random_action = random.choice(actions_list)
            new_actions_list = [random_action]
            return new_actions_list
        new_actions_list = self.type_unequal(actions_list,isopponent,gamestate)
        new_actions_list = self.find_important_move(new_actions_list,isopponent,gamestate)

        return new_actions_list

    #find tho token in side1_list which is most close to any tokens in side2_list
    def find_nearest_pos(self,side1_list,side2_list):
        nearest_distance = float('inf')
        nearest_pos = (5,5)
        for token_1 in side1_list:
            for token_2 in side2_list:
                tempDistance = self.cal_distance(token_1.position,token_2.position)
                if tempDistance < nearest_distance:
                    nearest_distance = tempDistance
                    nearest_pos = token_1.position
        return nearest_pos

    #find player or opponent's "urgent" tokens' action
    #not "urgent" tokens' action will be removed from the action list through this method
    def find_important_move(self,actions_list,isopponent,gamestate):
        my_r = gamestate.mytokens_r
        my_p = gamestate.mytokens_p
        my_s = gamestate.mytokens_s
        op_r = gamestate.optokens_r
        op_p = gamestate.optokens_p
        op_s = gamestate.optokens_s
        
        if (my_r != 0 and op_r != 0 and my_p + my_s + op_p + op_s == 0):
            return actions_list
        if (my_p != 0 and  op_p != 0 and my_r + my_s + op_r + op_s == 0):
            return actions_list
        if (my_s != 0 and  op_s != 0 and my_p + my_r + op_p + op_r == 0):
            return actions_list
        if (op_s + op_p + op_r == 0) or (my_s + my_p + my_r == 0):
            return actions_list
        

        op_r_list = []
        op_p_list = []
        op_s_list = []
        my_r_list = []
        my_p_list = []
        my_s_list = []

        optokenlist = list(gamestate.optokens.values())
        for token in optokenlist:
            if token.state == False:
                optokenlist.remove(token)
        mytokenlist = list(gamestate.mytokens.values())
        for token in mytokenlist:
            if token.state == False:
                mytokenlist.remove(token)

        for token in optokenlist:
            if token.type == "r":
                op_r_list.append(token)
            if token.type == "s":
                op_s_list.append(token) 
            if token.type == "p":
                op_p_list.append(token) 
        for token in mytokenlist:
            if token.type == "r":
                my_r_list.append(token) 
            if token.type == "s":
                my_s_list.append(token) 
            if token.type == "p":
                my_p_list.append(token) 
        
        newList = []
        if isopponent:
            if op_r != 0:
                if my_p != 0:
                    nearest_pos = self.find_nearest_pos(op_r_list,my_p_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
                if my_s != 0:
                    nearest_pos = self.find_nearest_pos(op_r_list,my_s_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
            if op_p != 0:
                if my_r != 0:
                    nearest_pos = self.find_nearest_pos(op_p_list,my_r_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
                if my_s != 0:
                    nearest_pos = self.find_nearest_pos(op_p_list,my_s_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
            if op_s != 0:
                if my_p != 0:
                    nearest_pos = self.find_nearest_pos(op_s_list,my_p_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
                if my_r != 0:
                    nearest_pos = self.find_nearest_pos(op_s_list,my_r_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
        else:
            if my_r != 0:
                if op_p != 0:
                    nearest_pos = self.find_nearest_pos(my_r_list,op_p_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
                if op_s != 0:
                    nearest_pos = self.find_nearest_pos(my_r_list,op_s_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
            if my_p != 0:
                if op_r != 0:
                    nearest_pos = self.find_nearest_pos(my_p_list,op_r_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
                if op_s != 0:
                    nearest_pos = self.find_nearest_pos(my_p_list,op_s_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
            if my_s != 0:
                if op_p != 0:
                    nearest_pos = self.find_nearest_pos(my_s_list,op_p_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
                if op_r != 0:
                    nearest_pos = self.find_nearest_pos(my_s_list,op_r_list)
                    for action in actions_list:
                        if action[1] == nearest_pos:
                            newList.append(action)
        for action in actions_list:
            if action[0] == "THROW":
                newList.append(action)
        return list(set(newList))
            
                        

    #decide which throw action can remain and to be a branch factor
    #in most cases, most of throw action will be removed from action list by this method
    def type_unequal(self,actions_list,isopponent,gamestate):
        my_r = gamestate.mytokens_r
        my_p = gamestate.mytokens_p
        my_s = gamestate.mytokens_s
        op_r = gamestate.optokens_r
        op_p = gamestate.optokens_p
        op_s = gamestate.optokens_s
        newList = []
        if isopponent:
            if gamestate.opthrownum <= 4:
                
                if my_p > op_s:
                    near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"s","p")
                    if near_action != None:
                        newList.append(near_action)
                if my_s > op_r:
                    near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"r","s")
                    if near_action != None:
                        newList.append(near_action)
                if my_r > op_p:
                    near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"p","r")
                    if near_action != None:
                        newList.append(near_action)
                for action in actions_list:
                        if action[0] != "THROW":
                            newList.append(action)
                return newList
            
            if (op_r == 0 and my_s != 0) or (my_s - op_r > 1):
                near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"r","s")
                if near_action != None:
                        newList.append(near_action)
            if (op_p == 0 and my_r != 0) or (my_r - op_p > 1):
                near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"p","r")
                if near_action != None:
                        newList.append(near_action)
            if (op_s == 0 and my_p != 0) or (my_p - op_s > 1):
                near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"s","p")
                if near_action != None:
                        newList.append(near_action)
            for action in actions_list:
                        if action[0] != "THROW":
                            newList.append(action)
            return newList
        ##our side
        else:
            if gamestate.mythrownum <= 4:

                if op_p > my_s:
                    near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"s","p")
                    if near_action != None:
                        newList.append(near_action)
                if op_s > my_r:
                    near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"r","s")
                    if near_action != None:
                        newList.append(near_action)
                if op_r > my_p:
                    near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"p","r")
                    if near_action != None:
                        newList.append(near_action)
                for action in actions_list:
                        if action[0] != "THROW":
                            newList.append(action)
                return newList

            if (my_s == 0 and op_p != 0) or (op_p - my_s > 1):
                near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"s","p")
                if near_action != None:
                        newList.append(near_action)
            if (my_r == 0 and op_s != 0) or (op_s - my_r > 1):
                near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"r","s")
                if near_action != None:
                        newList.append(near_action)
            if (my_p == 0 and op_r != 0) or (op_r - my_p > 1):
                near_action = self.find_nearest_action(isopponent,actions_list,gamestate,"p","r")
                if near_action != None:
                        newList.append(near_action)
            for action in actions_list:
                        if action[0] != "THROW":
                            newList.append(action)
            return newList


    #find the best thorw action
    # in this case "the best" mean the most close position to the token which can be defeated
    def find_nearest_action(self,isopponent,actions_list,gamestate,type1,type2):
        if isopponent:
            tokenlist = list(gamestate.mytokens.values())
            for token in tokenlist:
                if token.state == False:
                    tokenlist.remove(token)


            nearest_distance = float('inf')
            nearest_action = None
            for token in tokenlist:
                if token.type == type2:
                    for action in actions_list:
                        if action[1] == type1:
                            tempDistance = self.cal_distance(action[2],token.position)
                            if tempDistance < nearest_distance:
                                nearest_distance = tempDistance
                                nearest_action = action
            return nearest_action
            
        else:
            tokenlist = list(gamestate.optokens.values())
            for token in tokenlist:
                if token.state == False:
                    tokenlist.remove(token)

            nearest_distance = float('inf')
            nearest_action = None
            for token in tokenlist:
                if token.type == type2:
                    for action in actions_list:
                        if action[1] == type1:
                            tempDistance = self.cal_distance(action[2],token.position)
                            if tempDistance < nearest_distance:
                                nearest_distance = tempDistance
                                nearest_action = action
            return nearest_action

    #return an action list as player's action options
    #actions in action list will become branch factors for search method
    def find_my_possible_actions(self,gamestate):
        actions_list = []
        types = ["s", "r", "p"]
        if gamestate.mythrownum in range(0, 9):
            throw_pos = self.find_possible_throw(gamestate)
            for pos in throw_pos:
                for type in types:
                    actions_list.append(("THROW", type, pos))
        for mytoken in list(gamestate.mytokens.values()):
            # if token is alive
            if mytoken.state:
                slide_position = self.find_possible_slide(False,mytoken.position,mytoken.type,gamestate)
                for pos in slide_position:
                    actions_list.append(("SLIDE", mytoken.position, pos))
                swingable, center_pos = self.is_my_swingable(mytoken.position,gamestate)
                if swingable:
                    swing_position = self.find_possible_swing(mytoken.position, center_pos)
                    for pos in swing_position:
                        if pos != None:
                            actions_list.append(("SWING", mytoken.position, pos))
        actions_list = self.my_action_cut_off(actions_list,gamestate)
        if gamestate.mythrownum < 9:
            actions_list = self.preEval(actions_list,False,gamestate)
        
        return actions_list

    #return an action list as opponent's action options
    #actions in action list will become branch factors for search method
    def find_op_possible_actions(self,gamestate):
        actions_list = []
        types = ["s", "r", "p"]
        if gamestate.opthrownum in range(0, 9):
            throw_pos = self.find_op_possible_throw(gamestate)
            for pos in throw_pos:
                for type in types:
                    actions_list.append(("THROW", type, pos))
        for optoken in list(gamestate.optokens.values()):
            # if token is alive
            if optoken.state:
                slide_position = self.find_possible_slide(True,optoken.position,optoken.type,gamestate)
                for pos in slide_position:
                    actions_list.append(("SLIDE", optoken.position, pos))
                swingable, center_pos = self.is_op_swingable(optoken.position,gamestate)
                if swingable:
                    swing_position = self.find_possible_swing(optoken.position, center_pos)
                    for pos in swing_position:
                        if pos != None:
                            actions_list.append(("SWING", optoken.position, pos))
        actions_list = self.op_action_cut_off(actions_list,gamestate)
        if gamestate.opthrownum < 9:
            actions_list = self.preEval(actions_list,True,gamestate)
        return actions_list
    
    #entry of minimax search
    #return the best action to action method
    def minimax_decision(self):
        utilityList = []
        temp_gamestate = copy.deepcopy(self.gamestate)
        
        my_action_list = self.find_my_possible_actions(temp_gamestate)
        currMax = -float('inf')
        for my_action in my_action_list:
            deepth = 0
            utility = self.min_value(my_action,temp_gamestate,deepth,currMax)
            utilityList.append(utility)
            if currMax < utility: currMax = utility
        dicided_action = my_action_list[utilityList.index(max(utilityList))]
        return dicided_action

    #minimum part of search, return the smallest utility
    def min_value(self,my_action,gamestate,deepth,currMax):
        deepth += 1
        utilityList = []
        op_action_list = self.find_op_possible_actions(gamestate)
        currMin = float('inf')
        count = 0
        for op_action in op_action_list:
            count += 1
            utility = self.max_value(my_action,op_action,gamestate,deepth,currMin)
            utilityList.append(utility)
            try:
                if currMin > utility: currMin = utility
            except:
                print("catch op_action_list!",op_action_list)
                print("catch op_action!",op_action)
                print("catch previous my_action!",my_action)
                print("catch deepth!!",deepth)
                print("catch utility!!!",utility)
                print("catch count!!!",count)
            else:
                if currMax >= utility: break
        if len(utilityList) == 0:
                utility = -90000
        else:
            utility = min(utilityList)
        count = 0
        if utility == None:
                raise Exception("utility is none!!!in 651")
        return utility
    
    #maximum part of search, return the biggest utility
    def max_value(self,my_action,op_action,gamestate,deepth,currMin):
        deepth += 1
        newstate = copy.deepcopy(gamestate)
        newstate.update(my_action,op_action)
        if self.isEnd(newstate,deepth):
            utility = self.new_evaluate(newstate)
            if utility == None:
                raise Exception("utility is none!!!in 660")
            return utility
        else:
            my_action_list = self.find_my_possible_actions(newstate)
            utilityList = []
            count = 0
            currMax = -float('inf')
            for new_my_action in my_action_list:
                count += 1
                utility = self.min_value(new_my_action,newstate,deepth,currMax)
                utilityList.append(utility)
                try:
                    if currMax < utility: currMax = utility
                except:
                    print("catch my_action_list!",my_action_list)
                    print("catch new_my_action!",new_my_action)
                    print("catch previous my_action!",my_action)
                    print("catch previous op_action!",op_action)
                    print("catch deepth!!",deepth)
                    print("catch utility!!!",utility)
                    print("catch count!!!",count)
                else:
                    if currMin <= utility: break
            if len(utilityList) == 0:
                utility = -90000
            else:
                utility = max(utilityList)
            if utility == None:
                raise Exception("utility is none!!!in 685")
            return utility

    #decide the search can be terminated or not 
    def isEnd(self,gamestate,deepth):
        if gamestate.mytokens_death_num == 9 or gamestate.optokens_death_num == 9 or deepth == 4 or self.isDraw(gamestate):
            return True
        else: return False
    #find current game is draw or not
    def isDraw(self,gamestate):
        if gamestate.mytokens_on_num == 9 and gamestate.optokens_on_num == 9:
            my_tokens_type = []
            opponent_tokens_type = []
            for my_key in gamestate.mytokens:
                if gamestate.mytokens[my_key].state:
                    my_tokens_type.append(gamestate.mytokens[my_key].type)
            for op_key in gamestate.optokens:
                if gamestate.optokens[op_key].state:
                    opponent_tokens_type.append(gamestate.optokens[op_key].type)
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


    def new_evaluate(self,gamestate):

        utility = 0
        
        for my_key in gamestate.mytokens:
            for op_key in gamestate.optokens:
                if gamestate.mytokens[my_key].state :
                    my_token = gamestate.mytokens[my_key]
                    if gamestate.optokens[op_key].state :
                        opponent_token = gamestate.optokens[op_key]
                        releation = gamestate.get_relation(my_token, opponent_token)
                        if releation == 0:
                            continue
                        elif releation == 1:
                            distance = self.cal_distance(my_token.position, opponent_token.position)
                            if distance == 0:
                                return float('inf')
                            utility += 100/distance
                        elif releation == 2:
                            distance = self.cal_distance(my_token.position, opponent_token.position)
                            if distance == 0:
                                return -float('inf')
                            utility -= 100/distance
                        else:
                            print("judge_releation return wrong result")
        # if gamestate.mytokens_s > gamestate.optokens_p and gamestate.optokens_p != 0:
        #     utility += 10
        # if gamestate.mytokens_r > gamestate.optokens_s and gamestate.optokens_p != 0:
        #     utility += 10
        # if gamestate.mytokens_p > gamestate.optokens_r and gamestate.optokens_p != 0:
        #     utility += 10
        # if gamestate.optokens_p > gamestate.mytokens_r and gamestate.mytokens_r != 0:
        #     utility -= 10
        # if gamestate.optokens_s > gamestate.mytokens_p and gamestate.mytokens_p != 0:
        #     utility -= 10
        # if gamestate.optokens_r > gamestate.mytokens_s and gamestate.mytokens_s != 0:
        #     utility -= 10

        utility -= 10000 * gamestate.mytokens_death_num
        utility += 10000 * gamestate.optokens_death_num

        if utility == None:
            utility = -90000

        return utility



        ####################################################

    #caculate distance between two positions
    def cal_distance(self,my_token_pos,opponent_token_pos):
        
        r,q = my_token_pos
        i,j = opponent_token_pos
        row_dist = abs(r - i)
        dist = row_dist
        if r <= i:
            if q >= j and i+j >= q+r:
                dist += 0
            elif i+j < q+r:
                dist += abs((q + r) - (i + j))
            else:
                dist += abs(j - q)
        else:
            if q <= j and i+j <= q+r:
                dist += 0
            elif i+j > q+r:
                dist += abs((q + r) - (i + j))
            else:
                dist += abs(q - j)
        return dist
#######################################3
#If the type of tokens and their target position are the same then pruning,
# if the there is my token in the target position then pruning
    def my_action_cut_off(self,action_list,state):
        new_list = []
        position_dic = {}
        for action in action_list:
            if action[2] in state.my_pos_tokens:
                continue
            else:
                if action[0]=="THROW":
                    type_position= (action[1],action[2])
                else:
                    my_index = state.my_pos_tokens[action[1]][0]
                    my_type = state.mytokens[my_index].type
                    type_position = (my_type,action[2])
                if not type_position in position_dic:
                    position_dic[type_position] = action
                #priority: swing > slide > throw
                elif action[0] == "SWING":
                    position_dic[type_position] = action
                elif action[0] == "SLIDE" and  position_dic[type_position][0] == "THROW":
                    position_dic[type_position] = action
                else:
                    continue
        new_list = list(position_dic.values())
        if len(new_list) == 0:
            print("my_old actions list",action_list)
        return new_list

    def op_action_cut_off(self,action_list,state):
        new_list = []
        position_dic = {}
        for action in action_list:
            if action[2] in state.op_pos_tokens:
                continue
            else:
                if action[0]=="THROW":
                    type_position= (action[1],action[2])
                else:
                    op_index = state.op_pos_tokens[action[1]][0]
                    op_type = state.optokens[op_index].type
                    type_position = (op_type,action[2])
                if not type_position in position_dic:
                    position_dic[type_position] = action
                elif action[0] == "SWING":
                    position_dic[type_position] = action
                elif action[0] == "SLIDE" and  position_dic[type_position][0] == "THROW":
                    position_dic[type_position] = action
                else:
                    continue
        new_list = list(position_dic.values())
        if len(new_list) == 0:
            print("old actions list",action_list)
        return new_list

