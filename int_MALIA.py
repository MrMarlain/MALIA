from time import sleep
import sys
from random import randint as rd
from traceback import format_exc

def getCode(file_path: str):
    if INT_SETTINGS[5]: print(f'{file_path=}\n')
    with open(file_path, 'r', encoding='utf-8') as file:
        
        commands = [line.split("//")[0].replace('\n', '').strip().split(' ')[:3] for line in file.readlines()]
        
        i = 0
        while i < len(commands):
            command = commands[i]

            if command[0] == "":
                commands[i] = ""
            else:
                commands[i] = [command[0], *map(int, command[1:]), *[0 for _ in range(3 - len(command))]]

            if command[0] == "setarr":
                arr_vname = int(command[1])
                arr_size = int(command[2])
                for j in range(arr_size):
                    commands[i+j+1] = ['set', arr_vname+j, int(commands[i+j+1][0])]
                commands[i] = ''
                i += arr_size


            i+=1

        return commands
'''
include file_path // подключить "модуль" WIP

alocate count // выделить память
sarea arname // переключить арену

set addr value
setv addr addr
sets value       // по адресу select установить значение value
setsv addr       // по адресу select установить значение из addr
setrds start end // случайное число
setappv addr value


if compare_id value
ifsv compare_id addr // сравнить selector с значением addr
ifss compare_id value // сравнить selector.addr с value
ifv compare_id addr
    compare_id:
        0 - ==
        1 - !=
        2 - > 
        3 - <
        4 - >=
        5 - <=

point pname

goto line_count addtopath(0/1)
gotoadd count addtopath(0/1)
gotopoint pname  addtopath(0/1)
gotoback

add addr value
addv addr addr
adds value  // по адресу select прибавить value
addsv addr  // по адресу select прибавить значение из addr

show addr
shows

write char_code
writes // напечатать символ из selector
writev addr // напечатать символ из addr

select addr // переместить select на addr
selectv addr // переместить select на адресс из addr
selectm count // переместить select по памяти на count адресов

setarr addr size
'''


def compare(code, value_1, value_2) -> bool:
    if (code == 0 and value_1 == value_2) or \
        (code == 1 and value_1 != value_2) or \
        (code == 2 and value_1 > value_2) or \
        (code == 3 and value_1 < value_2) or \
        (code == 4 and value_1 >= value_2) or \
        (code == 5 and value_1 <= value_2):
            return True
    return False

def getValueSelect():
    return getValue(INT_CURRENT_VAR)

def getValue(address: int):
    if not (0 <= address < len(INT_MEMORY[INT_AREA])): raise Exception(f"Попытка получить несуществующий адрес ячейки({address})") 
    return INT_MEMORY[INT_AREA][address]

def setValue(address: int, value: int):
    if not (0 <= address < len(INT_MEMORY[INT_AREA])): raise Exception(f"Попытка получить несуществующий адрес ячейки({address})") 
    INT_MEMORY[INT_AREA][address] = value

def addValue(address: int, value: int):
    setValue(address, getValue(address) + value)

def runCommand(line):
    global INT_MEMORY, INT_LINE_COUNTER, INT_CURRENT_VAR

    if isinstance(line, str): return

    command = line[0]
    arg1 = int(line[1])
    arg2 = int(line[2])
    if command != "" and INT_SETTINGS[1]:
        sleep(INT_SETTINGS[2]/1000)
        print(f'        {INT_LINE_COUNTER+1}) {command=}\t{arg1=}\t{arg2=}')

    md = INT_SETTINGS[8]
    
    match command:
        case "alocate":
            INT_MEMORY[INT_AREA] = [0 for _ in range(arg1)]
        
        case "exit":
            INT_SETTINGS[0] = 1

        case "setappv":
            INT_SETTINGS[arg1] = arg2
        case "set":
            setValue(arg1, arg2)
        case "setv":
            setValue(arg1, getValue(arg2))
        case "sets":
            INT_CURRENT_VAR = arg2
        case "setsv":
            INT_CURRENT_VAR = getValue(arg2)
        case "setrds":
            setValue(INT_CURRENT_VAR, rd(arg1, arg2))

        case "if":
            if compare(arg1, getValueSelect(), arg2):
                INT_LINE_COUNTER += 1
        case "ifv":
            if compare(arg1, getValueSelect(), getValue(arg2)):
                INT_LINE_COUNTER += 1
        case "ifsv":
            if compare(arg1, INT_CURRENT_VAR, getValue(arg2)):
                INT_LINE_COUNTER += 1
        case "ifss":
            if compare(arg1, INT_CURRENT_VAR, arg2):
                INT_LINE_COUNTER += 1

        case "point":
            if arg1 in INT_POINTS.keys(): raise Ellipsis(f'Поинт с id={arg1} уже существует')
            INT_POINTS[arg1] = INT_LINE_COUNTER

        case "goto":
            if arg2: INT_POINT_PATH.append(INT_LINE_COUNTER)
            INT_LINE_COUNTER = arg1
        case "gotoadd":
            if arg2: INT_POINT_PATH.append(INT_LINE_COUNTER)
            INT_LINE_COUNTER += arg1 - 1
        case "gotopoint":
            if arg2: INT_POINT_PATH.append(INT_LINE_COUNTER)
            INT_LINE_COUNTER = INT_POINTS[arg1]
        case "gotoback":
            INT_LINE_COUNTER = INT_POINT_PATH[-1]
            INT_POINT_PATH.pop()

        case "add":
            addValue(arg1, arg2)
        case "addv":
            addValue(arg1, getValue(arg2))
        case "adds":
            INT_CURRENT_VAR += arg2
        case "addsv":
            INT_CURRENT_VAR += getValue(arg2)

        case "show":
            print(f'show var {arg1} = {getValue(arg1)}')
        case "shows":
            print(f'show var {arg1} = {getValue(INT_CURRENT_VAR)}')
        
        case "write":
            print(chr(arg1), end='', flush=True)
        case "writes":
            print(chr(getValueSelect()), end='', flush=True)
        case "writev":
            print(chr(arg1), end='', flush=True)

        case "select":
            INT_CURRENT_VAR = arg1
        case "selectv":
            INT_CURRENT_VAR = getValue(arg1)
        case "selectm":
            INT_CURRENT_VAR += arg1
        
        case _:
            raise Exception(f'Команды "{command}" не существует!')

try:
    if len(sys.argv) <= 1:
        input(f'Please, select file.malia and run interpreter:\npython int_MALIA.py your_file.malia')
        exit()
    INT_SETTINGS = {
        0: 0,    # 0/1  close app
        1: 0,    # 0/1  hide/show write commands
        2: 100,  # write delay in mls 
        3: 0,    # 0/1  wait close
        4: 0,    # 0/1  show code 
        5: 0,    # 0/1  show path file
        6: 0,    # 0/1  show result memory
        7: 0,    # 0/1  show count steps
        8: 0,    # 0/1  hide/show commands details
    }
    INT_CODE = getCode(sys.argv[1])
    INT_MEMORY = {0: []}
    if INT_SETTINGS[4]: print(f'INT_CODE:\n{"\n".join([f'{i+1})\t{isinstance(INT_CODE[i], str) if '' else INT_CODE[i]}' for i in range(len(INT_CODE))])}')   
    INT_STEP_COUNTER = 0
    INT_LINE_COUNTER = 0
    INT_CURRENT_VAR = None
    INT_POINTS = {}
    INT_POINT_PATH = []
    INT_AREA = 0
    if INT_SETTINGS[4]: print(f'\nPROGRAMM RUN\n')
    while INT_LINE_COUNTER < len(INT_CODE) and not INT_SETTINGS[0]:
        runCommand(INT_CODE[INT_LINE_COUNTER]) 
        INT_LINE_COUNTER += 1
        INT_STEP_COUNTER += 1
    if INT_SETTINGS[4]: print(f'\nPROGRAMM STOP\n')
    if INT_SETTINGS[7]: print(f'steps: {INT_STEP_COUNTER}')
    if INT_SETTINGS[6]: print(f'{INT_MEMORY=}')
    if INT_SETTINGS[3]: input()
except:
    input(format_exc())