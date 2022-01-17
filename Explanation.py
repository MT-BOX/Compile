import pandas
import easygui
import tkinter as tk
from tkinter import *
from copy import deepcopy

class explanation:
    def __init__(self, mid_code,symbol_table,path):
        self.mid_code=mid_code
        self.path=path
        self.symbol_table=symbol_table
        self.Temporary_variables=dict()
        self.assignment=['=','+=','-=','*=','/=','&=','|=']
        self.relation=['<','>','<=','>=','!=','==']
        self.oper=['+','-','*','/','&','|','<<','>>','%']
        self.prefix=['++','--','!']
        self.stack=[]
    def find_num(self,name,level):
        choice = level
        if (name in self.symbol_table[choice].keys()):
            return self.symbol_table[choice][name][2],choice
        else:
            i=len(level)-1
            while(i>=0):
                if(level[i]=='-'):
                    choice=level[:i]
                    if(name in self.symbol_table[choice].keys()):
                        return self.symbol_table[choice][name][2],choice
                i-=1
        return name,level
    def get_number(self,two,scope):
        level=scope
        if (type(two) == str):
            if (two[0] == '@'):
                x = self.Temporary_variables[two]
            elif('~'in two):
                fe=two.split('~')
                x,level=self.find_num(fe[0],scope)
                if(fe[1][0].isdigit()):
                    x=x[int(fe[1])]
                elif(fe[1][0]=='@'):
                    x=x[int(self.Temporary_variables[fe[1]])]
                else:
                    y,ll=self.find_num(fe[1],scope)
                    x=x[int(y)]
            else:
                x, level = self.find_num(two, scope)
        else:
            x = two
        return x,level

    def read_num(self):
        while(True):
            result = easygui.enterbox(msg='输入数据', title='解释器数据输入窗')
            if(result!=None):
                self.content+=result+'\n'
                return int(result)
    def run_code(self,Scope_f,fu,len_index,is_insert):
        # print(self.symbol_table)
        self.Four_code = self.mid_code[self.index]
        print(self.Four_code)
        one=self.Four_code[0]
        two=self.Four_code[1]
        three=self.Four_code[2]
        four=self.Four_code[3]
        Scope=self.Four_code[4]
        if(one=='call'):
            if(two=='read'):
                self.index+=2
                self.Temporary_variables['@rt']=self.read_num()
            elif(two=='write'):
                fucion = self.symbol_table['0'][two]
                Scope_fuction = self.mid_code[fucion[4]][4]
                self.index += 1
                i_inde=0
                while (self.mid_code[self.index][0] != 'go'):
                    i_inde = self.run_code(Scope_fuction, fucion, i_inde,False)
            else:
                fucion=self.symbol_table['0'][two]
                Scope_fuction=self.mid_code[fucion[4]][4]
                self.stack.append(deepcopy(self.symbol_table[Scope_fuction]))
                i_inde=0
                self.index+=1
                while(self.mid_code[self.index][0]!='go'):
                    i_inde=self.run_code(Scope_fuction,fucion,i_inde,True)
                print(self.stack)
                new_index=self.index
                self.index=fucion[4]+1
                while(self.mid_code[self.index][0]!='ret'):
                    self.run_code(Scope_fuction, fucion, 0,False)
                if(self.mid_code[self.index][3]!=''):
                    x,level=self.get_number(self.mid_code[self.index][3],Scope_fuction)
                    self.Temporary_variables['@rt']=x
                print(self.Temporary_variables['@rt'])
                self.symbol_table[Scope_fuction]= self.stack.pop()
                print(self.symbol_table[Scope_fuction])
                self.index=new_index+1
        if(one=='para'):
             x, level = self.get_number(two, Scope)
             if(is_insert):
                 self.symbol_table[Scope_f][fu[3][len_index][1]][2]=x
             else:
                 x=str(x)
                 if('\'' in x or '\"' in x):
                     x=x[1:-1]
                 self.content+=x
             self.index += 1
             len_index += 1
        elif(one in self.assignment):
            x, level=self.get_number(two,Scope)
            y, level=self.get_number(four,Scope)
            if one == '=':
                y=x
            elif one == '+=':
                y=x+y
            elif one == '-=':
                y=x-y
            elif one == '*=':
                y=x*y
            elif one == '/=':
                y=x/y
            elif one == '&=':
                y=x&y
            elif one == '|=':
                y=x|y
            if ('~' in four):
                fe = four.split('~')
                if (fe[1][0].isdigit()):
                    deinex=int(fe[1])
                elif (fe[1][0] == '@'):
                    deinex=int(self.Temporary_variables[fe[1]])
                else:
                    df, ll = self.find_num(fe[1], Scope)
                    deinex = int(df)
                self.symbol_table[level][fe[0]][2][deinex] = y
            else:
                self.symbol_table[level][four][2]=y
            self.index+=1
        elif(one in self.oper):
            if(two==''):
                x=0
            else:
                x,level=self.get_number(two,Scope)
            y,level=self.get_number(three,Scope)
            if one == '+':
                z = x + y
            elif one == '-':
                z = x - y
            elif one == '*':
                z = x * y
            elif one == '/':
                z = x / y
            elif one == '%':
                z = x % y
            elif one == '&':
                z = x & y
            elif one == '|':
                z = x | y
            elif one == '>>':
                z = x >> y
            elif one == '<<':
                z = x << y
            if (four[0] == '@'):
                self.Temporary_variables[four] = z
            else:
                self.symbol_table[level][four][2] = z
            self.index += 1
        elif(one in self.relation):
            x,level=self.get_number(two,Scope)
            y,level=self.get_number(three,Scope)
            if one == '<':
                if(x<y):z=1
                else:z=0
            elif one == '>=':
                if (x >= y):z = 1
                else:z = 0
            elif one == '>':
                if (x > y):z = 1
                else:z = 0
            elif one == '<=':
                if (x <= y):z = 1
                else:z = 0
            elif one == '==':
                if (x == y):z = 1
                else:z = 0
            elif one == '!=':
                if (x != y):z = 1
                else:z = 0
            if (four[0] == '@'):
                self.Temporary_variables[four] = z
            else:
                self.symbol_table[level][four][2] = z
            self.index += 1
        elif one in self.prefix:
            x, level = self.find_num(two, Scope)
            if one == '!':
                x=~x
            elif(one == '++'):
                x+=1
            else:
                x-=1
            self.symbol_table[level][two][2] = x
            self.index += 1
        elif one == 'j':
            self.index=four
        elif one == 'jnz':
            x,level=self.get_number(two,Scope)
            if(x>0):
                self.index=four
            else:
                self.index+=1
        else: self.index+=1
        return len_index
    def run_main(self):
        self.content = ''
        self.start = self.symbol_table['0']['main'][4]
        self.index = self.start
        self.Four_code = self.mid_code[self.index]
        while(self.Four_code[0]!='sys'):
            self.run_code('0',self.symbol_table['0']['main'],0,True)
        self.content+='Process over!!!\n'
        for x in self.symbol_table.keys():
            print(x,self.symbol_table[x])
        for x in self.Temporary_variables:
            print(x,self.Temporary_variables[x])
        return self.content
# mid=pandas.read_pickle('work/code6.txt/Mid_code.pickle')
# sym=pandas.read_pickle('work/code6.txt/Symbol_table.pickle')
#
# explanation(mid,sym,'work/code6.txt/')