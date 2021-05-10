

INVALID_POSITION = (-100, -100)  # 棋子死亡后设置为该位置


# 游戏状态类：游戏状态，upperorlower, 游戏轮次，扔的次数，已上场棋子个数，9个棋子对象，自己棋子死亡个数，s个数，p个数，r个数，棋子与位置的对应关系（同理敌人的棋子也需要统计）
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
        # 位置与棋子的映射关系，这样就可以很快得到某一个位置上是否有棋子，返回棋子列表  ？
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

    def update(self,player_action,opponent_action):
        #print(player_action,opponent_action)
        
        # 根据敌人的行动更新游戏状态
        if len(opponent_action) != 3:
            raise Exception("敌人的行动是无效的", opponent_action)

        if opponent_action[0] == "THROW":
            # if len(self.optokens) >= 9:
            #     raise Exception("敌人已经抛了9次了，不能再抛了", opponent_action)
            # new一个棋子对象
            tokens = Tokens(True, opponent_action[1], opponent_action[2])
            # 更新对手棋子字典
            self.optokens[self.optokens_on_num] = tokens
            # 如果这个位置有同一方的棋子
            if opponent_action[2] in self.op_pos_tokens:
                self.op_pos_tokens[opponent_action[2]].append(self.optokens_on_num)
            # 如果这个位置没有同一方的棋子，新建一个list添加新的棋子的index
            else:
                index_list = [self.optokens_on_num]
                self.op_pos_tokens[opponent_action[2]] = index_list

            # 更新已上场棋子个数和扔的总次数  ？
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
                # 移动敌人棋子
                origin_index_list = self.op_pos_tokens[opponent_action[1]]  # 得到该位置上对应棋子的标号列表
                # 这个index_list中一定是同一个类型的棋子，所以只需要选择一个存活的棋子移动即可
                for k in range(len(origin_index_list)): #？？？
                    origin_index = origin_index_list[k]
                    if self.optokens[origin_index].state:
                        self.op_pos_tokens[opponent_action[1]].pop(k)  # 从原来位置的棋子列表中删除这个棋子
                        if len(self.op_pos_tokens[opponent_action[1]]) == 0:
                            self.op_pos_tokens.pop(opponent_action[1])  # 删除遗留下的无效的映射关系

                        # 如果这个位置有同一方的棋子
                        if opponent_action[2] in self.op_pos_tokens:
                            
                            self.optokens[origin_index].position = opponent_action[2]  # 更新这个棋子位置
                            self.op_pos_tokens[opponent_action[2]].append(origin_index)  # 新的位置加入这个棋子 ？？是否要去除原来位置的index？

                        # 如果这个位置没有同一方的棋子，新建一个list添加新的棋子的index
                        else:
                            self.optokens[origin_index].position = opponent_action[2]  # 更新这个棋子位置
                            index_list = [origin_index]
                            self.op_pos_tokens[opponent_action[2]] = index_list
                        break
            else:
                raise Exception("更新敌人游戏状态过程出现了错误", opponent_action)

        elif opponent_action[0] == "SWING":
            if opponent_action[1] in self.op_pos_tokens:
                # 移动敌人棋子
                origin_index_list = self.op_pos_tokens[opponent_action[1]]  # 得到该位置上对应棋子的标号列表
                # 这个index_list中一定是同一个类型的棋子，所以只需要选择一个存活的棋子移动即可
                for k in range(len(origin_index_list)):
                    origin_index = origin_index_list[k]
                    if self.optokens[origin_index].state:
                        self.op_pos_tokens[opponent_action[1]].pop(k)  # 从原来位置的棋子列表中删除这个棋子
                        if len(self.op_pos_tokens[opponent_action[1]]) == 0:
                            self.op_pos_tokens.pop(opponent_action[1])  # 删除遗留下的无效的映射关系

                        # 如果这个位置有同一方的棋子
                        if opponent_action[2] in self.op_pos_tokens:
                                        self.optokens[origin_index].position = opponent_action[2]  # 更新这个棋子位置
                                        self.op_pos_tokens[opponent_action[2]].append(origin_index)  # 新的位置加入这个棋子
                        # 如果这个位置没有同一方的棋子，新建一个list添加新的棋子的index
                        else:
                            self.optokens[origin_index].position = opponent_action[2]  # 更新这个棋子位置
                            index_list = [origin_index]
                            self.op_pos_tokens[opponent_action[2]] = index_list
                        break
            else:
                raise Exception("更新敌人游戏状态过程出现了错误", opponent_action)

        # 根据自己的行动更新游戏状态
        if len(player_action) != 3:
            raise Exception("本方的行动是无效的", player_action)

        if player_action[0] == "THROW":

            # new一个棋子对象
            tokens = Tokens(True, player_action[1], player_action[2])
            # 更新对手棋子字典
            self.mytokens[self.mytokens_on_num] = tokens
            # 如果这个位置有同一方的棋子
            if player_action[2] in self.my_pos_tokens:              
                self.my_pos_tokens[player_action[2]].append(self.mytokens_on_num)
            # 如果这个位置没有同一方的棋子，新建一个list添加新的棋子的index
            else:
                index_list = [self.mytokens_on_num]
                self.my_pos_tokens[player_action[2]] = index_list

            # 更新已上场棋子个数和扔的总次数
            self.mytokens_on_num += 1
            self.mythrownum += 1
            if player_action[1] == "s":
                self.mytokens_s += 1
            elif player_action[1] == "p":
                self.mytokens_p += 1
            elif player_action[1] == "r":
                self.mytokens_r += 1

        elif player_action[0] == "SLIDE":
            # 自身移动或者跳跃更新过程，代码高度重复可以单独写成一个函数
            #print(self.my_pos_tokens)
            if player_action[1] in self.my_pos_tokens:
                # 移动棋子
                origin_index_list = self.my_pos_tokens[player_action[1]]  # 得到该位置上对应棋子的标号列表
                # 这个index_list中一定是同一个类型的棋子，所以只需要选择一个存活的棋子移动即可
                for k in range(len(origin_index_list)):
                    origin_index = origin_index_list[k]
                    if self.mytokens[origin_index].state:
                        self.my_pos_tokens[player_action[1]].pop(k)  # 从原来位置的棋子列表中删除这个棋子
                        if len(self.my_pos_tokens[player_action[1]]) == 0:
                            self.my_pos_tokens.pop(player_action[1])  # 删除遗留下的无效的映射关系

                        # 如果这个位置有同一方的棋子
                        if player_action[2] in self.my_pos_tokens:
                                        self.mytokens[origin_index].position = player_action[2]  # 更新这个棋子位置
                                        self.my_pos_tokens[player_action[2]].append(origin_index)  # 新的位置加入这个棋子
                        # 如果这个位置没有同一方的棋子，新建一个list添加新的棋子的index
                        else:
                            self.mytokens[origin_index].position = player_action[2]  # 更新这个棋子位置
                            index_list = [origin_index]
                            self.my_pos_tokens[player_action[2]] = index_list
                        break
            else:
                raise Exception("更新自身游戏状态过程出现了错误", player_action)

        elif player_action[0] == "SWING":
            if player_action[1] in self.my_pos_tokens:
                # 移动棋子
                origin_index_list = self.my_pos_tokens[player_action[1]]  # 得到该位置上对应棋子的标号列表
                # 这个index_list中一定是同一个类型的棋子，所以只需要选择一个存活的棋子移动即可
                for k in range(len(origin_index_list)):
                    origin_index = origin_index_list[k]
                    if self.mytokens[origin_index].state:
                        self.my_pos_tokens[player_action[1]].pop(k)  # 从原来位置的棋子列表中删除这个棋子
                        if len(self.my_pos_tokens[player_action[1]]) == 0:
                            self.my_pos_tokens.pop(player_action[1])  # 删除遗留下的无效的映射关系

                        # 如果这个位置有同一方的棋子
                        if player_action[2] in self.my_pos_tokens:
                                        self.mytokens[origin_index].position = player_action[2]  # 更新这个棋子位置
                                        self.my_pos_tokens[player_action[2]].append(origin_index)  # 新的位置加入这个棋子
                        # 如果这个位置没有同一方的棋子，新建一个list添加新的棋子的index
                        else:
                            self.mytokens[origin_index].position = player_action[2]  # 更新这个棋子位置
                            index_list = [origin_index]
                            self.my_pos_tokens[player_action[2]] = index_list
                        break
            else:
                raise Exception("更新自身游戏状态过程出现了错误", player_action)

        # 执行完之后，根据游戏规则来决斗
        self.pk()

        return

    # 获得两个棋子之间的关系，返回0是平局，返回1是克制，返回2是被克制，如果有一方棋子已经死亡，默认另一方胜利
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

    # 决斗规则
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
                # 胜利，该位置上所有的敌方棋子设置为死亡，并在删除该位置地方棋子的索引列表
                    if relation == 1:
                        for el in pk_list:
                            if el[1].type == type2_el[1].type:
                                self.kill_token(el[2],el[0])

                    # 失败，该位置上所有的敌方棋子设置为死亡，并在删除该位置地方棋子的索引列表
                    if relation == 2:
                        for el in pk_list:
                            if el[1].type == type1_el[1].type:
                                self.kill_token(el[2],el[0])
            else:
                continue
        
        return
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
    # 棋子死亡时，更新相应类型棋子的死亡个数
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


# 棋子类：棋子状态，棋子类型棋子位置（如果上场的话）
class Tokens:
    def __init__(self, state, type, position):
        self.state = state
        self.type = type
        self.position = position

