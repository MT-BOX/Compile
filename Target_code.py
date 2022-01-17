import pandas
class Targrt_code:
    def __init__(self, mid_code,symbol_table,path):
        self.mid_code=mid_code
        self.symbol_table=symbol_table
        self.path=path
    def target_code(self):
        fun_name = '**'
        f = open('./Target/data_segment.txt', 'r')
        s = f.read()
        # for i in global_main_symbol:
        #     s += '\t_' + i + ' dw 0\n'
        f.close()
        f = open('./Target/code_segment1.txt', 'r')
        s1 = f.read()
        s += s1
        f = open('./Target/code_segment2.txt', 'r')
        rear = f.read()
        f.close()
        fun_name = '**'
        for i in range(len(self.mid_code)):
            one = self.mid_code[i][0]
            if one == 'main' or one == 'OP':
                continue
            two = str(self.mid_code[i][1])
            three = str(self.mid_code[i][2])
            four = str(self.mid_code[i][3])
            # if one not in ['j']:
            #     if two != '_' and two in global_main_symbol:
            #         two = 'ds:[_' + two + ']'
            #     elif two[0] == '$':
            #         two = 'es:[' + str(int(two[5:]) * 2) + ']'
            #     elif fun_name != '**' and two in function[fun_name][0]:
            #         two = function[fun_name][0][two]
            #     elif fun_name != '**' and two in function[fun_name][1]:
            #         two = function[fun_name][1][two]
            #     if three != '_' and three in global_main_symbol:
            #         three = 'ds:[_' + three + ']'
            #     elif three[0] == '$':
            #         three = 'es:[' + str(int(three[5:]) * 2) + ']'
            #     elif fun_name != '**' and three in function[fun_name][0]:
            #         three = function[fun_name][0][three]
            #     elif fun_name != '**' and three in function[fun_name][1]:
            #         three = function[fun_name][1][three]
            #     if four != '_' and four in global_main_symbol:
            #         four = 'ds:[_' + four + ']'
            #     elif four[0] == '$':
            #         four = 'es:[' + str(int(four[5:]) * 2) + ']'
            #     elif fun_name != '**' and four in function[fun_name][0]:
            #         four = function[fun_name][0][four]
            #     elif fun_name != '**' and four in function[fun_name][1]:
            #         four = function[fun_name][1][four]
            if one == '=':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'MOV ' + four + ',AX\n'
            elif one == '+':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'ADD AX,' + three + '\n\t' + 'MOV ' + four + ',AX\n'
            elif one == '-':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'SUB AX,' + three + '\n\t' + 'MOV ' + four + ',AX\n'
            elif one == '*':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'MOV BX,' + three + '\n\t' + 'MUL BX\n\t' + 'MOV ' + four + ',AX\n'
            elif one == '/':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'MOV DX,0\n\t' + 'MOV AX,' + three + '\n\t' + 'DIV BX\n\t' + 'MOV ' + four + ',AX\n'
            elif one == '%':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'MOV DX,0\n\t' + 'MOV BX,' + three + '\n\t' + 'DIV BX\n\t' + 'MOV ' + four + ',DX\n'
            elif one == '<':
                s += '_%d:\t' % (i - 1) + 'MOV DX,1\n\t''MOV AX,' + two + '\n\t' + 'CMP AX,' + three + '\n\t' + 'JB _LT_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_LT' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '>=':
                s += '_%d:\t' % (
                            i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,' + three + '\n\t' + 'JNB _GE_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_GE_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '>':
                s += '_%d:\t' % (
                            i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,' + three + '\n\t' + 'JA _GT_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_GT_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '<=':
                s += '_%d:\t' % (
                            i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,' + three + '\n\t' + 'JNA _LE_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_LE_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '==':
                s += '_%d:\t' % (
                            i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,' + three + '\n\t' + 'JE _EQ_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_EQ_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '!=':
                s += '_%d:\t' % (
                            i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,' + three + '\n\t' + 'JN _NE_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_NE_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '&&':
                s += '_%d:\t' % (i - 1) + 'MOV DX,0\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JE _AND_' + str(
                    i - 1) + '\n\t' + 'MOV AX,' + three + '\n\t' + 'CMP AX,0\n\t' + 'JE _AND_' + str(
                    i - 1) + '\n\t' + 'MOV DX,1\n' + '_AND_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '||':
                s += '_%d:\t' % (i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JNE _OR_' + str(
                    i - 1) + '\n\t' + 'MOV AX,' + three + '\n\t' + 'CMP AX,0\n\t' + 'JNE _OR_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_OR_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == '!':
                s += '_%d:\t' % (i - 1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JE _NOT_' + str(
                    i - 1) + '\n\t' + 'MOV DX,0\n' + '_NOT_' + str(i - 1) + ':\tMOV ' + four + ',DX\n'
            elif one == 'j':
                gg = '_' + str(int(four) - 1)
                if self.mid_code[int(four)][0] == 'sys':
                    gg = 'quit'
                s += '_%d:\t' % (i - 1) + 'JMP far ptr ' + gg + '\n'
            elif one == 'jz':
                gg = '_' + str(int(four) - 1)
                if self.mid_code[int(four)][0] == 'sys':
                    gg = 'quit'
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JNE _NE_' + str(i - 1) + '\n\t' + 'JMP far ptr ' + gg + '\n' + '_NE_' + str(i - 1) + ':\tNOP\n'
            elif one == 'jnz':
                gg = '_' + str(int(four) - 1)
                if self.mid_code[int(four)][0] == 'sys':
                    gg = 'quit'
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JE _EZ_' + str(
                    i - 1) + '\n\t' + 'JMP far ptr ' + gg + '\n' + '_EZ_' + str(i - 1) + ':\tNOP\n'
            elif one == 'para':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'PUSH AX\n'
            elif one == 'call':
                s += '_%d:\t' % (i - 1) + 'CALL ' + two + '\n'
                if four != '_':
                    s += '\tMOV ' + four + ',AX\n'
            elif one == 'ret' and two != '_':
                s += '_%d:\t' % (i - 1) + 'MOV AX,' + two + '\n\t' + 'MOV SP,BP\n\t' + 'POP BP\n\t' + 'RET '
                # if four != '_':
                #     s += str(len(function[fun_name][0]) * 2)  # ret 后的数字是参数个数*2  即参数区的大小 返回原来地址
                s += '\n'
                fun_name = '**'
            elif one == 'ret':
                s += '_%d:\t' % (i - 1) + 'MOV SP,BP\n\t' + 'POP PB\n\t' + 'RET\n'
                fun_name = '**'
            elif one == 'sys':
                s += 'quit:\t' + 'mov ah,4ch\n\t' + 'int 21h\n'
            else:
                pass
                # fun_name = one
                # s += one + ':\t' + 'PUSH BP\n\t' + 'MOV BP,SP\n\t' + 'SUB SP,' + str(
                #     len(function[fun_name][1]) * 2) + '\n'
        f = open(self.path+'/Target_code.txt', 'w')
        f.write(s+rear)
        f.close()
        return s+rear

