class FAException(Exception):
    pass

class FiniteAutomata:
    def __init__(self,states=None,alphabet=None,transitions=None,initialState=None,finalStates=None,isDFA=False):
        self.__states = states
        self.__alphabet = alphabet
        self.__transitions = dict()
        self.__initial_state = initialState
        self.__final_states = finalStates
        self.__isDFA = isDFA

    def getStates(self):
        return self.__states

    def getAlphabet(self):
        return self.__alphabet

    def getInitialState(self):
        return self.__initial_state
    
    def getFinalStates(self):
        return self.__final_states
    
    def getTransitions(self):
        return self.__transitions
    
    def getIsDFA(self):
        return self.__isDFA
    
    def checkTransitions(self):
        for key in self.__transitions.keys():
            if key[0] not in self.__states:
                raise FAException("The states from the trasitions must be part of the set of states")
            if key[1] not in self.__alphabet:
                raise FAException("The second element of the transition must be part of the alphabet")
        for value in self.__transitions.values():
            for val in value:
                if val not in self.__states:
                    raise FAException("The states from the transitions must be part of the set of states")
    
    def checkFinalState(self):
        for state in self.__final_states:
            if state not in [sublist for sublist in self.__transitions.values()]:
                raise FAException("The final state is not final in any of the transitions")
            
    def checkInitialState(self):
        if self.__initial_state[0] not in [sublist[0] for sublist in self.__transitions.keys()]:
            raise FAException("The initial state is not initial in any of the transitions")
    
    def liniarize(self,nested_list):
        return [item for sublist in nested_list for item in sublist]

    def checkRedundantState(self):
        for state in self.__states:
            if state!= self.__initial_state[0] and state not in self.liniarize([transition for transition in self.__transitions.values()]):
                raise FAException("The state "+ state+" is not part of any transitions")
    
    def finalCheck(self):
        self.checkTransitions()
        self.checkFinalState()
        self.checkInitialState()
        self.checkRedundantState()

    def readFromFile(self,input_file):
        result = []
        with open(input_file,"r") as f:
            partial_result = f.readlines()
        for elem in partial_result:
            result.append(elem.split())
        return result

    def initializeFA(self,input_file):
        file = self.readFromFile(input_file)
        for i in range(0,len(file)):
            if i==0:
                self.__states = file[i][1:]
            elif i==1:
                self.__alphabet = file[i][1:]
            elif i==len(file)-2:
                self.__initial_state = file[i][1:]
            elif i==len(file)-1:
                self.__final_states = file[i][1:]
            else:
                key = (file[i][1],file[i][2])
                value = file[i][3]
                if key in self.__transitions.keys():
                    values = [self.__transitions[key]]
                    values.append(value)
                    self.__transitions[key] = values
                else:
                    self.__transitions[key] =  value
    
    def checkIfDFA(self):
        for value in self.__transitions.values():
            if len(value)>1:
                return False
            return True
    
    def loadFA(self,input_file):
        self.initializeFA(input_file)
        self.finalCheck()
        self.__isDFA = self.checkIfDFA()
    
    def checkSequenceAccepted(self,state,sequence,finalStates,transitions):
        # |- (qf,epsilon) state-ul curent e cel final iar secventa e empty,epsilon
        if not sequence and state in finalStates:
            return True
        
        if not sequence and state not in finalStates:
            return False
        
        for key, value in transitions.items():
            if key[0] == state[0] and key[1] == sequence[0]:
                if isinstance(value, list):
                    for resultState in value:
                        if self.checkSequenceAccepted(resultState, sequence[1:], finalStates, transitions):
                            return True
                else:
                    if self.checkSequenceAccepted(value, sequence[1:], finalStates, transitions):
                        return True

        return False
        


    

            


    


   