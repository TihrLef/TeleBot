def printu(s, end = "\n"):
    print('\033[4m' + s + '\033[0m', end = end)
    
def printb(s, end = "\n"):
    print('\033[1m' + s + '\033[0m', end = end)

dic = {type(dict()): "'''Словарь'''",
       type(list()): "'''Список'''",
       type(tuple()): "'''Кортеж'''",
       type(set()): "'''Множество'''"}

def SFO(struct, Format = False, word = "", key = ""):
    fulltab = ''
    for to in word:
        fulltab = fulltab + "│   " if to != '0' else fulltab + "    "
        
    if isinstance(struct, (int, str, float, bool)):
        print(fulltab + str(struct))
        return
    
    if key == "list":
        print(fulltab[:-4] + "├───", end = "")
    elif key == "listlast":
        print(fulltab[:-4] + "└───", end = "")
    if Format:
        printu('\033[41m' + dic[type(struct)] + '\033[0m')
    else:
        print(dic[type(struct)])

    newword = ""
    newtab = ""
    newkey = "list"

    if isinstance(struct, dict):
        helper = list(struct.keys())
        for i in range(len(helper)): 
            to = helper[i]
            if i != len(helper) - 1:
                newtab = fulltab + "├───"
                newword = word + '1'
            else:
                newtab = fulltab + "└───"
                newword = word + '0'
            if Format:
                printb(newtab + str(to), end = ": ")
            else:
                print(newtab + str(to), end = ": ")
            if isinstance(struct[to], (int, str, float, bool)): 
                print(struct[to])
            else:
                SFO(struct[to], Format, newword)
                    
    elif isinstance(struct, (list, tuple, set)):
        for i in range(len(struct)):
            to = struct[i]
            if i != len(struct) - 1:
                newtab = fulltab + "├───"
                newword = word + '1'
            else:
                newtab = fulltab + "└───"
                newword = word + '0'
                newkey = "listlast"
            if isinstance(to, (int, str, float, bool)): 
                print(newtab + str(to))
            else:
                SFO(to, Format, newword, newkey)
    print(fulltab)
                
                
struct = {0:1, 1: 5, 2: ["12", 23, 45.5, True], 3: {0:1, 1: 5, 2: ["12", 23, 45.5, True], 3: {0:1, 1: 5, 2: ["12", 23, 45.5, True]}}}         
SFO(struct)

