from FiniteAutomata import FiniteAutomata


class MenuFAException(Exception):
    pass
class MenuFA:
    def __init__(self):
        self.__finiteAutomata = FiniteAutomata()
        self.__commands = dict()
        self.__commands["1"] = lambda: self.showStates()
        self.__commands["2"] = lambda: self.showAlphabet()
        self.__commands["3"] = lambda: self.showTransitions()
        self.__commands["4"] = lambda: self.showInitialState()
        self.__commands["5"] = lambda: self.showFinalState()
        self.__commands["6"] = lambda: self.showIsDFA()
        self.__commands["7"] = lambda: self.showIsSequenceAccepted()

    def getCommands(self):
        return self.__commands
    
    def getFiniteAutomata(self):
        self.__finiteAutomata
    
    def showStates(self):
        print("The states are: "+" ".join(self.__finiteAutomata.getStates()))
    
    def showAlphabet(self):
        print("The alphabet is: "+" ".join(self.__finiteAutomata.getAlphabet()))
    
    def showInitialState(self):
        print("The intitial state is: "+" ".join(self.__finiteAutomata.getInitialState()))
    
    def showFinalState(self):
        print("The final state is: "+" ".join(self.__finiteAutomata.getFinalStates()))
    
    def showTransitions(self):
        print("The transitions are: ")
        for key, values in self.__finiteAutomata.getTransitions().items():
            for value in values:
                if isinstance(value, list):
                    for v in value:
                        print(f"{key[0]} -> {key[1]} -> {v}")
                else:
                    print(f"{key[0]} -> {key[1]} -> {value}")

    def showIsDFA(self):
        if self.__finiteAutomata.getIsDFA():
            print("The finite automata is DFA")
        else:
            print("The finite automata is NOT DFA")
    
    def showIsSequenceAccepted(self):
        if self.__finiteAutomata.getIsDFA() is False:
            print("The finite automata must be deterministic in order to check if a sequence is accepted")
        else:
            sequence = input("Enter the sequence ")
            if self.__finiteAutomata.checkSequenceAccepted(self.__finiteAutomata.getInitialState(),sequence,self.__finiteAutomata.getFinalStates(),self.__finiteAutomata.getTransitions()) is True:
                print("The sequence "+sequence+" is accepted by the FA")
            else:
                print("The sequence "+sequence+" is not accepted by the FA")
        

    def showMenu(self):
        print("1. Show set of states.")
        print("2. Show alphabet.")
        print("3. Show transitions.")
        print("4. Show initial state.")
        print("5. Show set of final states.")
        print("6. Is DFA?")
        print("7. Check if sequence is accepted (console).")
        print("0. Exit")

    def run(self):
        self.__finiteAutomata.loadFA("FA.in")
        while True:
            self.showMenu()
            try:
                choice =input("Enter the option that you want ")
                if choice in self.__commands:
                    self.__commands[choice]()
                elif choice=="0":
                    print("Exit!")
                    return
                else:
                    print("Invalid choice")
            except MenuFAException as e:
                print(e)
    

