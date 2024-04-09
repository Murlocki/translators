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

    #Лаба 1
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
        f = open('files/Input.txt','r')
        input_sequence = f.read()
        f.close()


        i=0
        state = 'S'
        output_sequance = buffer = ''

        add_return_counter=0
        bracers_func_stack=[]
        func_buff=''
        while i!=len(input_sequence):
            symbol = input_sequence[i]
            if (buffer == 'function' and func_buff!='function'):
                add_return_counter += 1
                func_buff='function'
            elif (add_return_counter > 0 and buffer == 'return'):
                add_return_counter -= 1
            elif (symbol == '{'):
                bracers_func_stack.append('{')
            elif (symbol == '}'):
                bracers_func_stack.pop()
                if (add_return_counter > 0 and not bracers_func_stack):
                    add_return_counter -= 1
                    self.createTokensCod('C','')
                    output_sequance += self.tokens['W']['return'] + ' '+ self.tokens['C']['']+ self.tokens['R'][';']
            if(buffer!='function'):
                func_buff=''
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
                elif symbol in self.tokens['R']:
                    state='S'
                    output_sequance+=' '+self.tokens['R'][symbol]
                    buffer=''
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

    #Лаба 2
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
        is_if = is_while = is_do = is_description_var =False
        is_return = []


        self.if_marks=[]
        self.else_marks=[]
        self.end_marks=[]

        self.while_start_marks=[]
        self.while_end_marks=[]

        self.do_start_marks=[]
        self.do_end_marks=[]
        while i < len(t):
            # print(out_seq)
            # print(stack)
            # print(t[i])
            # print('------')
            # print(self.if_marks)
            # print(self.else_marks)
            # print(self.while_start_marks)
            # print(self.while_end_marks)
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
                        if(t[i-1]!='('):
                            stack.append(str(f_c+1) + 'Ф')
                        else:

                            stack.append(str(f_c) + 'Ф')
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
                            self.else_marks.append('M' + str(tag_count))
                            self.end_marks.append('M' + str(tag_count))
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
                    self.if_marks.append('M' + str(tag_count))
                    self.end_marks.pop()
                elif t[i] == 'while':
                    if not is_do:
                        tag_count += 1
                        stack.append(t[i] + ' M' + str(tag_count))
                        out_seq += 'M' + str(tag_count) + ' : '
                        self.while_start_marks.append('M' + str(tag_count))
                        while_count += 1
                        is_while = True
                    bracket_count = 0
                elif t[i] == 'do':
                    tag_count += 1
                    stack.append(t[i] + ' M' + str(tag_count))
                    out_seq += 'M' + str(tag_count) + ' : '
                    self.do_start_marks.append('M' + str(tag_count))
                    do_count += 1
                    bracket_count = 0
                elif t[i] == 'function':
                    proc_num += 1
                    stack.append('function ' + str(proc_num) + ' ' + str(proc_level))
                elif t[i]=='return':
                   is_return.append('true')
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
                        if is_return:
                            out_seq += 'return КП '
                            is_return.pop()
                        else:
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
                        self.while_end_marks.append(tag[1])
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


    #Лаба 3
    def translate_to_R(self):
        CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']
        self.tokens = {}
        # файлы, содержащие все таблицы лексем
        for token_class in CLASSES_OF_TOKENS:
            with open('./files/%s.json' % token_class, 'r') as read_file:
                data = json.load(read_file)
                self.tokens.update(data)
                if token_class == 'C':
                    for k in data.keys():
                        data[k] = re.sub(r"'([^']*)'", r'"\1"', data[k])
                self.tokens.update(data)
        # лексемы (значение-код)
        inverse_tokens = {val: key for key, val in self.tokens.items()}
        replace = {'echo': 'print', '=': '<-', '!=': '!=',
                   '==': '==', '/': '/', '%': '%%','>':'>','>=':'>=','<':'<','<=':'<=',
                   '$':'','.':'paste(','+':'+','-':'-','*':'*','**':'**',
                    '^':'bitwXor(','&':'bitwAnd(','|':'bitwOr(','~':'bitwNot(','<<':'bitwShiftL(','>>':'bitwShiftR(',
                   'and':'&&','or':'||','xor':'xor(','!': '!',
                   'true':'TRUE','false':'FALSE','null':'NULL',
                   'do':'repeat','array':'c'
        }
        # файл, содержащий обратную польскую запись
        f = open('./files/reverse_polsk.txt', 'r')
        inp_seq = f.read()
        f.close()

        t = re.findall(r'(?:\'[^\']*\')|(?:"[^"]*")|(?:[^ ]+)', inp_seq)

        def is_identifier(token):
            return ((token in inverse_tokens) and re.match(r'^I\d+$', inverse_tokens[token]))

        def is_constant(token):
            return ((token in inverse_tokens) and re.match(r'^C\d+$', inverse_tokens[token])) or (
                        (token in inverse_tokens) and re.match(r'^N\d+$',inverse_tokens[token]))

        def is_operation(token):
            return (token in inverse_tokens) and re.match(r'^O\d+$', inverse_tokens[token])

        i = 0
        stack = []
        out_seq = ''
        is_func = False
        variable = 0

        t=[self.tokens[i] if i in self.tokens.keys() else i for i in t]
        tub_num=0
        markers = []

        print(self.else_marks)
        print(self.if_marks)
        # print(self.while_start_marks)
        # print(self.while_end_marks)
        # print(self.do_start_marks)
        # print(self.do_end_marks)
        while i < len(t):
            # print(out_seq)
            print(stack)
            # print(markers)
            # print(t[i])
            # print('-------')
            if is_func == True and not (is_identifier(t[i])):
                out_seq += '{\n'
                is_func = False
            if is_identifier(t[i]) or is_constant(t[i]):
                if t[i] in inverse_tokens and re.match(r'^C\d+$', inverse_tokens[t[i]]):
                    stack.append(f'"{t[i]}"')
                else:
                    stack.append(replace[t[i]] if t[i] in replace else t[i])
            elif t[i] == 'НП':
                stack.pop()
                stack.pop()
                func_name = stack.pop()
                out_seq += '\t'*tub_num + func_name.split('(')[0]+'=function('+func_name.split('(')[1]
                tub_num = tub_num + 1
                is_func = True
            elif t[i] == 'КП':
                tub_num-=1
                out_seq += '\t'*tub_num+ '}\n'
            elif t[i]=='return':
                result = stack.pop()
                out_seq+='\t'*tub_num+'return('+result+');\n'
            elif t[i] == 'УПЛ':
                if(t[i-1] in self.while_end_marks):
                    arg1 = stack.pop()
                    out_seq += '\t'*tub_num+f'while({arg1})' + '{\n'
                    tub_num += 1
                elif(t[i-1] in self.else_marks):
                    stack.pop()
                    arg1 = stack.pop()
                    out_seq += '\t'*tub_num+f'if ({arg1})' + '{\n'
                    tub_num += 1
                elif (t[i + 1] in self.do_start_marks):
                    arg1 = stack.pop()
                    out_seq += '\t'*tub_num+f'if ({arg1})' + '{break;}\n}\n'
                    tub_num -= 1
            elif t[i] == 'БП':
                if (t[i - 1] in self.while_start_marks):
                    out_seq += '\t'*tub_num+'}\n'
                    tub_num -= 1
                elif (t[i - 1] in self.if_marks):
                    out_seq += '\t'*tub_num+'}\nelse{\n'
                    out_seq = out_seq
            elif t[i] == ':':
                if(t[i-1] in self.end_marks):
                    out_seq += '\t' * tub_num + '}\n'
                    tub_num -= 1
                elif(t[i-1] in self.if_marks):
                    out_seq+='\t'*tub_num+'}\n'
                    tub_num-=1
                elif(t[i-1] in self.do_start_marks):
                    out_seq+='\t'*tub_num+'repeat{\n'
                    tub_num+=1
            elif t[i]=='echo':
                arg1=stack.pop()
                out_seq+='\t'*tub_num+f'print({arg1});\n'
            elif is_operation(t[i]):
                if t[i]=='$':
                    out_seq = out_seq
                elif t[i]=='.' and len(stack)>=2:
                    arg1=stack.pop()
                    arg2=stack.pop()
                    out_seq += '\t'*tub_num+f'Rp{variable}='+f'paste({arg2},{arg1},sep="");\n'
                    stack.append(f'Rp{variable}')
                    variable+=1
                elif t[i] == '=' and len(stack) >= 2:
                    arg1 = stack.pop()
                    arg2 = stack.pop()
                    out_seq += '\t'*tub_num+ f'{arg2} <- {arg1};\n'
                else:
                    operation = replace[t[i]] if t[i] in replace else t[i]
                    arg1 = stack.pop()
                    if t[i] != '!':
                        arg2 = stack.pop()
                        out_seq+='\t'*tub_num+f'Rp{variable}='+f'({arg2} {operation} {arg1});\n'
                        stack.append(f'Rp{variable}')
                        variable+=1
                    else:
                        stack.append(f'({operation}{arg1})')
            elif re.match("[0-9]+АЭМ",t[i]):
                k = int(t[i].split('АЭМ')[0])
                a = []
                while k != 0:
                    a.append(stack.pop())
                    k -= 1
                a.reverse()
                stack.append('\t'*tub_num + a[0] + '[' + ','.join(a[1:]) + ']')
            elif t[i] in ['break', 'continue']:
                stack.append(replace[t[i]] if t[i] in replace else t[i])
                arg0 = stack.pop()
                out_seq += '\t'*tub_num + f'\t{arg0};\n'

            elif re.match(r"[0-9]+Ф",t[i]):
                k = int(t[i].split('Ф')[0])
                a = []
                while k != 0:
                    a.append(stack.pop())
                    k -= 1
                a.reverse()
                if(i<len(t)-3 and t[i+3]!='НП'):
                    out_seq+='\t'*tub_num+f"Rp{variable}="+a[0]+'(' + ', '.join(a[1:]) + ');\n'
                    stack.append(f"Rp{variable}")
                    variable+=1
                else:
                    stack.append(a[0]+'(' + ', '.join(a[1:]) + ')')
            else:
                stack.append(t[i])
            i += 1

        stack.clear()
        return out_seq

    #Лаба 4
    def error(self):
        print(self.nxtsymb,self.row_counter,22222)
        out_sq = 'Ошибка в строке '
        f = open('./files/error.txt', 'a')
        out_sq += str(self.row_counter)
        f.write(out_sq+'\n')
        f.close()
        return
    def program(self):
        self.scan()
        if(self.nxtsymb!='<?'):
            self.error()
        self.scan()
        if(self.nxtsymb!='php'):
            self.error()
        self.scan()
        self.text()
        if(self.nxtsymb!='?>'):
            self.error()


    def text(self):

        self.no_end_op_error = ['-','+','/','*','**',')',']','.','==','<=','>=','<','>'
                                ',','<>','!=','%',';','^','&','|','<<','>>','and','or','xor']
        while(self.nxtsymb!='?>'):
            if(self.nxtsymb=='function'):
                self.procedure()
            elif self.identifier() or self.nxtsymb=='echo':
                self.scan()
                if self.nxtsymb == '(':
                    self.brackets.append('(')
                    self.scan()
                    if self.nxtsymb != ')':
                        self.expression()
                        while self.nxtsymb == ',':
                            self.scan()
                            self.expression()
                        if self.nxtsymb != ')':
                            self.error()
                    if len(self.brackets)==0 or (self.brackets and self.brackets.pop() != '('):
                        self.error()
                    self.scan()
                elif self.nxtsymb == '=':
                    self.scan()
                    self.expression()
                    if self.nxtsymb != ';':
                        self.row_counter-=1
                        self.error()
                        self.row_counter+=1
            elif self.nxtsymb=='$':
                self.scan()
                if not self.identifier():
                    self.error()
            elif self.nxtsymb=='return':
                self.scan()
                self.expression()
                if self.nxtsymb!=';':
                    self.row_counter-=1
                    self.error()
                    self.row_counter+=1
            elif self.nxtsymb == 'break':
                self.break_operator()
                self.scan()
                if self.nxtsymb != ';': self.error()
            elif self.nxtsymb == 'continue':
                self.continue_operator()
                self.scan()
                if self.nxtsymb != ';': self.error()
            elif self.nxtsymb=='if':
                self.conditional_operator()
            elif self.nxtsymb == 'while':
                self.while_loop()
            elif self.nxtsymb =='do':
                self.do_loop()
            elif self.nxtsymb=='{':
                self.compound_operator()
            elif self.nxtsymb=='[':
                self.scan()
                self.brackets.append('[')
                self.expression()
                if self.nxtsymb!=']':
                    self.error()
                if len(self.brackets)==0 or (self.brackets and self.brackets.pop()!='['):
                    self.error()
                self.scan()
                if self.nxtsymb == '=':
                    self.scan()
                    self.expression()
                    if self.nxtsymb != ';': self.error()
            elif self.nxtsymb==';':
                self.scan()
            else:
                break

    # оператор break
    def break_operator(self):
        return self.nxtsymb == 'break'

    # оператор continue
    def continue_operator(self):
        return self.nxtsymb == 'continue'
    #Сканирование do-while
    def do_loop(self):
        if self.nxtsymb !='do': self.error()
        self.scan()
        self.compound_operator()
        self.while_loop()

    #Сканирование while
    def while_loop(self):
        if self.nxtsymb != 'while': self.error()
        self.scan()
        if self.nxtsymb != '(': self.error()
        self.brackets.append('(')
        self.condition()
        if self.nxtsymb != ')': self.error()
        if len(self.brackets)==0 or (self.brackets and self.brackets.pop()!='('):
            self.error()
        self.scan()
    #Сканирование if
    def conditional_operator(self):
        if self.nxtsymb != 'if': self.error()
        self.scan()
        if self.nxtsymb != '(': self.error()
        self.condition()
        self.brackets.append('(')
        if self.nxtsymb != ')': self.error()
        if len(self.brackets)==0 or (self.brackets and self.brackets.pop() != '('):
            self.error()
        self.scan()
        self.text()
        if self.nxtsymb == 'else':
            self.scan()
            self.text()

    # условие
    def condition(self):
        if self.unary_log_operation():
            self.scan()
            if self.nxtsymb != '(': self.error()
            self.brackets.append('(')
            self.log_expression()
            if self.nxtsymb != ')': self.error()
            if len(self.brackets)==0 or (self.brackets and self.brackets.pop() != '('):
                self.error()
            self.scan()
        else:
            self.log_expression()
            while self.binary_log_operation():
                self.log_expression()

    # унарная логическая операция
    def unary_log_operation(self):
        return self.nxtsymb == '!'

    # логическое выражение
    def log_expression(self):
        self.scan()
        self.expression()
        self.comparison_operation()
        self.scan()
        self.expression()

    # операция сравнения
    def comparison_operation(self):
        return self.nxtsymb in ['!=', '<', '<=', '==', '>', '>=','<>']

    # бинарная логическая операция
    def binary_log_operation(self):
        return self.nxtsymb == 'and' or self.nxtsymb == 'or' or self.nxtsymb=='xor'

    #Сканирование выражения
    def expression(self):
        if self.nxtsymb == '(':
            self.brackets.append('(')
            self.scan()
            self.expression()
            if self.nxtsymb != ')': self.error()
            if len(self.brackets)==0 or (self.brackets and self.brackets.pop()!='('):
                self.error()
            self.scan()
        elif self.nxtsymb =='$':
            self.scan()
            if not self.identifier():
                self.error()
                self.scan()
            self.expression()
        elif self.identifier():
            self.scan()
            if self.nxtsymb == '(':
                self.brackets.append('(')
                self.scan()
                if self.nxtsymb != ')':
                    self.expression()
                    while self.nxtsymb == ',':
                        self.scan()
                        self.expression()
                    if self.nxtsymb != ')':
                        self.error()
                if len(self.brackets) == 0 or (self.brackets and self.brackets.pop() != '('):
                    self.error()
                self.scan()
            elif self.nxtsymb == '[':
                self.brackets.append('[')
                self.scan()
                self.expression()
                if self.nxtsymb != ']': self.error()
                if len(self.brackets) == 0 or (self.brackets and self.brackets.pop() != '['):
                    self.error()
                self.scan()
        elif self.number_const() or self.constant():
            self.scan()
        else:
            self.error()
        if self.arithmetic_operation():
            self.scan()
            self.expression()

    #Проверяем арифметическая ли операция
    def arithmetic_operation(self):
        return self.nxtsymb in ['%', '*','**', '+', '-', '/','.']
    #Сканирование следующего символа
    def scan(self):
        self.i+=1
        if(self.i>len(self.match)):
            if self.nxtsymb not in ['\n',';','}']:
                self.error()
        else:
            for token_class in self.tokens.keys():
                if self.match[self.i] in self.tokens[token_class]:
                    self.nxtsymb = self.tokens[token_class][self.match[self.i]]
            self.printer()
            if self.nxtsymb=='\n':
                if self.match[self.i-1] in self.tokens['R'].keys() and self.tokens['R'][self.match[self.i-1]] not in ['{','}', ';','\n'] and self.i!=2:
                    self.error()
                self.row_counter += 1
                self.scan()
    #Сканирование функций-процедуры
    def procedure(self):
        #Сканируем название
        self.scan()
        if not self.identifier():
            self.error()
        self.scan()
        #Сканируем аргументы
        if self.nxtsymb!='(':
            self.error()
        self.brackets.append('(')
        self.scan()
        if self.nxtsymb!=')':
            self.list_of_names(type_read=1)
        if self.nxtsymb!=')':
            print(self.nxtsymb,1)
            self.error()
        if len(self.brackets) == 0 or (self.brackets and self.brackets.pop() != '('):
            print(self.brackets)
            self.error()

        self.scan()
        if self.nxtsymb!='{':
            self.error()
        else:
            self.compound_operator()

    #Считываем список аргументов
    def check_is_agrument(self,type_read=0):
        if(self.nxtsymb=='$'):
            self.scan()
            if not self.identifier():
                self.error()
        elif type_read==1:
            self.error()
        else:
            if not(self.constant() or self.number_const()):
                self.error()
    def list_of_names(self,type_read=0):
        self.check_is_agrument(type_read)
        self.printer()
        self.scan()
        while(self.nxtsymb==','):
            self.scan()
            self.check_is_agrument(type_read)
            self.scan()
    #Проверка идентификатора
    def identifier(self):
        return self.nxtsymb in self.tokens['I'].values()
    #Проверка константы
    def constant(self):
        return  self.nxtsymb in self.tokens['C'].values()
    def number_const(self):
        return self.nxtsymb in self.tokens['N'].values()
    #Сканирование блока {}
    def compound_operator(self):
        if self.nxtsymb != '{':
            self.error()
        self.brackets.append('{')
        self.scan()
        self.text()
        if self.nxtsymb != '}':
            self.error()
        print(self.brackets)
        if len(self.brackets) == 0 or (self.brackets and self.brackets.pop() != '{'):
            self.error()

        self.scan()

    def analyzer(self):
        self.i = -1
        self.nxtsymb = None  # разбираемый символ
        self.row_counter = 1  # счётчик строк

        # лексемы
        self.tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

        # файлы, содержащие все таблицы лексем
        for token_class in self.tokens.keys():
            with open('./files/%s.json' % token_class, 'r') as read_file:
                data = json.load(read_file)
                self.tokens[token_class] = data

        # файл, содержащий последовательность кодов лексем входной программы
        f = open('./files/Output.txt', 'r')
        input_sequence = f.read()
        f.close()

        regexp = '[' + '|'.join(self.tokens.keys()) + ']' + '\d+'
        self.match = re.findall(regexp, input_sequence)
        print(self.tokens)
        print(self.match)
        f=open('./files/error.txt','w')
        f.close()
        self.brackets = []
        self.program()

    def printer(self):
        print(self.nxtsymb,self.i,self.row_counter)

