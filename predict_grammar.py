import pandas
from copy import deepcopy
import pickle
class First_follow:
    def __init__(self, grammar_def):
        self.start = grammar_def["Start"]
        self.overs = grammar_def["Terminator"]
        self.production = grammar_def['Production']
        self.nontermainals = grammar_def['Non-terminal']
        self.first = {nontermainal: {} for nontermainal in self.nontermainals}
        self.follow = {nontermainal: set() for nontermainal in self.nontermainals}
        self.analyse_table = {nontermainal: {} for nontermainal in self.nontermainals}
    # 求first的函数
    def get_first(self, nontermainal):
        ret_dict = {}
        for right in self.production[nontermainal]:
            ret_dict = self.first[nontermainal]
            if (nontermainal, right) in self.first_first:
                continue
            if right != ['ε']:
                if right[0] in self.overs:
                    ret_dict.update({right[0]: right})
                else:
                    for sign in right:
                        if sign in self.nontermainals:
                            first_ = self.first[sign]
                            ret_dict.update({key: right for key in first_.keys()})
                            if 'ε' not in first_.keys():
                                break
            else:
                ret_dict.update({'ε': 'ε'})
        return ret_dict

    # 求first集和follow集
    def get_first_follow(self):
        # 求first第一轮，产生式右部首字符为终结符号
        self.first_first = []
        for nontermainal in self.nontermainals:
            for right in self.production[nontermainal]:
                if right != ['ε'] and right[0] in self.overs:
                    self.first[nontermainal][right[0]] = right
                    if((nontermainal, right) not in self.first_first):
                        self.first_first.append((nontermainal, right))
        # 求first第二轮
        while True:
            old_first = deepcopy(self.first)
            for nontermainal in self.nontermainals:
                self.first[nontermainal].update(self.get_first(nontermainal))
            if old_first == self.first:
                break
        # 起始符号follow集
        self.follow[self.start].add('@')
        # 循环直到follow集不再变化
        while True:
            old_follow = deepcopy(self.follow)
            for nontermainal in self.nontermainals:
                for right in self.production[nontermainal]:
                    for i, sign in enumerate(right):
                        if sign in self.overs:
                            continue
                        if i == len(right) - 1:
                            if(sign!='ε'):
                                self.follow[sign] |= self.follow[nontermainal]
                        elif right[i + 1] in self.overs:
                            self.follow[sign].add(right[i + 1])
                        else:
                            next_set = {key for key in self.first[right[i + 1]].keys()}
                            next_set_without_null = {key for key in self.first[right[i + 1]].keys() if key != ''}
                            self.follow[sign] |= next_set_without_null
                            if 'ε' in next_set:
                                self.follow[sign] |= self.follow[nontermainal]
            if old_follow == self.follow:
                break
        # 将follow集加入first集
        for nontermainal in self.nontermainals:
            if(['ε'] in self.production[nontermainal]):
                if 'ε' in self.first[nontermainal].keys():
                    self.follow[nontermainal] -= {key for key in self.first[nontermainal].keys()}
                    self.first[nontermainal]['ε'] = self.follow[nontermainal]
        self.get_analyse_table()
        return self.analyse_table
    def return_first_follow(self):
        return [self.first,self.follow]

    def get_analyse_table(self):
        # 对于first集中每一个产生式及对应的输入符号
        for nontermainal in self.nontermainals:
            for a, right in self.first[nontermainal].items():
                # 如果输入符号为终结符号，将终结符号、输入符号、产生式右部写入分析表
                if a != 'ε':
                    self.analyse_table[nontermainal][a] = right
                # 如果输入符号是空串，将非终结符号的follow集中每一个符号在分析表中的值写为空串
                else:
                    for b in right:
                        self.analyse_table[nontermainal][b] = 'ε'
class PREE:
    def __init__(self,data):
        self.path='CSV'
        self.data=data
        self.lens=len(self.data)
        self.get_grammar()
        self.get_first_follow()
    def get_grammar(self):#将表格中的文法转为字典存储并记录终结符和非终结符信息
        self.grammar_def = dict()
        self.grammar_def['Start'] = self.data.Left[0]
        self.grammar_def['Non-terminal'] = []
        self.grammar_def['Terminator'] = set()
        self.grammar_def['Production'] = dict()
        for i in range(self.lens):
            self.grammar_def['Non-terminal'].append(self.data.Left[i])#记录非终结符
            if (self.data.Left[i] not in self.grammar_def['Production'].keys()):
                product=self.data.Right[i].split('$')#记录产生式
                node=[]
                for nu in product:
                    node.append(nu.split(' '))
                self.grammar_def['Production'][self.data.Left[i]] = node
            else:
                self.grammar_def['Production'][self.data.Left[i]].append(self.data.Right[i].split('$'))
        nbte=self.grammar_def['Production'].values()
        con_code=self.grammar_def['Non-terminal']
        end_code=set()
        for num in nbte:
            for x in num:
                for char in x:
                    if(char not in con_code and char !='ε'):
                        end_code.add(char)
        self.grammar_def["Terminator"]=end_code
    def get_first_follow(self):
        x=First_follow(self.grammar_def)
        analy=x.get_first_follow()
        first_follow=x.return_first_follow()
        cf = ['']
        content=[]
        for x in self.grammar_def["Terminator"]:
            cf.append(x)
        cf.append('@')
        content.append(cf)
        for x in self.grammar_def['Non-terminal']:
            cf = [x]
            for y in self.grammar_def["Terminator"]:
                if (y in analy[x].keys()):
                    cf.append(analy[x][y])
                else:
                    cf.append('')
            if ('@'in analy[x].keys()):
                cf.append(analy[x]['@'])
            else:
                cf.append('')
            content.append(cf)
        self.grammar_def.update({'Table':content})
        self.grammar_def.update({'Analay_table':analy})
        self.grammar_def.update({'First':first_follow[0]})
        self.grammar_def.update({'Follow': first_follow[1]})

    def return_result(self):
        return self.grammar_def

class predict_grammar:
    def __init__(self):
        self.path='CSV'
        self.data=pandas.read_csv('CSV/grammar.csv')
        self.lens=len(self.data)
        self.get_grammar()
        self.get_first_follow()
    def get_grammar(self):#将表格中的文法转为字典存储并记录终结符和非终结符信息
        self.type=set(self.data.Type)
        self.grammar_def=dict()
        for i in range(self.lens):
            x=self.data.Type[i]
            if(x not in self.grammar_def.keys()):
                self.grammar_def[x]=dict()
                self.grammar_def[x]['Start']=self.data.Left[i]
                self.grammar_def[x]['Non-terminal']=[]
                self.grammar_def[x]['Terminator']=set()
                self.grammar_def[x]['Production']=dict()
            self.grammar_def[x]['Non-terminal'].append(self.data.Left[i])#记录非终结符
            if (self.data.Left[i] not in self.grammar_def[x]['Production'].keys()):
                product=self.data.Right[i].split('$')#记录产生式
                node=[]
                for nu in product:
                    node.append(nu.split(' '))
                self.grammar_def[x]['Production'][self.data.Left[i]] = node
            else:
                self.grammar_def[x]['Production'][self.data.Left[i]].append(self.data.Right[i].split('$'))
        for v in self.grammar_def.keys():#记录终结符
            nbte=self.grammar_def[v]['Production'].values()
            con_code=self.grammar_def[v]['Non-terminal']
            end_code=set()
            for num in nbte:
                for x in num:
                    for char in x:
                        if(char not in con_code and char !='ε'):
                            end_code.add(char)
            self.grammar_def[v]["Terminator"]=end_code
    def get_first_follow(self):
        for v in self.grammar_def.keys():
            result=First_follow(self.grammar_def[v]).get_first_follow()
            self.grammar_def[v].update({'Analay_table':result})
            # for x in self.grammar_def[v].keys():
            #     print(x+':'+str(self.grammar_def[v][x]))
        pickle.dump(self.grammar_def,open('./CSV\predict_grammar_table.pickle','wb'))#将字典写进pkl文件
# predict_grammar()