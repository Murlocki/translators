from PyQt6.QtCore import QRunnable, QThread
from PyQt6.QtGui import QTextCursor
import json

class LecAnalysis():
    def createTokensCod(self,token_class,token_value):
        if not(token_value in self.tokens[token_class]):
            token_code = str(len(self.tokens[token_class])+1)
            self.tokens[token_class][token_value] = token_class + token_code
    def __init__(self):
        self.OPERATIONS = ['$','.','+','-','*','/','%','**','=','==','>','>=','<','<=','<>','^','&','|','~','<<','>>','!','and','or','xor','pow','sqrt','sin','cos','tan','abs','log','log10','max','min']
        self.SERVICE_WORDS = ['if','else','else if','while','break','continue','function','return','echo','true','false','array','null','do']
        self.SEPARATORS = [';','(',')',' ','\n','\t',"'",'"','<?','?>','{','}','[',']','#']
        self.tokens = {'W':{},'I':{},'O':{},'R':{},'N':{},'C':{}}
    def process(self):
        for service_word in self.SERVICE_WORDS:
            self.createTokensCod('W',service_word)
        for operation in self.OPERATIONS:
            self.createTokensCod('O',operation)
        for separator in self.SEPARATORS:
                self.createTokensCod('R', separator)
        f = open('./files/Input.txt','r')
        input_sequence = f.read()
        f.close()

        i=0
        state = 'S'
        output_sequance = buffer = ''
        while i!=len(input_sequence):
            symbol = input_sequence[i]
            if state=='S':
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
                    output_sequance += self.tokens['R'][symbol] + ' '
                elif symbol =='"':
                    state='q10'
                    output_sequance += self.tokens['R'][symbol] + ' '
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
            elif state=='q9':
                if symbol=='_':
                    state='q26'
                    buffer=symbol
                if symbol.isalpha():
                    state='q1'
                    buffer=buffer+symbol
            elif state =='q1':
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
            elif state=='q2':
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
            elif state=='q3':
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
            elif state=='q7':
                if symbol.isdigit():
                    state='q4'
                    buffer = buffer + symbol
            elif state=='q5':
                if symbol.isdigit() or symbol=='-':
                    state='q6'
                    buffer = buffer + symbol
            elif state=='q6':
                if symbol.isdigit():
                    state='q6'
                    buffer = buffer + symbol
                else:
                    self.createTokensCod('N',buffer)
                    output_sequance+=self.tokens['N'][buffer]+' '
                    state = 'S'
                    i=i-1
            elif state=='q4':
                if symbol.isdigit():
                    state='q4'
                    buffer = buffer + symbol
                else:
                    self.createTokensCod('N', buffer)
                    output_sequance += self.tokens['N'][buffer] + ' '
                    state='S'
                    i=i-1
            elif state=='q8':
                if symbol!="'":
                    state='q8'
                    buffer=buffer+symbol
                else:
                    self.createTokensCod('C',buffer)
                    output_sequance+=self.tokens['C'][buffer] + ' ' + self.tokens['R'][symbol] + ' '
                    state = 'S'
            #НИКАКИХ ОБРАЩЕНИЙ К ЭЛЕМЕНТАМ МАССИВОВ В ЭТИХ СТРОКАХ и никаких множественных $
            elif state=='q10':
                if symbol !='"' and symbol!="$":
                    state='q10'
                    buffer = buffer + symbol
                elif symbol=='"':
                    self.createTokensCod('C', buffer)
                    output_sequance += self.tokens['C'][buffer] + ' ' + self.tokens['R'][symbol]+ ' '
                    state = 'S'
                else:
                    self.createTokensCod('C', buffer)
                    output_sequance += self.tokens['C'][buffer] + ' ' + self.tokens['O']['.'] + ' ' + self.tokens['O']['$'] + ' '
                    state = 'q11'
                    buffer = ''
            elif state=='q11':
                buffer=''
                if symbol.isalpha():
                    state='q12'
                    buffer = buffer + symbol
                elif symbol=='_':
                    state='q27'
                    buffer = buffer + symbol
            elif state=='q12':
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
            elif state=='q13':
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
            elif state=='q14':
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
                elif symbol in self.tokens['O'].keys():
                    state='q14'
                    buffer=buffer+symbol
                else:
                    state='S'
                    self.createTokensCod('O', buffer)
                    output_sequance += self.tokens['O'][buffer]+ ' '
                    i=i-1
            elif state=='q15':
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
            elif state=='q16':
                if symbol=='*':
                    state='q18'
                    buffer=buffer+symbol
                else:
                    state='q16'
                    buffer=buffer+symbol
            elif state=='q17':
                if i==len(output_sequance)-1:
                    output_sequance+='\n'
                    state='Z'
                    buffer=''
                elif symbol=='\n':
                    output_sequance+='\n'
                    state='S'
            elif state=='q18':
                if symbol!='/':
                    state='q16'
                    buffer=buffer+symbol
                else:
                    output_sequance += '\n'
                    state = 'S'
            elif state=='q19':
                state='q17'
                buffer=buffer+symbol
            elif state=='q20':
                self.createTokensCod('R',buffer)
                state='S'
                if buffer!=' ':
                    output_sequance+=self.tokens['R'][buffer]+' '
                if buffer=='\n':
                    output_sequance += '\n'
                i=i-1
            elif state=='q26':
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

