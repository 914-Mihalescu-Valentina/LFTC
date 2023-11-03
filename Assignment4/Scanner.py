import re,os
from Pif import Pif
from SymbolTable import *

class LexicalError(Exception):
    pass

class Scanner:
    def __init__(self,input_file,tokens_file,pif,symtbl):
        self.__input_file = input_file
        self.__tokens_file = tokens_file
        self.__pif = pif
        self.__symtbl = symtbl
    
    def get_input_file(self):
        return self.__input_file
    
    def get_tokens_file(self):
        return self.__tokens_file
    
    def get_pif(self):
        return self.__pif
    
    def get__symtbl(self):
        return self.__symtbl
    
    def detect(self,input_string):
        space_split = input_string.split()
        result = []

        for element in space_split:
            # \s+: matches one or more whitespace characters (spaces, tabs, etc.) 
            split_elements = re.split(r'(\s+|\(|\)|==|:=|;|,|\[|\]|\{|\}|\+|\-|\*|<=|>=|>|<|!=|=|%|\/)', element)
            result.extend(split_elements)

        # Remove empty strings from the result
        result = [s for s in result if s]

        return result
    
    def is_identifier(self,token):
        pattern = r'^([a-zA-Z])([a-zA-Z]|[0-9])*$'
        match = re.match(pattern, token)
        if match:
            return True
        else:
            return False

        
    
    def is_constant(self,token):
        patterns = [
            r'^(0|((-|\+)|([1-9][0-9]*)))$',
            r'^"[a-zA-Z ]*"$',
            r"^'[a-zA-Z0-9 ]'$"
            ]
        matches_any = any(re.match(pattern, token) for pattern in patterns)
        if matches_any:
            return True
        else:
            return False
        

    def classify(self,token):
        try:
            with open("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\token.in",'r') as file:
                file_content = file.readlines()
                for line in file_content:
                    category = line.strip().split(':')[0]
                    if category == 'reserved':
                        values_list_string = line.strip().split(':')[1]
                        values_list_string = values_list_string.strip('[]')  # Remove square brackets
                        token_list = [token.strip("' ") for token in values_list_string.split(',')]
                    else:
                        start_index = line.find('[')
                        end_index = line.rfind(']')
                        array_content = line[start_index + 1:end_index]
                        token_list = array_content
                    if token in token_list:
                        if category == 'reserved':
                            return 'reserved'
                        elif category == 'operator':
                            return 'operator'
                        else:
                            return 'separator'
                if self.is_constant(token) is True:
                        return 'constant'
                elif self.is_identifier(token) is True:
                        return 'identifier'
                else:
                        return 'lexical error'

        except FileNotFoundError:
            print(f"The file '{self.__tokens_file}' does not exist.")

    def codify(self,token):
        if self.classify(token)=='separator' or self.classify(token)=='operator' or self.classify(token)=='reserved':
            self.__pif.add(token,(-1))
            return 1
        elif self.classify(token) =='identifier':
            pair_pos = self.__symtbl.getPos(token)
            if pair_pos==():
                pair_pos = self.__symtbl.getPos(token)
            self.__pif.add('id',pair_pos)
            return 1
        elif self.classify(token) =='constant':
            pair_pos = self.__symtbl.getPos(token)
            if pair_pos==():
                pair_pos = self.__symtbl.getPos(token)
            self.__pif.add('const',pair_pos)
            return 1
        else:
           return 0

    def scan(self):
        try:
            with open(self.__input_file,'r') as file:
                line_number = 0
                res = 0
                flag=1
                file_content = file.readlines()
                for line in file_content:
                    line_number = line_number+1
                    tokens = self.detect(line)
                    try:
                        for token in tokens:
                            res = self.codify(token)
                            if res==0:
                                error_message = f"Lexical error! for token {token} on line {line_number}"
                                flag=0
                                raise LexicalError(error_message)
                    except LexicalError as message:
                                print(message)
                if flag == 1:
                    return (self.__pif,self.__symtbl)
                  
                    
                

        except FileNotFoundError:
            print(f"The file '{self.__input_file}' does not exist.")





    


        
