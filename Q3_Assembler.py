#
# Q3_Assembler.py
# By - Shivoy Arora
#      Suhani Mathur
#      Shobhit Pandey
# Date - 20/06/2022
#

import sys


######## Declaring dictionaries ########
# opcode of each command
opcodes = {"add": "10000", "sub": "10001", "mov1": "10010", "mov2": "10011", "ld": "10100", "st": "10101", "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010",
           "or": "11011", "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010", "addf": "00000", "subf": "00001", "movf": "00010"}

# registers binary representation
regs = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
        "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

# statement types
stmtTypes = {"add": "A", "sub": "A", "mov1": "B", "mov2": "C", "ld": "D", "st": "D", "mul": "A", "div": "C", "rs": "B", "ls": "B", "xor": "A",
             "or": "A", "and": "A", "not": "C", "cmp": "C", "jmp": "E", "jlt": "E", "jgt": "E", "je": "E", "hlt": "F", "addf": "A", "subf": "A", "movf": "B"}

# unused space in regard to ops type
unusedSpace = {"A": "00", "B": "", "C": "00000",
               "D": "", "E": "000", "F": "00000000000"}

# address of the variables declared
vars = {}

# address of the labels
labels = {}


class color:
    """ Class color to color the output of the terminal """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def floatBin(number):
    """ Convert a floating number to binary representation with 3-bit exp and 5-bit mantissa

        Args:
            number: floating point number to be converted
        Returns:
            num: string of the floating point representation
    """
    whole, dec = str(number).split(".")

    whole = int(whole)
    dec = float("0."+dec)

    binRepr = bin(whole)[2:] + "."

    for _ in range(7):
        whole, dec = str(dec * 2).split(".")
        binRepr += whole
        dec = float("0."+dec)

    binRepr.strip("0")

    pt = binRepr.find(".")

    exp = pt - 1

    binRepr = "".join(binRepr.split("."))
    mantissa = binRepr[1:6]

    num = "0" * (3 - len(bin(exp)[2:])) + bin(exp)[2:]
    num += mantissa + (5 - len(mantissa)) * "0"

    return num


def checkLine(line, lineNum):
    """ Check if a line of command is correct """
    global vars, labels, stmtTypes
    global flag, errorGenerated

    regs = {"R0", "R1", "R2", "R3", "R4", "R5", "R6"}

    # Operations allowed in the assembler
    opSet = {"add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or",
             "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt", "addf", "subf", "movf"}

    try:
        if line == ["hlt"]:
            flag = 1
        elif line[0] not in opSet:
            errorGenerated = 1
            print(color.RED + color.BOLD + "Error:" +
                  color.END, "Line", lineNum, ", invalid operation")

        else:
            ops = line[0]

            # converting ops to incorporate two types of mov command
            if ops == "mov":
                if line[2][0] == "$":
                    ops = "mov1"
                else:
                    ops = "mov2"

            stmtType = stmtTypes[ops]
            if stmtType == "A" or stmtType == "C":
                if ops == "mov2" and line[1] == "FLAGS" and line[2] in regs:
                    return
                for i in line[1:]:
                    if i not in regs:
                        errorGenerated = 1
                        print(color.RED + color.BOLD + "Error:" +
                              color.END, "Line", lineNum, ", invalid register")

            elif stmtType == "B":
                try:
                    if line[1] not in regs:
                        errorGenerated = 1
                        print(color.RED + color.BOLD + "Error:" +
                              color.END, "Line", i+1, ", invalid register")
                    elif ops == "movf" and (float(line[2][1:]) > 252 or float(line[2][1:]) < 1):
                        errorGenerated = 1
                        print(color.RED + color.BOLD + "Error:" + color.END, "Line",
                              lineNum, ", invalid value of floating point immediate")
                    elif ops == "movf" and line[2][1:].find(".") == -1:
                        errorGenerated = 1
                        print(color.RED + color.BOLD + "Error:" + color.END, "Line",
                              lineNum, ", invalid floating point immediate (No floating point found)")
                    elif ops != "movf" and (int(line[2][1:]) > 255 or int(line[2][1:]) < 0):
                        errorGenerated = 1
                        print(color.RED + color.BOLD + "Error:" + color.END, "Line",
                              lineNum, ", invalid value of immediate")
                except ValueError as e:
                    errorGenerated = 1
                    print(color.RED + color.BOLD + "Error:" + color.END, "Line",
                          lineNum, ", invalid immediate value")
            elif stmtType == "D":
                if line[1] not in regs:
                    errorGenerated = 1
                    print(color.RED + color.BOLD + "Error:" +
                          color.END, "Line", lineNum, ", invalid register")
                elif line[2] not in vars:
                    errorGenerated = 1
                    print(color.RED + color.BOLD + "Error:" +
                          color.END, "Line", lineNum, ", variable not found")
            elif stmtType == "E":
                if line[1] not in labels:
                    errorGenerated = 1
                    print(color.RED + color.BOLD + "Error:" +
                          color.END, "Line", lineNum, ", label not found")
    except:
        errorGenerated = 1
        print(color.RED + color.BOLD + "Error:" +
              color.END, "Line", lineNum, ", unexpected error found")


################# Main Function #################
if __name__ == "__main__":
    ######## Getting the input from STDIN ########
    """ 
        Format of lines: List[List[string]]

        For eg:-
            for command:    "add R1 R2 R3\nmov R3 R4"
            lines is:       [["add", "R1", "R2", "R3"], ["mov", "R3", "R4"]]
    """
    lines = [[j.strip() for j in i.strip().split()]
             for i in sys.stdin.readlines()]

    ######## Managing Addresses of labels and variables ########
    # Getting the labels addresses
    addr = 0
    commands = []
    for i in lines:
        if i == []:
            continue
        elif i[0] == "var":
            continue
        elif i[0][-1] == ":":
            binAddr = bin(addr)[2:]
            labels[i[0][:-1]] = "0" * (8 - len(binAddr)) + binAddr

            # removing the label from the command
            i.pop(0)

            # if the label doesn't have a command on the same line continuing
            if i == []:
                continue

        commands.append(i)
        addr += 1

    # Getting the variables addresses
    for i in lines:
        if i == []:
            continue
        if i[0] == "var":
            binAddr = bin(addr)[2:]
            vars[i[1]] = "0" * (8 - len(binAddr)) + binAddr
            addr += 1
        else:
            break

    ######## Checking Errors ########
    flag = 0                # For hlt instruction not found
    errorGenerated = 0      # To check if no error is generated, if not then assemble the code
    for i in range(len(lines)):
        # skipping empty lines
        if len(commands) > 256:
            print(color.RED + color.BOLD + "Error:" + color.END,
                  "Number of lines in code exceed the memory of the ISA")

        if lines[i] == []:
            continue

        # if hlt is not the last operation
        if flag == 1:
            print(color.RED + color.BOLD + "Error:" + color.END,
                  "Line", i+1, ", halt is not the last instruction")

            errorGenerated = 1
            break

        if lines[i][0] == "var":
            continue
        elif lines[i][-1] == ":":
            checkLine(lines[i][1:], i+1)
        else:
            checkLine(lines[i], i+1)

    # if hlt statement is not present
    if flag == 0:
        print(color.RED + color.BOLD + "Error:" +
              color.END, "hlt instructions not found")
        errorGenerated = 1

    ######## Converting to machine code ########
    if errorGenerated == 0:
        # creating machine code lst
        machineCode = []

        # traversing each command
        for sNo in range(len(commands)):
            binLine = ""

            ops = commands[sNo][0]

            # converting ops to incorporate two types of mov command
            if ops == "mov":
                if commands[sNo][2][0] == "$":
                    ops = "mov1"
                else:
                    ops = "mov2"

            # adding opcode to binLine
            binLine = opcodes[ops]

            # adding unused space
            stmtType = stmtTypes[ops]
            binLine += unusedSpace[stmtType]

            # For statements with only registers and immediate values
            if stmtType == "A" or stmtType == "B" or stmtType == "C":
                for i in commands[sNo][1:]:

                    # if registers are present
                    if i[0] != "$":
                        binLine += regs[i]

                    # immediate value is present
                    #
                    # For floating point
                    elif ops == "movf" and i[0] == "$":
                        binLine += floatBin(i[1:])

                    else:
                        binRepr = bin(int(i[1:]))[2:]
                        binLine += "0" * (8 - len(binRepr)) + binRepr

            # For ld and st statements
            elif stmtType == "D":
                # adding register to binLine
                binLine += regs[commands[sNo][1]]

                binLine += vars[commands[sNo][2]]

            # For jumping statements
            elif stmtType == "E":
                # adding label addr to binLine
                binLine += labels[commands[sNo][1]]

            # For hlt statement
            elif stmtType == "F":
                pass

            # Adding the line to the machine code
            machineCode.append(binLine)

        ######## Writing to stdout ########
        for i in machineCode:
            print(i)
