#
# Q4.py
# By - Shivoy Arora
#      Suhani Mathur
#      Shobhit Pandey
# Date - 30/06/2022
#

from matplotlib import pyplot as plt
import sys

MAX_REG = 65535

xPC = []
yPC = []

x = []
y = []

showPlt = False

memAddress = dict()


class registers:
    """ Call registers to handle the value of registers and printing them """

    def __init__(self):
        self.regs = {"000": 0, "001": 0, "010": 0, "011": 0,
                     "100": 0, "101": 0, "110": 0, "111": "0"*16, "PC": 0}

    def clearFlag(self):
        """ Clear FLAGS """
        self.regs["111"] = "0"*16

    def setOverflow(self):
        """ Set Overflow in FLAGS """
        self.regs["111"] = "0"*12 + "1" + "000"

    def setLess(self):
        """ Set less than in FLAGS """
        self.regs["111"] = "0"*13 + "1" + "00"

    def setGreater(self):
        """ Set greater than in FLAGS """
        self.regs["111"] = "0"*14 + "1" + "0"

    def setEqual(self):
        """ Set equal to in FLAGS """
        self.regs["111"] = "0"*15 + "1"

    def convBin8(self, num):
        """ Convert the num to 8 bit binary  number

            Args:
                int num: number to be converted

            Returns: 8 bit binary representation of num
        """
        binNum = bin(num)[2:]
        return "0"*(8-len(binNum)) + binNum

    def convBin16(self, num):
        """ Convert the num to 16 bit binary  number

            Args:
                int num: number to be converted

            Returns: 16 bit binary representation of num
        """
        binNum = bin(num)[2:]
        return "0"*(16-len(binNum)) + binNum

    def __repr__(self) -> str:
        return "{} {} {} {} {} {} {} {} {}".format(self.convBin8(self.regs["PC"]), self.convBin16(self.regs["000"]), self.convBin16(self.regs["001"]), self.convBin16(self.regs["010"]),
                                                   self.convBin16(self.regs["011"]), self.convBin16(self.regs["100"]), self.convBin16(self.regs["101"]), self.convBin16(self.regs["110"]), self.regs["111"])


class operation:
    """ Class operation to handle the operations to be done """

    def __init__(self, regs: registers) -> None:
        # operation of each opcode
        self.opcodes = {"10000": self.add, "10001": self.sub,  "10010": self.mov1,  "10011": self.mov2,  "10100": self.ld,  "10101": self.st,  "10110": self.mul,  "10111": self.div,  "11000": self.rs,  "11001": self.ls,
                        "11010": self.xor,  "11011": self.orOps,  "11100": self.andOps,  "11101": self.notOps,  "11110": self.cmp,  "11111": self.jmp,  "01100": self.jlt,  "01101": self.jgt,  "01111": self.je,  "01010": self.hlt}

        self.regsObj = regs
        self.regs = regs.regs

    ##### Functions of the operations that has to be done #####
    def add(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] + \
            self.regs[command[3:6]]

        # checking for overflow
        if self.regs[reg3] > MAX_REG:
            self.regsObj.setOverflow()

            self.regs[reg3] %= (MAX_REG+1)

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def sub(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation who is eight
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] - \
            self.regs[command[3:6]]

        # checking for overflow
        if self.regs[reg3] < 0:
            self.regs[reg3] = 0
            self.regsObj.setOverflow()

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def mov1(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[:3]] = int(command[3:], 2)

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def mov2(self, command):
        # removing filler bits
        command = command[5:]

        if command[:3] != "111":
            self.regs[command[3:]] = self.regs[command[:3]]
        else:
            self.regs[command[3:]] = int(self.regs[command[:3]], 2)

        # Clearing the flag
        self.regsObj.clearFlag()

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def ld(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        # adding to the graph
        y.append(int(command[3:], 2))
        x.append(xPC[-1])

        if int(command[3:], 2) in memAddress:
            self.regs[command[:3]] = memAddress[int(command[3:], 2)]
        else:
            self.regs[command[:3]] = 0
            memAddress[int(command[3:], 2)] = 0

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def st(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        # adding to the graph
        y.append(int(command[3:], 2))
        x.append(xPC[-1])

        memAddress[int(command[3:], 2)] = self.regs[command[:3]]

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def mul(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] * \
            self.regs[command[3:6]]

        # checking for overflow
        if self.regs[reg3] > MAX_REG:
            self.regsObj.setOverflow()

            self.regs[reg3] %= (MAX_REG+1)

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def div(self, command):
        # removing filler bits
        command = command[5:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # quotient
        self.regs["000"] = self.regs[command[:3]] // self.regs[command[3:]]
        # remainder
        self.regs["001"] = self.regs[command[:3]] % self.regs[command[3:]]

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def rs(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[:3]] = self.regs[command[:3]] >> int(command[3:], 2)

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def ls(self, command):
        # Clearing the flag
        self.regsObj.clearFlag()

        self.regs[command[:3]] = self.regs[command[:3]] << int(command[3:], 2)

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def xor(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] ^ \
            self.regs[command[3:6]]

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def orOps(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] | \
            self.regs[command[3:6]]

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def andOps(self, command):
        # removing filler bits
        command = command[2:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        reg3 = command[6:]
        self.regs[reg3] = self.regs[command[:3]] & \
            self.regs[command[3:6]]

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def notOps(self, command):
        # removing filler bits
        command = command[5:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # Doing the operation
        num = self.regsObj.convBin16(self.regs[command[:3]])

        invert = ["1" if i == "0" else "0" for i in num]
        self.regs[command[3:]] = int("".join(invert), 2)

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def cmp(self, command):
        # removing filler bits
        command = command[5:]

        # Setting FLAGS
        if self.regs[command[:3]] == self.regs[command[3:]]:
            self.regsObj.setEqual()
        elif self.regs[command[:3]] > self.regs[command[3:]]:
            self.regsObj.setGreater()
        elif self.regs[command[:3]] < self.regs[command[3:]]:
            self.regsObj.setLess()

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] += 1

    def jmp(self, command):
        # removing filler bits
        command = command[3:]

        # Clearing the flag
        self.regsObj.clearFlag()

        # printing the object
        print(self.regsObj)

        # Setting the program counter
        self.regs["PC"] = int(command, 2)

    def jlt(self, command):
        # removing filler bits
        command = command[3:]

        FLAGS = self.regs["111"]

        # Clearing the flag
        self.regsObj.clearFlag()

        # printing the object
        print(self.regsObj)

        # Checking flag
        # Setting the program counter
        if FLAGS[-3] == "1":
            self.regs["PC"] = int(command, 2)
        else:
            self.regs["PC"] += 1

    def jgt(self, command):
        # removing filler bits
        command = command[3:]

        FLAGS = self.regs["111"]

        # Clearing the flag
        self.regsObj.clearFlag()

        # printing the object
        print(self.regsObj)

        # Checking flag
        # Setting the program counter
        if FLAGS[-2] == "1":
            self.regs["PC"] = int(command, 2)
        else:
            self.regs["PC"] += 1

    def je(self, command):
        # removing filler bits
        command = command[3:]

        FLAGS = self.regs["111"]

        # Clearing the flag
        self.regsObj.clearFlag()

        # printing the object
        print(self.regsObj)

        # Checking flag
        # Setting the program counter
        if FLAGS[-1] == "1":
            self.regs["PC"] = int(command, 2)
        else:
            self.regs["PC"] += 1

    def hlt(self, command):
        global showPlt
        global lines

        # Clearing the flag
        self.regsObj.clearFlag()

        # printing the object
        print(self.regsObj)

        for i in range(256):
            if i < len(lines):
                print(lines[i])

            elif i in memAddress:
                binNum = bin(memAddress[i])[2:]
                print("0" * (16 - len(binNum)) + binNum)
            else:
                print("0" * 16)

        showPlt = True


############# Main Function #############
if __name__ == "__main__":
    ######## getting input ########
    lines = [i.strip() for i in sys.stdin.readlines()]

    while lines[-1] == "":
        lines.pop()

    ######## Creating Objects ########
    # registers
    regs = registers()

    # operations
    ops = operation(regs)

    while not showPlt:
        xPC.append((xPC[-1] + 1) if (len(xPC) > 0) else 1)
        yPC.append(regs.regs["PC"])
        ops.opcodes[lines[regs.regs["PC"]][:5]](lines[regs.regs["PC"]][5:])

    #### PLotting the graph ####
    # Setting the graph size
    plt.figure(figsize=(10, 7))

    plt.scatter(xPC, yPC, label="PC")
    plt.scatter(x, y, label="Variables")

    plt.xticks(xPC)
    # plt.yticks([i for i in range(257)])
    if len(y) != 0:
        plt.yticks([i for i in range(max(max(y), max(yPC)) + 1)])
    else:
        plt.yticks([i for i in range(max(yPC) + 1)])
    plt.yticks([i for i in range(max(max(y), max(yPC)) + 1)])

    plt.xlabel("Cycle Number")
    plt.ylabel("Memory Address")

    plt.legend()
    plt.show()
