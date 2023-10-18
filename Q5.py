import math
from os import cpu_count

memsizes = {"B": 8, "kB": 8*2**10, "MB": 8*2**20, "GB": 8*2**30,
            "b": 1, "kb": 2**10, "Mb": 2**20, "Gb": 2**30,
            "byte": 8, "nibble": 4, "bit": 1}

val, b = input("Enter memory storage (like 16 MB): ").split()
addressable = input("What type of addressable mem is being used: ")

option = input('''Choose one of the following
a. Query related to ISA
b. Query related to system enhancements
Enter your choice here : ''')


###### Query related to ISA ######
if option.lower() == "a":
    intlen = int(input("Enter instruction length [bits]: "))
    reglen = int(input("Enter register length [bits]: "))
    if addressable.lower() == "word":
        processor = int(input("Enter the bits in CPU: "))
        memory = int(val)*memsizes[b]/processor
    else:
        memory = int(val)*memsizes[b]/memsizes[addressable.lower()]

    memorysize = int(math.log(memory, 2))
    opbit = intlen - reglen - memorysize
    filbit = intlen - 2*reglen - opbit
    maxin = 2**opbit
    maxreg = 2**reglen
    print(f'''
    bits required for opcode                     |{opbit}
    filler bits in instruction type 2            |{filbit}
    max number of supported instructions by ISA  |{maxin}
    max number of registers supported by ISA     |{maxreg}''')


###### Query related to System enhancement ######
elif option.lower() == 'b':
    type = int(input("Choose query type (1/2): "))
    if type == 1:
        cpubit = int(input("Enter the number of bits in CPU: "))
        change = input("Change type of memory addressable: ")
        dict = {"bit": 1, "nibble": 4, "byte": 8, "word": cpubit}
        addr = int(val)*memsizes[b]/dict[addressable.lower()]
        addrpins = int(math.log(addr, 2))
        newaddr = int(val)*memsizes[b]/dict[change.lower()]
        newpins = int(math.log(newaddr, 2))
        saved = newpins - addrpins
        print(f'number of pins saved: {saved}')
    elif type == 2:
        cpubit = int(input("Enter the number of bits in CPU: "))
        addrpins = int(input("Enter the number of pins: "))
        typemem = input("Enter the addressable memory type: ")
        dict = {"bit": 1, "nibble": 4, "byte": 8, "word": cpubit}
        byteval = {0: "B", 1: "KB", 2: "MB", 3: "GB"}
        membit = 2**addrpins*dict[typemem.lower()]/8
        mem2 = int(math.log(membit, 2))
        value = 2**(mem2 % 10)
        print("Total Storage:", value, byteval[mem2//10])
    else:
        print("invalid choice")
else:
    print("invalid choice")
