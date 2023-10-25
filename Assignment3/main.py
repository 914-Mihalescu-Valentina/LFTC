from SymbolTable import SymTable
def main():
    sym_table = SymTable(8)

    sym_table.insert("key1") #
    sym_table.insert("key2") #
    sym_table.insert("key3") #
    sym_table.insert("z")    #ascii code of z is 122, 122%8 = 2
    sym_table.insert("2")    #ascii code of 2 is 50, 50%9 = 2

    print(sym_table.search("key1"))  
    print(sym_table.search("key4")) 

    for i in range(sym_table.get_m()):
        print(f"Bucket {i}:")
        current_node = sym_table.get_tbl()[i].head
        while current_node:
            print(current_node.get_keysymbol())
            current_node = current_node.get_next()

if __name__ == "__main__":
    main()

       
