import pandas
import pickle
import json
import os
import Predict_parsing
from copy import deepcopy
from pyecharts import options as opts
from pyecharts.charts import Page, Tree

class Create_tree:
    def __init__(self, result):
        self.result=result
        self.lens=len(self.result)
        self.index=0
        self.tree=[{'name':result[0][0]}]
        self.get_tree(self.tree)
    def return_tree(self):
        return self.tree
    def get_tree(self,dicts):
        flag=-1
        if(self.index==self.lens):
            return True
        x=self.result[self.index]
        for i in range(len(dicts)):
            if (dicts[i]['name']==x[0]):
                flag=i
        if(flag>=0):
            node=dicts[flag]
            if('ε' not in x[1]):
                node['children']=[]
                for i in range(len(x[1])):
                    node['children'].append({'name': x[1][i]})
                self.index+=1
                Isok=True
                for j in range(len(x[1])):
                    Isok=self.get_tree(node['children'])
                    if(Isok):
                        break
                return Isok
            else:
                dicts.pop(flag)
                self.index+=1
                return False
        else:
            return False


class Parsing:
    def __init__(self,armmessage,path):
        self.path=path
        self.armmessage=armmessage
        self.lens=len(self.armmessage)
        self.row=1
        self.index=0
        self.begin=0
        self.type=0
        self.string=[]
        self.break_word=['break','continue']
        self.keyword=['int','void','double','float','char','long','short']
        self.equal=['=','*=','/=','+=','-=','&=','|=']
        self.errors=[]
        self.tree=[{'name':'File','children':[]}]
        self.grammar=Predict_parsing.LL1_parsing()
        self.analyse_main(self.tree[0])

    def find_catch(self,x,y,index):#寻找到匹配字段
        i=index
        row=self.armmessage.row[i]
        if(x=='$'):
          stack=[x]
        else:
          stack=[]
        flag=1
        end=i
        while(True):
            if (i == self.lens):
                return ['', end, False]
            m = self.armmessage.loc[i]
            if(m[1]==0):
                self.string.append('标识符')
            elif(str(m[1])[0]=='4'):
                self.string.append('数值')
            else:
                self.string.append(m[0])
            if(m[2]!=row and flag==1 ):
                end=i-1
                flag=0

            if(m[0]==x):
                stack.append(x)
            elif(m[0]in y):
                if(stack[-1]==x):
                    stack.pop()
                    if(len(stack)==0):
                        s=deepcopy(self.string)
                        self.string.clear()
                        return [s,i,True]
            i+=1
    def single_pression(self,result_t,fl,index,tree):
        print(result_t)
        choo=[]
        if(fl==0):
            choo=['++','--']
        flag=1
        cg=0
        for cg in range(len(result_t)):
            if(result_t[cg]in self.equal):
                if(cg>0):
                    if(result_t[cg-1]=='标识符'):
                        pass
                    elif(cg>1):
                        if(result_t[cg-1]in choo):
                            if(result_t[cg-2]=='标识符'):
                                pass
                            else:
                                flag=0
                                break
                        elif(cg>3):
                            if(result_t[cg-1]==']'):
                                t_flag = False  # 标记[]
                                cb=cg-3
                                while(cb>=1):
                                    if(result_t[cb]=='['):
                                        t_flag=True
                                        break
                                    cb-=1
                                if(t_flag):
                                    if(result_t[cb-1]!='标识符'):
                                        flag=0
                                        break
                                    else:
                                       pass
                                else:
                                    flag = 0
                                    break
                            else:
                                flag = 0
                                break
                        else:
                            flag = 0
                            break
                    else:
                        flag=0
                        break
                else:
                    flag = 0
                    break
        if(flag==1):
            # print(index)
            # print(self.armmessage.loc[index])
            s_back=self.grammar.analyse('Expresion', result_t,index)
            if (s_back[0]):
                if(len(s_back[1])==1):
                    tree .append( {'name':'空语句'})
                else:
                    cv=Create_tree(s_back[1])
                    data=cv.return_tree()
                    tree+=data
            else:
                self.errors.append(['EPP-0'+str(s_back[1]),self.armmessage.loc[index+s_back[2]]])
        else:
            self.errors.append(['EPP-06', self.armmessage.loc[index + cg]])
    #单语句分析
    def one_sentence(self,index,tree,max_index):
        result_m = self.find_catch('$', [';'], index)
        print(result_m)
        if (result_m[2] == True and result_m[1]<=max_index):
            self.single_pression(result_m[0][:-1], 0, index,tree)
            index = result_m[1] + 1
        else:
            self.errors.append(['EPS-03', self.armmessage.loc[result_m[1]]])
            index=max_index
        return index
    #{}分析
    def is_body(self,m,m_index,tree,max_index):
        if (m[0] == '{'):
            result_m = self.find_catch('{', ['}'], m_index)
            if (result_m[2] == False or result_m[1]>=max_index):
                m_index=max_index
                self.errors.append(['EPS-01',self.armmessage.loc[result_m[1]]])
                return m_index
            else:
                print('进入大括号语句块')
                div = {'name': '大括号语句', 'children': []}
                tree.append(div)
                self.function_body(m_index, result_m, div['children'])
                m_index=result_m[1]+1
        elif (m[0] == '#'):
            self.index = self.Declaration(self.index, tree['children'])
        elif(m[0] == 'for'):
            m_index += 1
            div = {'name': 'For循环语句', 'children': []}
            tree.append(div)
            print('进入For循环')
            m_index = self.forstatement(m_index, div['children'],max_index)
            print('离开For循环')
        elif (m[0] == 'if'):
            print('进入if判断')
            div = {'name': 'if判断语句', 'children': [{'name':'if'}]}
            tree.append(div)
            m_index = self.if_else(m_index, div['children'],max_index)
            print('离开if判断')
        elif (m[1] >= 101 and m[1] <= 107):
            m_index += 1
            n = self.armmessage.loc[m_index]
            if (n[1] != 0):
                self.errors.append(['EPD-01', n])
            else:
                dicts = {'name': '标识符定义', 'children': [{'name': '数值类型', 'children': [{'name': str(m_index-1)}]}]}
                tree.append(dicts)
                m_index = self.define_Identifier(m_index, dicts['children'],max_index)
        elif (m[0] == 'do'):
            print('进入do循环')
            div = {'name': 'do循环语句', 'children': [{'name':'do'}]}
            tree.append(div)
            m_index = self.do_while(m_index, div['children'], max_index)
            print('离开do循环')
        elif (m[0] == 'while'):
            print('进入while循环')
            div = {'name': 'while循环语句', 'children': [{'name':'while'}]}
            tree.append(div)
            m_index = self.whilestatement(m_index, div['children'], max_index)
            print('离开while循环')
        elif (m[0] == 'return'):
            dicts = {'name': '返回值语句', 'children': [{'name': str(m_index)}]}
            tree.append(dicts)
            m_index += 1
            s = self.armmessage.loc[m_index]
            if (s[0] != ';'):
                m_index = self.one_sentence(m_index, dicts['children'],max_index)
            else:
                m_index+=1
        elif(m[0] in self.break_word):
            tree.append({'name':'跳转语句','children':[{'name':str(m_index)}]})
            m_index+=1
            m=self.armmessage.loc[m_index]
            if(m[0]!=';'):
                self.errors.append(['EPS-03', self.armmessage.loc[m_index-1]])
            else:
                m_index+=1
        else:
            dicts = {'name': '单行表达式语句', 'children': []}
            tree.append(dicts)
            m_index = self.one_sentence(m_index,dicts['children'],max_index)
        return m_index

    #判断语句分析
    def if_else(self,m_index,tree,max_index):
        m_index += 1
        result = self.find_catch('(', [')'], m_index)
        if(result[2]==True and result[1]<max_index):
            if(m_index!=result[1]-1):
                div={'name':'判断语句','children':[]}
                tree.append(div)
                self.single_pression(result[0][1:-1], 0, m_index+1,div['children'])
                m_index = result[1]
                m_index += 1
                m = self.armmessage.loc[m_index]
                s_tree = {'name': '是语句块', 'children': []}
                tree.append(s_tree)
                m_index = self.is_body(m, m_index,s_tree['children'],max_index)
                m = self.armmessage.loc[m_index]
                if (m[0] == 'else'):
                    tree.append({'name':'else'})
                    s_tree={'name': '非语句块','children':[]}
                    tree.append(s_tree)
                    m_index += 1
                    m = self.armmessage.loc[m_index]
                    m_index= self.is_body(m, m_index,s_tree['children'],max_index)
                else:
                    return m_index
            else:
                m_index=result[1]+1
                self.errors.append(['EPI-01', self.armmessage.loc[result[1]]])
        else:
            m_index=max_index
            self.errors.append(['EPS-02', self.armmessage.loc[result[1]]])
        return m_index
    def do_while(self,m_index,tree,max_index):
        m_index+=1
        m = self.armmessage.loc[m_index]
        dic = {'name': '循环体', 'children': []}
        tree.append(dic)
        m_index = self.is_body(m, m_index, dic['children'],max_index)
        m = self.armmessage.loc[m_index]
        if(m[0]=='while'):
            tree.append({'name': 'while'})
            m_index+=1
            result = self.find_catch('(', [')'], m_index)
            if (result[2] == True and result[1] < max_index):
                if(m_index!=result[1]-1):
                    div = {'name': '判断语句', 'children': []}
                    tree.append(div)
                    self.single_pression(result[0][1:-1], 0, m_index+1, div['children'])
                    m_index = result[1]+1
                    m = self.armmessage.loc[m_index]
                    if(m[0]!=';' or m_index >= max_index ):
                        self.errors.append(['EPW-02', self.armmessage.loc[result[1]]])
                    else:
                        m_index+=1
                else:
                    m_index = result[1] + 1
                    self.errors.append(['EPW-03', self.armmessage.loc[result[1]]])
            else:
                m_index = max_index
                self.errors.append(['EPS-02', self.armmessage.loc[result[1]]])
        else:
            m_index=max_index
            self.errors.append(['EPW-01', self.armmessage.loc[m_index]])
        return m_index

    def whilestatement(self,m_index,tree,max_index):
        m_index += 1
        result = self.find_catch('(', [')'], m_index)
        if (result[2] == True and result[1] < max_index):
            if (m_index != result[1] - 1):
                div = {'name': '判断语句', 'children': []}
                tree.append(div)
                self.single_pression(result[0][1:-1], 0, m_index+1, div['children'])
                m_index = result[1] + 1
                m = self.armmessage.loc[m_index]
                dic={'name': '循环体', 'children': []}
                tree.append(dic)
                m_index = self.is_body(m, m_index, dic['children'],max_index)
            else:
                m_index = result[1] + 1
                self.errors.append(['EPW-0#', self.armmessage.loc[result[1]]])
        else:
            m_index = max_index
            self.errors.append(['EPS-02', self.armmessage.loc[result[1]]])
        return m_index
    def forstatement(self,m_index,tree,max_index):
        result = self.find_catch('(', [')'], m_index)
        if (result[2] == True and result[1]<max_index):
            cut=[]
            for i in range(len(result[0])):
                if(result[0][i]==';'):
                    cut.append(i)
            if(len(cut)==2):
                fs={'name': '单行表达式语句','children':[]}
                f1 = {'name': '定义语句','children':[]}
                f2 = {'name': '判断语句', 'children': []}
                f3 = {'name': '循环语句', 'children': []}
                tree.append(f1)
                tree.append(f2)
                tree.append(f3)
                m=self.armmessage.loc[m_index+1]
                if(m[1]>= 101 and m[1] <= 107):
                    print(1)
                    dict = {'name': '标识符定义', 'children': [{'name': '数值类型', 'children': [{'name': str(m_index+1)}]}]}
                    f1['children'].append(dict)
                    self.define_Identifier(m_index+2,dict['children'],m_index+cut[0]+1)
                else:
                    f1['children'].append(fs)
                    self.single_pression(result[0][1:cut[0]], 0, m_index + 1, fs['children'])
                    if(fs['children'][0]['name']=='空语句'):
                        f1['children']=[{'name': '空语句','children':[]}]
                self.single_pression(result[0][cut[0]+1:cut[1]], 0, m_index + cut[0]+1,f2['children'])
                self.single_pression(result[0][cut[1]+1:-1], 0, m_index + cut[1]+1,f3['children'])
            else:
                self.errors.append(['EPF-01', self.armmessage.loc[m_index]])
            m_index = result[1]
            m_index += 1
            div={'name':'循环体','children':[]}
            tree.append(div)
            m = self.armmessage.loc[m_index]
            m_index = self.is_body(m, m_index,div['children'],max_index)
        else:
            m_index=max_index
            self.errors.append(['EPS-02', self.armmessage.loc[result[1]]])
        return m_index
    def function_body(self,index,result,tree):#大括号内部表达式：
        m_index=index
        m_index += 1
        while(m_index<=result[1]):
            m = self.armmessage.loc[m_index]
            if (m[0] == '}'):
                break
            m_index = self.is_body(m, m_index, tree, result[1])
        print('大括号语句结束')

    def define_Identifier(self,index,tree,max_index):#定义标识符
        result = self.find_catch('$', [';'],index)
        if (result[2] == True and result[1] < max_index):
            new_index=index
            while(new_index<=result[1]):
                b_dict={'name':'定义语句','children':[]}
                tree.append(b_dict)
                result_m = self.find_catch('$', [',',';'], new_index)
                length=result_m[1]-new_index
                if(length>0):
                    if(result_m[0][0]=='标识符'):
                        b_dict['children'].append({'name':str(new_index)})
                        if(length>2):
                            if(result_m[0][1]=='='):
                                dict={'name':'初始语句','children':[]}
                                self.single_pression(result_m[0][2:length],1,new_index+2,dict['children'])
                                b_dict['children'].append(dict)
                            elif(result_m[0][1]=='['):
                                dict = {'name': '数组定义', 'children': []}
                                if(length==4):
                                    if(self.armmessage.loc[new_index+2][1]!=401):
                                        self.errors.append(['EPD-09', self.armmessage.loc[new_index + 2]])
                                    else:
                                        dict['children'].append({'name':str(new_index+2)})
                                else:
                                    self.errors.append(['EPD-08', self.armmessage.loc[new_index]])
                                b_dict['children'].append(dict)
                            else:
                                self.errors.append(['EPD-03', self.armmessage.loc[new_index+1]])
                        elif(length==2):
                            self.errors.append(['EPD-03', self.armmessage.loc[new_index+1]])
                    else:
                        self.errors.append(['EPD-02', self.armmessage.loc[new_index]])
                new_index=result_m[1]+1
        else:
            self.errors.append(['EPS-03', self.armmessage.loc[result[1]]])
        index=result[1]+1
        return index

    def define_function(self,index,tree,max_index):#定义函数
        result = self.find_catch('(', [')'],index)
        index+=1
        if (result[2] == True and result[1]<max_index):
            s_back=self.grammar.analyse('Function',result[0][1:-1],index)
            if (s_back[0]):
                if(len(s_back[1])==1):
                    tree.append({'name': '参数','children':[{'name':'空参数列表'}]})
                else:
                    cv = Create_tree(s_back[1])
                    data = cv.return_tree()
                    tree+=data
            else:
                self.errors.append(['EPD-03',self.armmessage.loc[index+s_back[2]]])
        else:
            self.errors.append(['EPS-02', self.armmessage.loc[result[1]]])
        index=result[1]+1
        m = self.armmessage.loc[index]
        if(m[0]==';'):
            index+=1
            return index
        elif(m[0]=='{'):
            result = self.find_catch('{', ['}'],index)
            if(result[2]== False or result[1]>=max_index ):
                self.errors.append(['EPS-01',self.armmessage.loc[result[1]]])
            else:
                print('进入函数体')
                div={'name':'函数体','children':[]}
                tree.append(div)
                self.function_body(index,result,div['children'])
                print('离开函数体')
            index=result[1]+1
        else:
            self.errors.append(['EPD-04', self.armmessage.loc[result[1]]])
        return index
    def Declaration(self,index,tree):
        begin=index
        m = self.armmessage.loc[index]
        index+=1
        string=['#']
        s = self.armmessage.loc[index]
        i=s[2]
        while(i==m[2] and index<self.lens):
            if(s[1]==407):
                string.append('字符串')
            elif(s[1]==0):
                string.append('标识符')
            elif (int((s[1] / 100)) == 4):
                string.append('数值')
            else:
                string.append(s[0])
            index+=1
            s = self.armmessage.loc[index]
            i=s[2]
        s_back=self.grammar.analyse('Declaration',string,begin)
        if (s_back[0]):
            cv = Create_tree(s_back[1])
            data = cv.return_tree()
            tree += data
        else:
            self.errors.append(['EPD-06', self.armmessage.loc[s_back[2]]])
        return index
    def analyse_main(self,tree):
        self.index=0
        while(self.index<self.lens):
            m=self.armmessage.loc[self.index]
            if(m[0]=='#'):
                self.index=self.Declaration(self.index,tree['children'])
            elif(m[1]>=101 and m[1]<=107):
                self.index+=1
                n = self.armmessage.loc[self.index]
                if(n[1]!=0):
                    self.errors.append(['EPD-01',n])
                else:
                    if(self.armmessage.loc[self.index+1][0]=='('):
                        self.index+=1
                        dicts={'name':'函数','children':[{'name':'返回值类型','children':[{'name':m[0]}]},{'name':'函数名','children':[{'name':str(self.index-1)}]}]}
                        tree['children'].append(dicts)
                        self.index=self.define_function(self.index,dicts['children'],self.lens)
                    else:
                        dicts = {'name': '标识符定义', 'children': [{'name':'数值类型','children':[{'name':str(self.index-1)}]}]}
                        tree['children'].append(dicts)
                        n_index=self.index
                        self.index= self.define_Identifier(self.index,dicts['children'],self.lens)
                        if(self.index-n_index==1):
                            tree.pop()
            elif(m[0]==';'):
                self.index += 1
            else:
                self.errors.append(['EPR-01', self.armmessage.loc[self.index]])
                self.index+=1
        print(self.errors)
        if(len(self.errors)==0):
            tree=(Tree().add("", self.tree).set_global_opts(title_opts=opts.TitleOpts(title="语法树")))
            tree.render(self.path+'/语法树.html')
            pickle.dump(self.tree, open(self.path+'/Parsing.pickle', 'wb'))
    def return_parsing_tree(self):
        return self.tree
    def return_errors(self):
        return self.errors
# armmessage=pandas.read_pickle('work/code6.txt/Lexical.pickle')
# x=Parsing(armmessage,'work/code6.txt/')
#
# x=LL1_parsing()
#
# y=['标识符', '(', '标识符', ',', '数值', ')']
# re=x.analyse('Expresion',y,n)
# # print(len(re[1]))
# # for v in re[1]:
# #     print(v)
# cv=Create_tree(re[1])
# data=cv.return_tree()
# tree=(Tree().add("", data).set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例")))
# tree.render()
# y=['标识符','+','数值']
# y=['标识符','+', '标识符','(','标识符','+', '标识符',',','数值',')']
# re=x.analyse('Expresion', y)
# y=['(','int','标识符',',','char',')']
# re=x.analyse('Function', y)
# for v in re[1]:
#     print(v)
# cv=Create_tree(re[1])
# data=cv.return_tree()



# re=[['A',['B','F']],
#     ['B',['D','C']],
#     ['D',['F','E']],
#     ['F',['G','S','H']],
#     ['H',['b']],
#     ['S',['ε']],
#     ['G',['ε']],
#     ['E',['ε']],
#     ['C',['ε']],
#     ['F',['ε']]]
# # re=[['A',['B','C','F']],
# #     ['B',['a']],
# #     ['C',['b']],
# #     ['F',['c']]]
# cv=Create_tree(re)
# data=cv.return_tree()

# tree=(Tree().add("", data).set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例")))
# tree.render()
# x.analyse('Arithmetic', y)