import pandas
from copy import deepcopy
class pre_parsing:
    def __init__(self):
        pass
    def analyse_llone(self):
        while True:
            # 拿出分析栈栈顶符号分析
            s=deepcopy(self.stack)
            x = self.stack.pop()
            # 如果是栈顶符号终结符号
            if x in self.overs:
                # 如果和待分析的符号匹配，分析下一个符号
                if x == self.a:
                    self.precess.append([s,self.string[self.index:],self.a+'匹配'])
                    self.index+=1
                    self.a = self.string[self.index]
                # 如果不匹配，返回False
                else:
                    self.precess.append(['', '', 'OK'])
                    break
            # 如果栈顶符号是'#'
            elif x == '@':
                # 如果和待分析的符号匹配，返回True
                if x == self.a:
                    self.precess.append(['', '', 'OK'])
                    break
                # 如果不匹配，返回False
                else:
                    self.precess.append(['', '', 'Error'])
                    break
            # 如果是非终结符号，将产生式右部元素逆序压入分析栈
            elif self.a in self.analyse_table[x].keys():
                chose = list(reversed(self.analyse_table[x][self.a]))
                self.re_t.append([x,self.analyse_table[x][self.a]])
                self.precess.append([s, self.string[self.index:], self.analyse_table[x][self.a]])
                if (chose != ['ε']):
                    self.stack += chose

            # 如果是未知符号，返回False
            else:
                self.precess.append(['','','Error'])
                break

        # ll(1)文法分析程序入口
    def analyse(self, string,grammar_def):
        self.grammar=grammar_def
        self.re_t=[]
        self.precess = [['栈', '输入缓冲区', '说明']]
        self.type = type
        self.Non = self.grammar['Non-terminal']
        self.start = self.grammar['Start']
        self.overs = self.grammar['Terminator']
        self.analyse_table = self.grammar['Analay_table']
        self.string = string
        self.string.append('@')
        self.stack = ['@', self.start]
        self.index = 0
        self.a = self.string[self.index]
        self.analyse_llone()
        return self.precess
class LL1_parsing:
    def __init__(self):
        self.grammar = pandas.read_pickle('CSV/predict_grammar_table.pickle')
    def analyse_llone(self):
        while True:
            # 拿出分析栈栈顶符号分析
            # print(self.stack)
            # print(self.a)
            x = self.stack.pop()
            # try:
            #     print(self.analyse_table[x].keys())
            # except:
            #     pass
            # 如果是栈顶符号终结符号
            if x in self.overs:
                # 如果和待分析的符号匹配，分析下一个符号
                if x == self.a:
                    if(self.a=='标识符' or self.a=='数值' or self.a=='字符串'):
                        # try:
                        self.re_t.append([x, [str(self.begin+self.index)]])
                        # except:
                        #     pass
                    self.index+=1
                    self.a = self.string[self.index]
                # 如果不匹配，返回False
                else:
                    return [False,1,x]
            # 如果栈顶符号是'#'
            elif x == '@':
                # 如果和待分析的符号匹配，返回True
                if x == self.a:
                    return [True,0,x]
                # 如果不匹配，返回False
                else:
                    return [False,2,x]
            # 如果是非终结符号，将产生式右部元素逆序压入分析栈
            elif self.a in self.analyse_table[x].keys():
                chose = list(reversed(self.analyse_table[x][self.a]))
                self.re_t.append([x,self.analyse_table[x][self.a]])
                if (chose != ['ε']):
                    self.stack += chose
            # 如果是未知符号，返回False
            else:
                return [False, 3, x]

        # ll(1)文法分析程序入口
    def analyse(self, type, string,begin):
        self.begin=begin
        self.re_t=[]
        self.tree={'name':'算术表达式','children':{}}
        self.type = type
        self.Non = self.grammar[self.type]['Non-terminal']
        self.start = self.grammar[self.type]['Start']
        self.overs = self.grammar[self.type]['Terminator']
        self.analyse_table = self.grammar[self.type]['Analay_table']
        self.string = string
        self.string.append('@')
        self.stack = ['@', self.start]
        self.index = 0
        self.a = self.string[self.index]
        s=self.analyse_llone()
        if s[0]:
            print('OK  ', string,type)
            return [True,self.re_t,self.index]
        else:
            print('Fail', string,s[1],type)
            return [False,s[1],self.index]