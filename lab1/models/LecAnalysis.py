import re

from PyQt6.QtCore import QRunnable, QThread
from PyQt6.QtGui import QTextCursor
import json

class LecAnalysis():
    def createTokensCod(self,token_class,token_value):
        if not(token_value in self.tokens[token_class]):
            token_code = str(len(self.tokens[token_class])+1)
            self.tokens[token_class][token_value] = token_class + token_code
    def __init__(self):
        self.OPERATIONS = ['$','.','+','-','*','/','%','**','=','==','!=','>','>=','<','<=','<>','^','&','|','~','<<','>>','!','and','or','xor']
        self.CREATED_FUNC = ['pow','sqrt','sin','cos','tan','abs','log','log10','max','min','array']
        self.SERVICE_WORDS = ['if','else','while','break','continue','function','return','echo','true','false','null','do']
        self.SEPARATORS = [',',';','(',')',' ','\n','\t',"'",'"','<?','?>','{','}','[',']','#']
        self.tokens = {'W':{},'I':{},'O':{},'R':{},'N':{},'C':{}}
    def process(self):
        self.tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}
        for service_word in self.SERVICE_WORDS:
            self.createTokensCod('W',service_word)
        for operation in self.OPERATIONS:
            self.createTokensCod('O',operation)
        for separator in self.SEPARATORS:
                self.createTokensCod('R', separator)
        for operation in self.CREATED_FUNC:
            self.createTokensCod('I',operation)
        f = open('./files/Input.txt','r')
        input_sequence = f.read()
        f.close()


        i=0
        state = 'S'
        output_sequance = buffer = ''
        while i!=len(input_sequence):
            symbol = input_sequence[i]
            if state == 'S':
                buffer=''
                if symbol=='$':
                    state = 'q9'
                    output_sequance+=self.tokens['O']['$']+' '
                elif symbol=='_':
                    state='q26'
                    buffer=symbol
                elif symbol=='?':
                    buffer = symbol
                    state='q28'
                elif symbol.isalpha():
                    state = 'q1'
                    buffer=symbol
                elif symbol.isdigit():
                    buffer=symbol
                    state = 'q3'
                elif symbol=='.':
                    buffer=symbol
                    state = 'q7'
                elif symbol == "'":
                    state = 'q8'
                elif symbol =='"':
                    state='q10'
                elif symbol == '/':
                    state = 'q15'
                    buffer=symbol
                elif symbol == '#':
                    state = 'q19'
                elif i == len(input_sequence) - 1:
                    state = 'Z'
                elif symbol in self.tokens['O'].keys():
                    state = 'q14'
                    buffer=symbol
                elif symbol in self.tokens['R'].keys():
                   state='q20'
                   buffer=symbol
            elif state == 'q9':
                if symbol=='_':
                    state='q26'
                    buffer=symbol
                if symbol.isalpha():
                    state='q1'
                    buffer=buffer+symbol
            elif state == 'q1':
                if symbol.isalpha() or symbol=='_':
                    buffer = buffer + symbol
                    state='q1'
                elif symbol.isdigit():
                    buffer = buffer + symbol
                    state='q2'
                else:
                    if buffer in self.SERVICE_WORDS:
                        output_sequance+=self.tokens['W'][buffer]+ ' '
                    elif buffer in self.OPERATIONS:
                        output_sequance+=self.tokens['O'][buffer]+' '
                    else:
                        self.createTokensCod('I',buffer)
                        output_sequance+=self.tokens['I'][buffer]+' '
                    state='S'
                    i=i-1
            elif state == 'q2':
                if symbol.isalpha() or symbol.isdigit() or symbol=='_':
                    state='q2'
                    buffer = buffer + symbol
                else:
                    if buffer in self.SERVICE_WORDS:
                        output_sequance+=self.tokens['W'][buffer]+ ' '
                    elif buffer in self.OPERATIONS:
                        output_sequance+=self.tokens['O'][buffer]+' '
                    else:
                        self.createTokensCod('I',buffer)
                        output_sequance+=self.tokens['I'][buffer]+' '
                    state='S'
                    i=i-1
            elif state == 'q3':
                if symbol.isdigit():
                    state='q3'
                    buffer = buffer + symbol
                elif symbol=='.':
                    state='q4'
                    buffer = buffer + symbol
                elif symbol=='E' or symbol=='e':
                    state='q5'
                    buffer = buffer + symbol
                else:
                    self.createTokensCod('N', buffer)
                    output_sequance += self.tokens['N'][buffer] + ' '
                    state='S'
                    i=i-1
            elif state == 'q7':
                if symbol.isdigit():
                    state='q4'
                    buffer = buffer + symbol
                else:
                    i=i-1
                    output_sequance +=self.tokens['O']['.']+' '
                    state='S'
            elif state == 'q5':
                if symbol.isdigit() or symbol=='-':
                    state='q6'
                    buffer = buffer + symbol
            elif state == 'q6':
                if symbol.isdigit():
                    state='q6'
                    buffer = buffer + symbol
                else:
                    self.createTokensCod('N',buffer)
                    output_sequance+=self.tokens['N'][buffer]+' '
                    state = 'S'
                    i=i-1
            elif state == 'q4':
                if symbol.isdigit():
                    state='q4'
                    buffer = buffer + symbol
                else:
                    self.createTokensCod('N', buffer)
                    output_sequance += self.tokens['N'][buffer] + ' '
                    state='S'
                    i=i-1
            elif state == 'q8':
                if symbol!="'":
                    state='q8'
                    buffer=buffer+symbol
                else:
                    self.createTokensCod('C',buffer)
                    output_sequance+=self.tokens['C'][buffer]  + ' '
                    state = 'S'
            #НИКАКИХ ОБРАЩЕНИЙ К ЭЛЕМЕНТАМ МАССИВОВ В ЭТИХ СТРОКАХ и никаких множественных $
            elif state == 'q10':
                if symbol !='"' and symbol!="$":
                    state='q10'
                    buffer = buffer + symbol
                elif symbol=='"':
                    self.createTokensCod('C', buffer)
                    output_sequance += self.tokens['C'][buffer] + ' '
                    state = 'S'
                else:
                    self.createTokensCod('C', buffer)
                    output_sequance += self.tokens['C'][buffer] + ' ' + self.tokens['O']['.'] + ' ' + self.tokens['O']['$'] + ' '
                    state = 'q11'
                    buffer = ''
            elif state == 'q11':
                buffer=''
                if symbol.isalpha():
                    state='q12'
                    buffer = buffer + symbol
                elif symbol=='_':
                    state='q27'
                    buffer = buffer + symbol
            elif state == 'q12':
                if symbol.isalpha() or symbol=='_':
                    state='q12'
                    buffer = buffer + symbol
                elif symbol.isdigit():
                    state='q13'
                    buffer = buffer + symbol
                else:
                    if buffer in self.SERVICE_WORDS:
                        output_sequance+=self.tokens['W'][buffer]+ ' '
                    elif buffer in self.OPERATIONS:
                        output_sequance+=self.tokens['O'][buffer]+' '
                    else:
                        self.createTokensCod('I',buffer)
                        output_sequance+=self.tokens['I'][buffer]+ ' ' + self.tokens['O']['.'] + ' '
                    state='q10'
                    buffer=''
                    i=i-1
            elif state == 'q13':
                if symbol.isalpha() or symbol.isdigit() or symbol=='_':
                    state='q13'
                    buffer = buffer + symbol
                else:
                    if buffer in self.SERVICE_WORDS:
                        output_sequance+=self.tokens['W'][buffer]+ ' '
                    elif buffer in self.OPERATIONS:
                        output_sequance+=self.tokens['O'][buffer]+' '
                    else:
                        self.createTokensCod('I',buffer)
                        output_sequance+=self.tokens['I'][buffer]+' ' + self.tokens['O']['.'] + ' '
                    state='q10'
                    buffer = ''
                    i = i - 1
            elif state == 'q14':
                if symbol=='?':
                    buffer=buffer+symbol
                    self.createTokensCod('R',buffer)
                    state='S'
                    output_sequance+=self.tokens['R'][buffer]+ ' '
                elif symbol=='-':
                    state = 'S'
                    self.createTokensCod('O', buffer)
                    output_sequance += self.tokens['O'][buffer] + ' '
                    i=i-1
                elif symbol in [i[1] for i in self.tokens['O'] if len(i)==2]:
                    state='q14'
                    buffer=buffer+symbol
                else:
                    state='S'
                    self.createTokensCod('O', buffer)
                    output_sequance += self.tokens['O'][buffer]+ ' '
                    i=i-1
            elif state == 'q15':
                if symbol=='*':
                    state='q16'
                    buffer=buffer+symbol
                elif symbol=='/':
                    state='q17'
                    buffer=buffer+symbol
                else:
                    state = 'S'
                    self.createTokensCod('O', buffer)
                    output_sequance += self.tokens['O'][buffer] + ' '
                    i=i-1
            elif state == 'q16':
                if symbol=='*':
                    state='q18'
                    buffer=''
                else:
                    state='q16'
                    buffer=''
            elif state == 'q17':
                if i==len(input_sequence)-1:
                    state='Z'
                    buffer=''
                elif symbol=='\n':
                    buffer=''
                    state='S'
                else:
                    buffer=''
                    state='q17'
            elif state == 'q18':
                if symbol!='/':
                    state='q16'
                    buffer=''
                else:
                    state = 'S'
                    buffer=''
                    i=i+1
            elif state == 'q19':
                state='q17'
                buffer=''
            elif state == 'q20':
                self.createTokensCod('R',buffer)
                state='S'
                if buffer =="\t":
                    output_sequance+='\t'
                elif buffer!=' ':
                    output_sequance+=self.tokens['R'][buffer]+' '
                if buffer=='\n':
                    output_sequance += '\n'
                i=i-1
            elif state == 'q26':
                if symbol=='_':
                    state='q26'
                    buffer=buffer+symbol
                else:
                    state='q1'
                    buffer=buffer+symbol
            elif state == 'q27':
                if symbol == '_':
                    state = 'q27'
                    buffer = buffer + symbol
                else:
                    state = 'q12'
                    buffer = buffer + symbol
            elif state=='q28':
                if symbol=='>':
                    buffer=buffer+symbol
                    self.createTokensCod('R', buffer)
                    state = 'Z'
                    output_sequance += self.tokens['R'][buffer]
            elif state=='Z':
                break
            i=i+1
        for token_class in self.tokens.keys():
            with open('./files/%s.json' % token_class, 'w') as write_file:
                data = {val: key for key, val in self.tokens[token_class].items()}
                json.dump(data, write_file, indent=4, ensure_ascii=False)
        return output_sequance,input_sequence

    # self.SERVICE_WORDS = [ 'break', 'continue',

    def get_priority(self,token):
        if token in ['(', 'if', 'while', '[', 'АЭМ', 'Ф', '{']:
            return 0
        if token in [')', ',', ';', 'do', 'else', ']',
                     ]:
            return 1
        if token == '=':
            return 2
        if token == 'or' or token=='xor':
            return 3
        if token == 'and':
            return 4
        if token == '!':
            return 5
        if token in ['<', '<=', '!=','<>', '==', '>', '>=']:
            return 6
        if token in ['^', '&', '|', '~', '<<', '>>']:
            return 7
        if token in ['+', '-', '.']:
            return 8
        if token in ['*', '/', '%']:
            return 9
        if token in ['**']:
            return 10
        if token in ['$']:
            return 11
        if token in ['}','function',
                     'return', 'echo',
                     ]:
            return 12
        return -1


    def reverse_polsk(self):
        CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

        def is_identifier(token):
            return re.match(r'^I\d+$', inverse_tokens[token])
        self.tokens={}
        # файлы, содержащие все таблицы лексем
        for token_class in CLASSES_OF_TOKENS:
            with open('./files/%s.json' % token_class, 'r') as read_file:
                data = json.load(read_file)
                self.tokens.update(data)
        # лексемы (значение-код)
        inverse_tokens = {val: key for key, val in self.tokens.items()}
        # файл, содержащий последовательность кодов лексем входной программы
        f = open('./files/Output.txt', 'r')
        inp_seq = f.read()
        f.close()

        regexp = '[' + '|'.join(CLASSES_OF_TOKENS) + ']' + '\d+'
        match = re.findall(regexp, inp_seq)

        t = [self.tokens[i] for i in match]

        i = 0
        stack = []
        out_seq = ''
        aem_count = 2
        proc_level = operand_count = 1
        tag_count = proc_num = if_count = while_count = do_count= \
            begin_count = end_count = bracket_count = 0
        func_count = 1
        is_if = is_while = is_do = is_description_var = False
        while i < len(t):
            print(stack)
            print(out_seq)
            print(t[i])
            print(do_count)
            p = self.get_priority(t[i])
            if p == -1:
                if t[i]=='<?' and t[i+1]=='php':
                    out_seq +=''
                    i=i+1
                elif t[i]=='?>':
                    out_seq+=''
                elif t[i] != '\n' and t[i] != '\t':
                    out_seq += t[i] + ' '
            else:
                if t[i] == '[':
                    if not re.match(r'^\d+АЭМ$', stack[-1]):
                        aem_count = 2
                    stack.append(str(aem_count) + 'АЭМ')
                elif t[i] == ']':
                    while not (re.match(r'^\d+АЭМ$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if i < len(t) - 1 and t[i+1] == '[':
                        aem_count =  int(stack.pop().split('А')[0]) + 1
                        stack.append(str(aem_count) + 'АЭМ')
                        i=i+1
                    else:
                        out_seq += stack.pop()  + ' '
                        aem_count = 2
                elif t[i] == '(':
                    if is_identifier(t[i - 1]):
                        if t[i + 1] != ')':
                            func_count = 1
                        stack.append(str(func_count) + 'Ф')
                    else:
                        stack.append(t[i])
                    bracket_count += 1
                elif t[i] == ')':
                    while stack[-1] != '(' and not (re.match(r'^\d+Ф$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if re.match(r'^\d+Ф$', stack[-1]):
                        f_c=int(stack[-1].split('Ф')[0])
                        stack.append(str(f_c+1) + 'Ф')
                        out_seq += stack.pop() + ' '
                        while len(stack) > 0 and stack[-1] != "1Ф":
                            stack.pop()
                        stack.pop()
                        stack.append('2')
                        func_count = 1
                    stack.pop()
                    bracket_count -= 1
                    if bracket_count == 0:
                        if is_if:
                            while stack[-1] != 'if':
                                out_seq += stack.pop() + ' '
                            tag_count += 1
                            stack[-1] += ' M' + str(tag_count)
                            out_seq += 'M' + str(tag_count) + ' УПЛ '
                            is_if = False
                        if is_while:
                            while not (re.match(r'^while M\d+$', stack[-1])):
                                out_seq += stack.pop() + ' '
                            tag_count += 1
                            out_seq += 'M' + str(tag_count) + ' УПЛ '
                            stack[-1] += ' M' + str(tag_count)
                            is_while = False
                elif t[i] == ',':
                    while not (re.match(r'^\d+АЭМ$', stack[-1])) and \
                            not (re.match(r'^\d+Ф$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if re.match(r'^\d+АЭМ$', stack[-1]):
                        aem_count += 1
                        stack.append(str(aem_count) + 'АЭМ')
                    if re.match(r'^\d+Ф$', stack[-1]):
                        func_count += 1
                        stack.append(str(func_count) + 'Ф')
                elif t[i] == 'if':
                    stack.append(t[i])
                    if_count += 1
                    bracket_count = 0
                    is_if = True
                elif t[i] == 'else':
                    while not (re.match(r'^if M\d+$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    stack.pop()
                    tag_count += 1
                    stack.append('if M' + str(tag_count))
                    out_seq += 'M' + str(tag_count) + ' БП M' + str(tag_count - 1) + ' : '
                elif t[i] == 'while':
                    if not is_do:
                        tag_count += 1
                        stack.append(t[i] + ' M' + str(tag_count))
                        out_seq += 'M' + str(tag_count) + ' : '
                        while_count += 1
                        is_while = True
                    bracket_count = 0
                elif t[i] == 'do':
                    tag_count += 1
                    stack.append(t[i] + ' M' + str(tag_count))
                    out_seq += 'M' + str(tag_count) + ' : '
                    do_count += 1
                    bracket_count = 0

                elif t[i] == 'function':
                    proc_num += 1
                    stack.append('function ' + str(proc_num) + ' ' + str(proc_level))
                elif t[i] == '{':
                    if len(stack) > 0 and re.match(r'^function', stack[-1]):
                        num = re.findall(r'\d+', stack[-1])
                        stack.pop()
                        out_seq += '0Ф ' + str(num[0]) + ' ' + str(num[1]) + ' НП '
                        stack.append('function ' + str(proc_num) + ' ' + str(proc_level))
                    begin_count += 1
                    proc_level = begin_count - end_count + 1
                    stack.append(t[i])
                elif t[i] == '}':
                    end_count += 1
                    proc_level = begin_count - end_count + 1
                    while stack[-1] != '{':
                        out_seq += stack.pop() + ' '
                    stack.pop()
                    if len(stack) > 0 and re.match(r'^function', stack[-1]):
                        stack.pop()
                        out_seq += 'КП '
                    if if_count > 0 and re.match(r'^if M\d+$', stack[-1]):
                        tag = re.search('M\d+', stack[-1]).group(0)
                        j = i + 1
                        while j < len(t) and t[j] == '\n':
                            j += 1
                        if j >= len(t) or t[j] != 'else':
                            stack.pop()
                            out_seq += tag + ' : '
                            if_count -= 1
                    if do_count > 0 and re.match(r'^do M\d+$', stack[-1]):
                        is_do = True
                    if while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]):
                        tag = re.findall('M\d+', stack[-1])
                        stack.pop()
                        out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                        while_count -= 1
                elif t[i] == ';':
                    if len(stack) > 0 and re.match(r'^function', stack[-1]):
                        num = re.findall(r'\d+', stack[-1])
                        stack.pop()
                        out_seq += str(num[0]) + ' ' + str(num[1]) + ' НП '
                    elif len(stack) > 0 and stack[-1] == 'end':
                        stack.pop()
                        out_seq += 'КП '
                    elif is_description_var:
                        proc_num, proc_level = re.findall('\d+', stack[-1])
                        stack.pop()
                        out_seq += str(operand_count) + ' ' + proc_num + ' ' + proc_level + \
                                   ' КО '
                        is_description_var = False
                    elif if_count > 0 or while_count > 0 or do_count>0:
                        while not (len(stack) > 0 and stack[-1] == '{') and \
                                not (if_count > 0 and re.match(r'^if M\d+$', stack[-1])) and \
                                not (while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]))\
                                and not (do_count > 0 and re.match(r'^do M\d+', stack[-1])):
                            out_seq += stack.pop() + ' '
                        if if_count > 0 and re.match(r'^if M\d+$', stack[-1]):
                            tag = re.search('M\d+', stack[-1]).group(0)
                            j = i + 1
                            while t[j] == '\n':
                                j += 1
                            if t[j] != 'else':
                                stack.pop()
                            out_seq += tag + ' : '
                            if_count -= 1
                        if while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]):
                            tag = re.findall('M\d+', stack[-1])
                            out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                            while_count -= 1
                        if do_count > 0 and re.match(r'^do M\d+', stack[-1]):
                            tag = re.findall('M\d+', stack[-1])
                            stack.pop()
                            tag_count+=1
                            out_seq += 'M'+str(tag_count) + ' УПЛ ' + tag[0] + ' БП ' + 'M'+str(tag_count) +' : '
                            do_count -= 1
                            is_do = False
                    else:
                        while len(stack) > 0 and stack[-1] != '{':
                            out_seq += stack.pop() + ' '
                else:
                    while len(stack) > 0 and self.get_priority(stack[-1]) >= p:
                        out_seq += stack.pop() + ' '
                    stack.append(t[i])
            i += 1

        while len(stack) > 0:
            out_seq += stack.pop() + ' '
        out_seq = re.sub(r'(\d)Ф', r'\1Ф', out_seq)
        out_seq = out_seq.replace(' 0Ф','')
        print(out_seq)
        return ' '.join([inverse_tokens[symbol] if symbol in inverse_tokens.keys() else symbol for symbol in out_seq.split(' ')])
