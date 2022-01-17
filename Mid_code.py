import pandas
import pickle

class Midcode:
    def __init__(self,armmessage,parsing,target_path):
        self.path=target_path
        self.armmessage=armmessage
        self.parsing=parsing
        self.index=0
        self.relation=['<','>','<=','>=','!=','==']
        self.mid_code = []
        self.Symbol_table=dict()
        self.errors=[]
        self.NXQ=0
        self.code_main()
    def get_leaf(self,tree):
        if('children'  not in tree.keys()):
            return tree['name']
        else:
            return self.get_leaf(tree['children'][0])
    def find_num(self,name,level,type):
        choice = level
        if (name in self.Symbol_table[choice].keys()):
            if (self.Symbol_table[choice][name][1] in type):
                return [True, self.Symbol_table[choice][name]]
        else:
            i=len(level)-1
            while(i>=0):
                if(level[i]=='-'):
                    choice=level[:i]
                    if(name in self.Symbol_table[choice].keys()):
                        if(self.Symbol_table[choice][name][1]  in type):
                            return [True,self.Symbol_table[choice][name]]
                i-=1

        return [False,'']

    def operator_s(self,num1,tree,level,par,fuc):
        code = ['', '', '', '',level]
        oper=''
        num2=[['','','',''],[False,['','','']]]
        for i in range(len(tree['children'])):
            if(i==0):
                oper=self.get_leaf(tree['children'][i])
                if(oper==','and par):
                    self.mid_code.append(['para', num1[0][0], '', '', level])
                    fuc[0] += 1
                    self.NXQ += 1
            elif(i==1):
                result=self.single_sentence(tree['children'][i],level,par,[0])
                num2 = result
                if(result[1][0]==False and result[0][0]!=''):
                    try:
                        if(result[1][1][1]=='函数'):
                            self.errors.append(['EMO-19', result[0][0], result[0][2], result[0][3]])
                        else:
                            self.errors.append(['EMO-05', result[0][0], result[0][2], result[0][3]])
                    except:
                        self.errors.append(['EMO-05', result[0][0], result[0][2], result[0][3]])
                    return num1
                elif (oper==','and par and len(tree['children'][i]['children'])==1):
                    fuc[0]+=1
                    self.mid_code.append(['para', num2[0][0], '', '', level])
                    self.NXQ += 1

        code[0] = oper
        x_type=''
        y_type=''
        if (num1[1][0]):
            x = num1[0][0]
            if (num1[0][1] != 0):
                x_type=str(num1[0][1])[0:3]
                if (x_type == '407'):
                    self.errors.append(['EMO-01',oper,num1[0][2],num1[0][3]])
                x_type=int(x_type)
                if(x_type<=403):
                    x_type='int'
                elif(x_type==404):
                    x_type='char'
                else:
                    x_type='double'
            else:
                x_type=num1[1][1][0]
        else:
            x=num1[0][0]

        if(num2[1][0]):
            y = num2[0][0]
            if (num2[0][1] != 0):
                y_type = str(num2[0][1])[0:3]
                if (y_type == '407'):
                    self.errors.append(['EMO-01',oper,num2[0][2],num2[0][3]])
                y_type = int(y_type)
                if (y_type <= 403):
                    y_type = 'int'
                elif (y_type == 404):
                    y_type = 'char'
                else:
                    y_type = 'double'
            else:
                y_type=num2[1][1][0]
        else:
            y=num2[0][0]
        if (oper == '/'):
            if (num2[0][1] != 0):
                if (num2[0][0] == 0):
                    self.errors.append(['EMO-02',oper,num2[0][2],num2[0][3]])
            else:
                if(float(num2[1][1][2])==0):
                    self.errors.append(['EMO-02', oper, num2[0][2], num2[0][3]])
        if (oper == '%'):
            if (num2[0][1] == 0):
                if (num2[1][1][0] != 'int'):
                    self.errors.append(['EMO-03',oper,num2[0][2],num2[0][3]])
            elif (num2[0][1] > 403):
                self.errors.append(['EMO-03',oper,num2[0][2],num2[0][3]])
            if (num1[0][1] == 0):
                if (num1[1][1][0] != 'int'):
                    self.errors.append(['EMO-03',oper,num1[0][2],num1[0][3]])
            elif (num1[0][1] > 403):
                self.errors.append(['EMO-03',oper,num1[0][2],num1[0][3]])
        if(oper!=','):
            if (oper == '='or oper =='/=' or oper =='*=' or oper =='-='or oper=='+=' or oper =='&=' or oper =='|='):
                if(num1[1][1][1]=='变量' or num1[1][1][1]=='变量-数组'):
                    code[1] = y
                    code[3] = x
                else:
                    self.errors.append(['EMO-04',y,num2[0][2],num2[0][3]])
            elif(oper in self.relation):
                code=[oper,x,y,'@' + str(self.index),level]
                num1 = [['@' + str(self.index), 401, 0, 0], [True,['int', '变量', '']]]
                self.index += 1
            elif(oper =='&&' or oper=='||'):
                code = [oper[0], x,y, '@' + str(self.index),level]
                num1 = [['@' + str(self.index), 401, 0, 0], [True,['int', '变量', '']]]
                self.index+=1
            elif(oper=='++' or oper =='--'):
                if(x==''):
                    code = [oper, y, '', '@' + str(self.index), level]
                    num1=num2
                else:
                    code = [oper, x, '', '@' + str(self.index), level]
            else:
                # print(x_type+'->'+y_type)
                if(x_type=='double' or y_type=='double'):
                    x_type='double'
                elif(x_type=='int' or y_type=='int'):
                    x_type='int'
                # else:
                code[1] = x
                code[2] = y
                code[3] = '@' + str(self.index)
                num1 = [['@' + str(self.index), 401,num2[0][2], num2[0][3]], [True,[x_type, '变量', '']]]
                self.index += 1
            self.mid_code.append(code)
            self.NXQ+=1
        if(len(tree['children'])==3):
            num1 = self.operator_s(num1, tree['children'][2], level, par,fuc)
        return num1
    def single_sentence(self,tree,level,par,fuc):
        if('children' not in tree.keys()):
            # print('->',tree['name'])
            num= self.armmessage.loc[int(tree['name'])]
            result=[True,['','','']]
            if (num[1] == 0):
                result = self.find_num(num[0], level, ['变量','常量','变量-数组'])
            return [[num[0],num[1],num[2],num[3]],result]
        num1=[['','','',''],[False,['','','']]]
        if(tree['children'][0]['name']!='('):
            if(len(tree['children'])>1):
                if(tree['name']=='IDER'):
                    num1 = self.operator_s(num1, tree, level,par,fuc)
                    return num1
                if(tree['name']=='XR'):
                    num1=self.single_sentence(tree['children'][0],level,par,fuc)
                    nade=tree['children'][1]['children'][0]
                    if(nade['name']=='后缀运算符'):
                        oper=self.get_leaf(nade)
                        if (num1[1][0]):
                            x = num1[0][0]
                            if (num1[0][1] != 0):
                                x_type = str(num1[0][1])[0:3]
                                if (x_type == '407'):
                                    self.errors.append(['EMO-01', oper, num1[0][2], num1[0][3]])
                                else:
                                    self.mid_code.append([oper,x,'','@' + str(self.index),level])
                                    self.index+=1
                                    self.NXQ+=1
                            else:
                                self.mid_code.append([oper, x, '', '@' + str(self.index), level])
                                self.index += 1
                                self.NXQ += 1
                        else:
                            self.errors.append(['EMO-05', num1[0][0], num1[0][2], num1[0][3]])
                        return num1
                    elif(nade['name']=='函数式'):
                        function_name=num1[0][0]
                        if(function_name in self.Symbol_table['0'].keys()):
                            if(self.Symbol_table['0'][function_name][1]=='函数'):
                                self.mid_code.append(['call', num1[0][0], '', '', level])
                                self.index += 1
                                self.NXQ += 1
                                fus = [0]
                                if(nade['children'][1]['name']!=')'):
                                    num=self.single_sentence(nade['children'][1],level,True,fus)
                                    if (str(num[0][0])[0]!='@' and self.mid_code[self.NXQ-1][0]=='call'):
                                        if(num[1][0]):
                                            self.mid_code.append(['para', num[0][0], '', '', level])
                                            fus[0]+=1
                                            self.NXQ += 1
                                        else:
                                            self.errors.append(['EMO-05', num[0][0], num[0][2], num[0][3]])
                                    elif(fus[0]==0):
                                        self.mid_code.append(['para', num[0][0], '', '', level])
                                        fus[0] += 1
                                        self.NXQ += 1
                                self.mid_code.append(['go', num1[0][0], '', '', level])
                                self.NXQ += 1
                                if(fus[0]!=self.Symbol_table['0'][function_name][2]):
                                    self.errors.append(['EMO-20', num1[0][0], num1[0][2], num1[0][3]])
                                if(self.Symbol_table['0'][function_name][0]!='void'):
                                    self.mid_code.append(['ret', '@rt', '', '', level])
                                    self.NXQ += 1
                                    num1[1][0] = True
                                    num1[0][0] = '@rt'
                                else:
                                    num1[1][0] = False
                                    self.mid_code.append(['ret', '', '', '', level])
                                    self.NXQ += 1
                                num1[1][1]=self.Symbol_table['0'][function_name]
                            else:
                                self.errors.append(['EMO-17', num1[0][0], num1[0][2], num1[0][3]])
                        else:
                            self.errors.append(['EMO-16', num1[0][0], num1[0][2], num1[0][3]])
                        return num1
                    elif(nade['name']=='数组定义'):
                        index_o=self.single_sentence(nade['children'][1],level,par,fuc)
                        print(index_o)
                        num1[0][0]=num1[0][0]+'~'+str(index_o[0][0])
                        if(index_o[0][1]!=0 and str(index_o[1][1][2])!='' and str(index_o[1][1][2])[0]!='@'):
                            if(int(index_o[0][0])>=len(num1[1][1][2])  or int(index_o[0][0])<0):
                                self.errors.append(['EMO-18', index_o[0][0], index_o[0][2], index_o[0][3]])
                        elif(str(index_o[1][1][2])!='' and str(index_o[1][1][2])[0]!='@' ):
                            if (int(index_o[1][1][2]) >= len(num1[1][1][2]) or int(index_o[1][1][2]) < 0):
                                self.errors.append(['EMO-18', index_o[0][0], index_o[0][2], index_o[0][3]])
                        return num1
                    else:
                        num1 = [['', '', '', ''], [False, ['', '', '']]]
                        num1 = self.operator_s(num1, tree, level,fuc)
                else:
                    num1 = self.single_sentence(tree['children'][0], level,par,fuc)
                    num1 = self.operator_s(num1, tree['children'][1], level,par,fuc)
                    return num1
            else:
                num1 = self.single_sentence(tree['children'][0],level,par,fuc)
            return num1
        else:
            return self.single_sentence(tree['children'][1],level,par,fuc)
    def if_else(self,tree,level,jump_NXQ):
        else_nxq=self.NXQ
        end_nxq=-1
        for x in tree:
            if(x['name']=='判断语句'):
                result=self.single_sentence(x['children'][0],level,False,[0])
                if (result[0][1] != 0):
                    y_type = str(result[0][1])[0:3]
                    if (y_type == '407'):
                        self.errors.append(['EMO-01', result[0][0], result[0][2], result[0][3]])
                code = ['jnz', result[0][0], '', self.NXQ + 2, level]  # 为真的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
                else_nxq = self.NXQ
                code = ['j', '', '', '', level]  # 为假的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
            elif(x['name']=='是语句块'):
                self.function_body(x['children'],level,[],jump_NXQ)
            elif(x['name']=='非语句块'):
                end_nxq=self.NXQ
                code = ['j', '', '', '', level]  # 为假的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
                self.mid_code[else_nxq][3]=self.NXQ
                self.function_body(x['children'], level, [], jump_NXQ)
        if(end_nxq!=-1):
            self.mid_code[end_nxq][3]=self.NXQ
            self.mid_code[else_nxq][3] = end_nxq+1
        else:
            self.mid_code[else_nxq][3] = self.NXQ

    def while_state(self,tree,level):
        jump_NXQ = [True, [], []]
        begin_nxq=self.NXQ
        while_nxq = self.NXQ
        p_nxq = self.NXQ
        end_nxq = self.NXQ
        for x in tree:
            if(x['name']=='判断语句'):
                p_nxq=self.NXQ
                result = self.single_sentence(x['children'][0], level,False,[0])
                if (result[0][1] != 0):
                    y_type = str(result[0][1])[0:3]
                    if (y_type == '407'):
                        self.errors.append(['EMO-01', result[0][0], result[0][2], result[0][3]])
                code = ['jnz', result[0][0], '', self.NXQ + 2, level]  # 为真的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
                while_nxq = self.NXQ
                code = ['j', '', '', '', level]  # 为假的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
            elif(x['name']=='循环体'):
                self.function_body(x['children'], level, [], jump_NXQ)
                code = ['j', '', '', begin_nxq, level]  # 为假的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
                self.mid_code[while_nxq][3]=self.NXQ
                end_nxq=self.NXQ
        for i in jump_NXQ[1]:
            self.mid_code[i][3]=end_nxq
        for i in jump_NXQ[2]:
            self.mid_code[i][3] = p_nxq
    def do_while(self,tree,level):
        jump_NXQ = [True, [], []]
        begin_nxq = self.NXQ
        p_nxq=self.NXQ
        end_nxq=self.NXQ
        for x in tree:
            if (x['name'] == '循环体'):
                self.function_body(x['children'], level, [], jump_NXQ)
            elif (x['name'] == '判断语句'):
                p_nxq=self.NXQ
                result = self.single_sentence(x['children'][0], level,[0])
                if (result[0][1] != 0):
                    y_type = str(result[0][1])[0:3]
                    if (y_type == '407'):
                        self.errors.append(['EMO-01', result[0][0], result[0][2], result[0][3]])
                code = ['jnz', result[0][0], '', begin_nxq, level]  # 为真的跳转语句
                self.mid_code.append(code)
                self.NXQ += 1
                end_nxq=self.NXQ
        for i in jump_NXQ[1]:
            self.mid_code[i][3]=end_nxq
        for i in jump_NXQ[2]:
            self.mid_code[i][3] = p_nxq
    def for_state(self,tree,level):
        do_nxq=self.NXQ
        if_nxq=self.NXQ
        p_nxq=self.NXQ
        end_nxq=self.NXQ
        jump_NXQ=[True,[],[]]
        if_el=True
        for x in tree:
            if(x['name'] == '定义语句'):
                self.function_body(x['children'], level, [], jump_NXQ)
            elif (x['name'] == '判断语句'):
                p_nxq=self.NXQ
                if(x['children'][0]['name']!='空语句'):
                    result = self.single_sentence(x['children'][0], level,False,[0])
                    if (result[0][1] != 0):
                        y_type = str(result[0][1])[0:3]
                        if (y_type == '407'):
                            self.errors.append(['EMO-01', result[0][0], result[0][2], result[0][3]])
                    if_nxq=self.NXQ
                    code = ['jnz', result[0][0], '', '', level]  # 为真的跳转语句
                    self.mid_code.append(code)
                    self.NXQ += 1
                    code = ['j', '', '', '', level]  # 为假的跳转语句
                    self.mid_code.append(code)
                    self.NXQ += 1
                else:
                    if_el=False
                    if_nxq=self.NXQ
                    code = ['j', '', '', '', level]
                    self.mid_code.append(code)
                    self.NXQ += 1
            elif(x['name'] == '循环语句'):
                if (x['children'][0]['name'] != '空语句'):
                    do_nxq = self.NXQ
                    self.single_sentence(x['children'][0], level,False,[0])
                    self.mid_code.append(['j', '', '', p_nxq, level])
                    self.NXQ += 1
                else:
                    do_nxq=p_nxq
            elif (x['name'] == '循环体'):
                self.mid_code[if_nxq][3] = self.NXQ
                self.function_body(x['children'], level, [], jump_NXQ)
                code = ['j', '', '', do_nxq, level]
                self.mid_code.append(code)
                self.NXQ += 1
                if(if_el):
                    self.mid_code[if_nxq+1][3] = self.NXQ
                end_nxq=self.NXQ
        for i in jump_NXQ[1]:
            self.mid_code[i][3]=end_nxq
        for i in jump_NXQ[2]:
            self.mid_code[i][3] = p_nxq

    def return_stae(self,tree,level):
        result=self.armmessage.loc[int(tree[0]['name'])]
        if(self.return_type=='void'):
            self.errors.append(['EMO-14', result[0], result[2], result[3]])
        else:
            if_flag=True
            for x in tree:
                if(x['name']=='表达式'):
                    r_type=''
                    if_flag=False
                    result = self.single_sentence(x['children'][0], level,False,[0])
                    if(result[0][1]!=0):
                        if result[0][1]>=401 and result[0][1]<=403:
                            r_type='int'
                        elif result[0][1]==404:
                            r_type='char'
                        elif result[0][1]==405:
                            r_type = 'float'
                        elif result[0][1]==406:
                            r_type = 'double'
                        else: r_type='string'
                    else:
                        r_type=result[1][1][0]
                    if(r_type!=self.return_type):
                        self.errors.append(['EMO-15', result[0][0], result[0][2], result[0][3]])

                    self.mid_code.append(['ret', '', '', result[0][0], level])
                    self.NXQ+=1
            if(if_flag):
                self.mid_code.append(['ret', '', '', '', level])
                self.NXQ+=1
    def function_body(self,tree,level,parameter,jump_NXQ):
        for x in parameter:
            if(x[1]!=''):
                self.Symbol_table[level][x[1]]=[x[0],'变量','']
        deep=0
        for x in tree:
            if(x['name']=='单行表达式语句'):
                if(x['children'][0]['name']!='空语句'):
                  self.single_sentence(x['children'][0],level,False,[0])
                  deep-=1
            elif(x['name']=='大括号语句'):
                self.Symbol_table[level+'-'+str(deep)] = {}
                self.function_body(x['children'],level+'-'+str(deep),[],jump_NXQ)
            elif (x['name'] == '标识符定义'):
                self.Id_denfine(x, level)
                deep -= 1
            elif(x['name'] == 'if判断语句'):
                self.Symbol_table[level + '-' + str(deep)] = {}
                self.if_else(x['children'],level+'-'+str(deep),jump_NXQ)
            elif(x['name']=='For循环语句'):
                self.Symbol_table[level + '-' + str(deep)] = {}
                self.for_state(x['children'],level+'-'+str(deep))
            elif(x['name']=='do循环语句'):
                self.Symbol_table[level + '-' + str(deep)] = {}
                self.do_while(x['children'],level+'-'+str(deep))
            elif(x['name']=='while循环语句'):
                self.Symbol_table[level + '-' + str(deep)] = {}
                self.while_state(x['children'],level+'-'+str(deep))
            elif(x['name']=='返回值语句'):
                self.return_stae(x['children'],level)
                deep -= 1
            elif(x['name']=='跳转语句'):
                result = self.armmessage.loc[int(x['children'][0]['name'])]
                deep -= 1
                if(jump_NXQ[0]):
                    if(result[0]=='break'):
                        jump_NXQ[1].append(self.NXQ)
                    else:
                        jump_NXQ[2].append(self.NXQ)
                    self.mid_code.append(['j','','','',level])
                    self.NXQ+=1
                else:
                    self.errors.append(['EMO-12', result[0], result[2], result[3]])
            deep+=1


    def get_parameter(self,tree,parameter):
        if('children' not in tree.keys()):
            return
        elif(tree['name']=='B'):
            ps=['','']
            for i in range(len(tree['children'])):
                if(i==0):
                    ps[i]=self.get_leaf(tree['children'][i])
                else:
                    ps[i]=self.armmessage.loc[int(self.get_leaf(tree['children'][i]))][0]
            parameter.append(ps)
        else:
            for x in tree['children']:
                self.get_parameter(x,parameter)
    def function(self,tree,level,jc):#函数定义
        fuction=['','函数','',[],-1]
        name=''
        parameter=[]
        for x in tree['children']:
            if(x['name']=='函数体'):
                fuction[4]=self.NXQ
                self.mid_code.append([name[0],'','','',level+'-'+str(jc)])
                self.NXQ+=1
                self.Symbol_table[level + '-' + str(jc)] = {}
                self.function_body(x['children'],level+'-'+str(jc),parameter,[False])
                self.mid_code.append(['ret', '', '', '',level+'-'+str(jc)])
                self.NXQ += 1
                if(name[0]=='main'):
                    self.mid_code.append(['sys', '', '', '',level])
                    self.NXQ+=1
            elif(x['name']=='返回值类型'):
                fuction[0]=self.get_leaf(x)
                self.return_type=fuction[0]
            elif(x['name']=='函数名'):
                name=self.armmessage.loc[int(self.get_leaf(x))]
            elif(x['name']=='参数'):
                self.get_parameter(x,parameter)
                fuction[3]=parameter
                fuction[2]=len(parameter)
        flag=True
        for x in self.Symbol_table.values():#查看是否有重名变量
            for y in x.keys():
                if(x[y][1]!='函数' and y==name[0]):
                    flag=False
                    break
        if(flag):
            if(name[0] in self.Symbol_table[level].keys()):
                node=self.Symbol_table[level][name[0]]
                if(node[4]==-1):
                    if(fuction[4]==-1):
                        self.Symbol_table[level][name[0]]=fuction
                    else:
                        if(node[2]==fuction[2]):
                            flag=True
                            for i in range(node[2]):
                                if(node[3][i][0]!=fuction[3][i][0]):
                                    flag=False
                                    break
                            if(flag):
                                self.Symbol_table[level][name[0]] = fuction
                            else:
                                self.errors.append(['EMO-06',name[0],name[2],name[3]])
                        else:
                            self.errors.append(['EMO-06',name[0],name[2],name[3]])
                else:
                    self.errors.append(['EMO-07',name[0],name[2],name[3]])
            else:
                self.Symbol_table[level][name[0]]=fuction
        else:
            self.errors.append(['EMO-08', name[0], name[2], name[3]])
    def Id_denfine(self,tree,level):#标识符定义
        id_type=self.armmessage.loc[int(self.get_leaf(tree['children'][0]))]
        if(id_type[0]!='void'):
            for i in range(1,len(tree['children'])):
                x=tree['children'][i]
                m=[]
                for xd in x['children']:
                    if('children' not in xd.keys()):
                        m=self.armmessage.loc[int(xd['name'])]
                        if(m[0] not in self.Symbol_table['0'] or self.Symbol_table['0'][m[0]][1]!='函数'):
                             if(m[0] not in self.Symbol_table[level]):
                                self.Symbol_table[level][m[0]] = [id_type[0],'变量','']
                             else:
                                self.errors.append(['EMO-10', m[0], m[2], m[3]])
                        else:
                            self.errors.append(['EMO-11', m[0], m[2], m[3]])
                            break
                    elif(xd['name']=='数组定义'):
                        s=self.armmessage.loc[int(xd['children'][0]['name'])]
                        gh=[]
                        for i in range(int(s[0])):
                            gh.append('')
                        self.Symbol_table[level][m[0]] = [id_type[0], '变量-数组',gh]
                    else:
                        self.index=0
                        num=self.single_sentence(xd, level,False,[0])
                        self.mid_code.append(['=',num[0][0],'',m[0],level])
                        if(num[0][1]!=0):
                            self.Symbol_table[level][m[0]][2]=num[0][0]
                        self.NXQ+=1
        else:
            self.errors.append(['EMO-09',id_type[0],id_type[2],id_type[3]])

    def const_define(self,tree,level):#常量定义
        if(tree['name']=='导入库文件'):
            pass
        else:
            x=int(self.get_leaf(tree['children'][1]))
            y=int(self.get_leaf(tree['children'][2]))
            m1=self.armmessage.loc[x]
            m2=self.armmessage.loc[y]
            if(m1[0] not in self.Symbol_table[level].keys()):
                self.Symbol_table[level][m1[0]]=[m2[0],'常量',m2[1]]

    def code_main(self):
        level='0'
        jc=0
        self.Symbol_table[level] = {}
        self.Symbol_table[level]['read']=['char','函数',0,[],0]
        self.Symbol_table[level]['write'] = ['void', '函数',1, [['string','']], 0]
        for x in self.parsing[0]['children']:
            if(x['name']=='函数'):
                self.function(x,level,jc)
                jc+=1
            elif(x['name']=='标识符定义'):
                self.Id_denfine(x,level)
            else:
                self.const_define(x['children'][1]['children'][0],level)
        m=self.armmessage.loc[len(self.armmessage)-1]
        if('main' not in self.Symbol_table['0']):
            self.errors.append(['EMO-21', '', m[2], m[3]])
        for i in range(len(self.mid_code)):
            print(i,':',self.mid_code[i])
        # print(self.Symbol_table)
        # for x in self.errors:
        #     print(x)
        if(len(self.errors)==0):
            pickle.dump(self.mid_code, open(self.path + '/Mid_code.pickle', 'wb'))
            pickle.dump(self.Symbol_table, open(self.path + '/Symbol_table.pickle', 'wb'))
    def return_results(self):
        return [self.mid_code,self.Symbol_table,self.errors]

# ar=pandas.read_pickle('work/code.txt/Lexical.pickle')
# gr=pandas.read_pickle('work/code.txt/Parsing.pickle')
# x=Midcode(ar,gr,'work/code.txt')
# print(x.Symbol_table)