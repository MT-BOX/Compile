import pandas
import pickle
class Lexical_Analysis:
    def __init__(self,content,path):
        self.index=0
        self.path=path
        self.content=content
        self.Ans = pandas.DataFrame(columns=['Word', 'Species_code', 'row', 'cloumn'], dtype='str')
        self.lens=len(self.content)
        self.Delimiter=['{','}',';',',',':']
        self.Null=['\t','\n',' ','\a','\b']
        self.to_zuh={'a':'\a','t':'\t','b':'\b','o':'\o','n':'\n','r':'\r','v':'\v','f':'\f','\\':'\\','"':'\"','?':'\?'}
        self.ZHUANYI=['a','t','b','o','n','r','v','f','\\','"','?']
        self.Operator=['!','[',']','(',')','*','/','%','+','-','<','>','=','&','|']
        self.row=1
        self.column=1
        self.length=0
        self.species_code=pandas.read_pickle('CSV\Species_code.pickle')
        self.error=[]
    def get_char(self):
        target_str = '\''
        state = 1
        self.add_index()
        while(True):
            ch = self.content[self.index]
            if(state==1):
                if(ch=='\\'):
                    state=3
                    self.add_index()
                elif(ch=='\n'):
                    self.error.append(['ELC-04', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
                else:
                    target_str+=ch
                    state=2
                    self.add_index()
            elif(state==2):
                if(ch=='\''):
                    state=13
                    self.add_index()
                else:
                    self.error.append(['ELC-01', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
            elif (state == 3):
                self.add_index()
                target_str += ch
                if(target_str[1:] in self.ZHUANYI):
                    target_str='\''+self.to_zuh[target_str[1:]]
                if(ch=='x'):
                    state=8
                elif(ch<='7' and ch>='0'):
                    state=4
                else:
                    state=2
            elif (state == 4 or state==5):
                if(ch<='7' and ch>='0'):
                    target_str += ch
                    state+=1
                    self.add_index()
                elif(ch=='\''):
                    state=7
                    self.add_index()
                else:
                    self.error.append(['ELC-02', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
            elif (state == 6):
                if (ch == '\''):
                    state = 7
                    self.add_index()
                else:
                    self.error.append(['ELC-04', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
            elif (state == 7):
                target_str += '\''
                return [target_str, 404514, self.row, self.column]
            elif (state == 8 or state == 9):
                if (ch.isdigit() or (ch <= 'f' and ch >= 'a') or (ch <= 'F' and ch >= 'A')):
                    target_str += ch
                    state += 1
                    self.add_index()
                elif (ch == '\''):
                    state = 7
                    self.add_index()
                else:
                    self.error.append(['ELC-03', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
            elif (state == 10):
                if (ch == '\''):
                    state = 7
                    self.add_index()
                else:
                    self.error.append(['ELC-04', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
            elif (state == 11):
                target_str += '\''
                return [target_str, 404515, self.row, self.column]
            elif (state == 13):
                if(target_str in self.species_code['Translation'].keys()):
                    target_str += '\''
                    return [target_str, 404*1000+self.species_code['Translation'][target_str], self.row, self.column]
                else:
                    target_str += '\''
                    return [target_str, 404, self.row,self.column]
    def get_string(self):
        target_str='\"'
        state=1
        self.add_index()
        while(True):
            if (self.index == self.lens):
                if(state==2):
                    target_str+='\"'
                    return [target_str, 407, self.row, self.column]
                else:
                    self.error.append(['ELS-01', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
            ch=self.content[self.index]
            if(state==1):
                if(ch=='\"'):
                    self.add_index()
                    state=2
                elif(ch=='\\'):
                    target_str+=ch
                    state=3
                    self.add_index()
                elif(ch=='\n'):
                    self.error.append(['ELS-01',self.row,self.column,target_str])
                    return [target_str,0,self.row,self.column]
                else:
                    target_str+=ch
                    self.add_index()
            elif(state==2):
                target_str += '\"'
                return [target_str,407,self.row,self.column]
            elif(state==3):
                if(ch=='\n'):
                    self.error.append(['ELS-01', self.row, self.column,target_str])
                    return [target_str, 0, self.row, self.column]
                else:
                    target_str+=ch
                    state=1
                    self.add_index()
    def get_Identifier(self):#识别标识符
        target_str=''.join(self.content[self.index])
        self.add_index()
        state=1
        while(state!=2 and self.index<self.lens):
            ch=self.content[self.index]
            if(ch.isdigit() or ch.isalpha() or ch=='_'):
                target_str+=ch
                self.index += 1
                self.column += 1
            else:
                state+=1
        sr=0
        if(target_str in self.species_code['key_word'].keys()):
            sr=self.species_code['key_word'][target_str]
        return [target_str,sr,self.row,self.column]
    def add_index(self):
        self.index+=1
        self.column+=1
    def delete_annotation(self):
        target_str='/'
        state=1
        begin_row=self.row
        begin_col=self.column
        self.add_index()
        while(True):
            ch = self.content[self.index]
            if(self.index==(self.lens-1)):
                if(state==1):
                    return [target_str,self.species_code['Operator'][target_str],self.row,self.column]
                elif(state==7 or(state==3 and ch=='/')):
                    return [0,0,0,0]
                else:#多行注释未闭合错误
                    self.error.append(['ELA-01', begin_row, begin_col,target_str])
                    return [0, 0, 0,0]
            if(ch=='\n'):
                self.row+=1
                self.column=0
            if(state==1):
                if(ch=='*'):
                    state=2
                    self.add_index()
                elif(ch=='/'):
                    state=7
                    self.add_index()
                else:
                    return [target_str,self.species_code['Operator'][target_str],self.row,self.column]
            elif(state==2):
                self.add_index()
                if(ch=='*'):
                    state=3
                else:
                    state=2
            elif (state == 3):
                self.add_index()
                if(ch=='/'):
                    return [0,0,0,0]
                elif(ch=='*'):
                   state=3
                else:
                   state=2
            elif (state == 7):
                self.add_index()
                if(ch=='\n'):
                    return [0,0,0,0]
                else:
                    state=7
    def get_Numericalvalue(self):#识别数值
        begin=self.column
        target_str = ''
        state=0
        while(True):
            if (self.index == self.lens):
                if(state==3 or state==11):
                    return [target_str,self.species_code['Word_category']['Integer-10'],self.row,self.column]
                elif(state==5 or state==10):
                    return [target_str,self.species_code['Word_category']['Float'],self.row,self.column]
                elif(state==4):#小数点后未跟数字错误
                    self.error.append(['ELN-02',self.row,self.column,target_str])
                    return [target_str, '',self.row,self.column]

                elif(state==8 or state==9):
                    return [target_str,self.species_code['Word_category']['Float-e'],self.row,self.column]
                elif(state==6):#E后未跟数字错误
                    self.error.append(['ELN-03', self.row, self.column,target_str])
                    return [target_str,'',self.row,self.column]

                elif(state==7):#+-符合后未跟数字错误
                    self.error.append(['ELN-04', self.row, self.column,target_str])
                    return [target_str, '',self.row,self.column]

                elif(state==12 or state==13):
                    return [target_str,self.species_code['Word_category']['Integer-8'],self.row,self.column]
                elif(state==14): #16进制0X后未跟数字错误
                    self.error.append(['ELN-05', self.row, self.column,target_str])
                    return [target_str,'',self.row,self.column]

                elif(state==15 or state==16):
                    return [target_str,self.species_code['Word_category']['Integer-16'],self.row,self.column]
            ch=self.content[self.index]
            if(state==0):
                target_str+=ch
                if(ch=='0'):
                    self.add_index()
                    state = 12
                else:
                    state = 3
                    self.add_index()
            elif (state==3):
                if(ch.isdigit()):
                    target_str+=ch
                    self.add_index()
                elif(ch=='.'):
                    target_str+=ch
                    self.add_index()
                    state=4
                elif(ch=='E' or ch=='e'):
                    target_str+=ch
                    self.add_index()
                    state=6
                elif(ch in self.Delimiter or ch in self.Operator or ch in self.Null):
                    state=11
                else:
                    self.error.append(['ELN-01', self.row, self.column,target_str])
                    return [target_str,'',self.row,self.column]

            elif (state==4):
                if(ch.isdigit()):
                    target_str+=ch
                    self.add_index()
                    state=5
                else:#小数点后未跟数字错误
                    self.error.append(['ELN-02', self.row, self.column,target_str])
                    return [target_str, '', self.row, self.column]
            elif (state == 5):
                if(ch.isdigit()):
                    target_str+=ch
                    self.add_index()
                elif(ch=='E' or ch=='e'):
                    target_str+=ch
                    self.add_index()
                    state=6
                elif (ch in self.Delimiter or ch in self.Operator or ch in self.Null):
                    state=10
                else:# 数字后出现异常字符错误
                    self.error.append(['ELN-01', self.row, self.column,target_str])
                    return [target_str, '', self.row, self.column]
            elif (state == 6):
                if(ch=='+' or ch=='-'):
                    target_str+=ch
                    self.add_index()
                    state=7
                elif(ch.isdigit()):
                    target_str+=ch
                    self.add_index()
                    state=8
                else:#E后出现异常字符错误
                    self.error.append(['ELN-03', self.row, self.column,target_str])
                    return [target_str, '', self.row, self.column]
            elif (state == 7):
                if (ch.isdigit()):
                    target_str += ch
                    self.add_index()
                    state = 8
                else:
                    self.error.append(['ELN-04', self.row, self.column,target_str])
                    return [target_str, '', self.row, self.column]
            elif (state==8):
                if (ch.isdigit()):
                    target_str += ch
                    self.add_index()
                elif (ch in self.Delimiter or ch in self.Operator or ch in self.Null):
                    state = 9
                else:
                    self.error.append(['ELN-01', self.row, self.column,target_str])
                    return [target_str, '', self.row, self.column]
                    pass
            elif (state == 9):
                return [float(target_str),self.species_code['Word_category']['Float-e'],self.row,self.column]
            elif (state==10):
                return [float(target_str),self.species_code['Word_category']['Float'],self.row,self.column]
            elif (state == 11):
                return [int(target_str),self.species_code['Word_category']['Integer-10'],self.row,self.column]
            elif (state == 12):
                if(ch<='7' and ch>='0'):
                    target_str += ch
                    self.add_index()
                elif(ch=='.'):
                    target_str += ch
                    self.add_index()
                    state=4
                elif(ch=='X' or ch=='x'):
                    target_str += ch
                    self.add_index()
                    state=14
                else:
                    state=13
            elif (state == 13):
                if(len(target_str)==1):
                    return [int(target_str),self.species_code['Word_category']['Integer-10'],self.row,self.column]
                return [int(target_str),self.species_code['Word_category']['Integer-8'],self.row,self.column]
            elif (state == 14):
                if(ch.isdigit() or (ch<='f' and ch>='a') or (ch<='F' and ch>='A')):
                    target_str += ch
                    self.add_index()
                    state = 15
                else:
                    self.error.append(['ELN-05', self.row, self.column,target_str])
                    return [target_str, '', self.row, self.column]
            elif (state == 15):
                if (ch.isdigit() or (ch <= 'f' and ch >= 'a') or (ch <= 'F' and ch >= 'A')):
                    target_str += ch
                    self.add_index()
                else:
                    state=16
            elif (state == 16):
                return [int(target_str),self.species_code['Word_category']['Integer-16'],self.row,self.column]

    def main_Analysis(self):
        flag=1
        while(self.index<self.lens):
            ch=self.content[self.index]
            if(ch=='\n'):
                self.row+=1
                self.column=0
            elif(ch=='\t'):
                self.column+=7
            if(ch.isalpha() or ch=='_'):
                result=self.get_Identifier()
            elif(ch.isdigit()):
                result=self.get_Numericalvalue()
            elif(ch=='/'):
                result=self.delete_annotation()
                if(result[0]!='/'):
                    flag=0
            elif(ch=='\"'):
                result = self.get_string()
            elif(ch in self.species_code['Operator'].keys()):
                xt=ch+self.content[self.index+1]
                if(xt in self.species_code['Operator'].keys()):
                    xr=self.species_code['Operator'][xt]
                    self.add_index()
                    result=[xt,xr,self.row,self.column]
                    self.add_index()
                # elif(xt[1] in self.species_code['Operator'].keys() or xt[1]==and '(' not in xt and "[" not in xt and ')' not in xt and ']' not in xt and xt!='=!' and xt!='=~'):
                #     self.error.append(['ELO-01', self.row, self.column, xt])
                #     self.add_index()
                #     flag=0
                else:
                    xr = self.species_code['Operator'][ch]
                    result = [ch, xr, self.row, self.column]
                    self.add_index()
            elif(ch in self.species_code['delimiter'].keys()):
                xr=self.species_code['delimiter'][ch]
                result = [ch, xr, self.row, self.column]
                self.add_index()
            elif(ch =='\''):
                result = self.get_char()
            elif(ch!=' ' and ch !='\n' and ch !='\t'):
                self.error.append(['ELT-01', self.row, self.column, ch])
                self.add_index()
                flag=0
            else:
                flag=0
                self.add_index()
            if(flag==1):
                self.Ans.loc[self.length] = result
                self.length += 1
            flag=1
        print("OK")
        if(len(self.error)==0):
            self.Ans.to_csv(self.path+ "/Lexical.csv", encoding='utf_8_sig',index=False)
            pickle.dump(self.Ans, open(self.path+ '/Lexical.pickle', 'wb'))  # 将字典写进pkl文件
    def get_ans(self):
        return self.Ans
    def get_errors(self):
        return self.error


