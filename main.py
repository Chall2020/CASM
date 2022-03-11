import os
import time

global stack
global reg
global var
global labels
global flag

stack = {"eax": 0, "ax": 0, "al": 0, "ah": 0, "edx": 0, "dx": 0, "dh": 0, "dl": 0}
reg = {"eax": 0, "ax": 0, "al": 0, "ah": 0, "edx": 0, "dx": 0, "dh": 0, "dl": 0}

flag = 1
labels = {}
stack_var = {}
var = {}

def isreg(string):
    global reg

    if string in reg:
        return True
    else:
        return False


def isvar(string):
    global var

    if string in var:
        return True
    else:
        return False


def parse(cmd):
    global reg
    global stack
    global var
    global flag

    args = cmd.lower().split(" ")

    if args[0] == "ce":
        if flag:
            parse(f"call {args[1]}")
            return

    elif args[0] == "cne":
        if not flag:
            parse(f"call {args[1]}")
            return

    elif args[0] == "cmp":
        if isreg(args[1]):
            if isreg(args[2]):
                flag = (reg.get(args[1]) == reg.get(args[2]))
            elif isvar(args[2]):
                flag = (reg.get(args[1]) == var.get(args[2]))
            else:
                flag = (reg.get(args[1]) == hex(int(args[2], 16)))
        elif isvar(args[1]):
            if isreg(args[2]):
                flag = (var.get(args[1]) == reg.get(args[2]))
            elif isvar(args[2]):
                flag = (var.get(args[1]) == var.get(args[2]))
            else:
                flag = (var.get(args[1]) == hex(int(args[2], 16)))
        else:
            if isreg(args[2]):
                flag = (hex(int(args[1], 16)) == reg.get(args[2]))
            elif isvar(args[2]):
                flag = (hex(int(args[1], 16)) == var.get(args[2]))
            else:
                flag = (hex(int(args[1], 16)) == hex(int(args[2], 16)))


    elif args[0] == "call":
        label = labels.get(args[1])

        try:
            for i in range(0, len(label)):
                parse(label[i])
        except RecursionError:
            return

    elif args[0].startswith(";"):
        return

    elif args[0] == "inc":
        if isreg(args[1]):
            reg[args[1]] = hex(int(reg.get(args[1]), 16) + 1)
        elif isvar(args[1]):
            var[args[1]] = hex(int(var.get(args[1]), 16) + 1)

    elif args[0] == "dec":
        if isreg(args[1]):
            reg[args[1]] = hex(int(reg.get(args[1]), 16) - 1)
        elif isvar(args[1]):
            var[args[1]] = hex(int(var.get(args[1]), 16) - 1)

    elif args[0] == "push":
        if isreg(args[1]):
            stack[args[1]] = reg.get(args[1])
            reg[args[1]] = 0
        elif isvar(args[1]):
            stack_var[args[1]] = var.get(args[1])
            var[args[0]] = 0

    elif args[0] == "pop":
        if isreg(args[1]):
            reg[args[1]] = stack.get(args[1])
            stack[args[1]] = 0
        elif isvar(args[1]):
            var[args[1]] = stack_var.get(args[1])
            stack_var[args[1]] = 0

    elif args[0] == "mov":
        chars = list(args[2])

        if isreg(args[1]):
            if isreg(args[2]):
                reg[args[1]] = reg.get(args[2])
            elif isvar(args[2]):
                reg[args[1]] = var.get(args[2])
            else:
                try:
                    reg[args[1]] = hex(int(args[2], 16))
                except ValueError:
                    word = args[2][1:]
                    reg[args[1]] = [hex(ord(character)) for character in word[:-1]]
        elif isvar(args[1]):
            if isreg(args[2]):
                var[args[1]] = reg.get(args[2])
            elif isvar(args[2]):
                var[args[1]] = var.get(args[2])
            else:
                try:
                    var[args[1]] = hex(int(args[2], 16))
                except ValueError:
                    word = args[2][1:]
                    var[args[1]] = [hex(ord(character)) for character in word[:-1]]
        else:
            print(f"{args[1]} is not a valid register or variable.")

    elif args[0] == "out":
        print(reg.get("dx"))
    elif args[0] == "outc":
        char = reg.get("dx")

        if isinstance(char, list):
            for i in range(0, len(char)):
                temp = char[i]
                temp = temp[2:]
                temp = bytes.fromhex(temp)
                temp = temp.decode("ASCII")
                print(temp, end="")
            print()
        else:
            temp = char[2:]
            temp = bytes.fromhex(temp)
            temp = temp.decode("ASCII")
            print(temp)


    elif args[0] == "in":
        input_given = input("IN: ")
        reg["dx"] = [hex(ord(character)) for character in input_given]

    elif args[0] == "add":
        if isreg(args[1]) and isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) + int(reg.get(args[2]), 16))
        elif isreg(args[1]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) + int(args[2], 16))
        elif isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[2]), 16) + int(args[1], 16))
        else:
            reg["ah"] = hex(int(args[1], 16) + int(args[2], 16))

    elif args[0] == "sub":
        if isreg(args[1]) and isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) - int(reg.get(args[2]), 16))
        elif isreg(args[1]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) - int(args[2], 16))
        elif isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[2]), 16) - int(args[1], 16))
        else:
            reg["ah"] = hex(int(args[1], 16) - int(args[2], 16))

    elif args[0] == "div":
        if isreg(args[1]) and isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) // int(reg.get(args[2]), 16))
        elif isreg(args[1]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) // int(args[2], 16))
        elif isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[2]), 16) // int(args[1], 16))
        else:
            reg["ah"] = hex(int(args[1], 16) // int(args[2], 16))

    elif args[0] == "mul":
        if isreg(args[1]) and isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) * int(reg.get(args[2]), 16))
        elif isreg(args[1]):
            reg["ah"] = hex(int(reg.get(args[1]), 16) * int(args[2], 16))
        elif isreg(args[2]):
            reg["ah"] = hex(int(reg.get(args[2]), 16) * int(args[1], 16))
        else:
            reg["ah"] = hex(int(args[1], 16) * int(args[2], 16))

    elif args[0] == "cls" or args[0] == "clear":
        os.system('clear')

    elif args[0] == "wait":
        time.sleep(int(args[1], 16)/1000)

    else:
        if len(args) < 2:
            return

        if args[1] == "equ":
            if isreg(args[2]):
                var[args[0]] = reg.get(args[2])
            elif isvar(args[2]):
                var[args[0]] = var.get(args[2])
            else:
                try:
                    var[args[0]] = hex(int(args[2], 16))
                except ValueError:
                    var[args[0]] = [hex(ord(character)) for character in args[2]]

        else:
            print(f"'{args[0]}' is not a recognised instruction.")
            return

def get_lines(lines, i):
    to_return = []
    for x in range(i+1, len(lines)):
        if lines[x].startswith("end"):
            return to_return
        else:
            to_return.append(lines[x])


os.system("clear")

while True:
    start_flag = False
    to_do = input("File to open (Type @q to quit): ")

    if to_do == "@q":
        break

    file = open(to_do, "r")

    lines = []

    for line in file:
        lines.append(line)

    temp = "".join(lines)
    lines = temp.split("\n")

    print()

    for i in range(len(lines)):
        if not lines[i].startswith("def "):
            if not start_flag:
                args = lines[i].split(" ")
                if args[0] == "section" and args[1] == ".code":
                    start_flag = True
                    continue
                else:
                    continue

            parse(lines[i])
        else:
            lines[i] = lines[i][4:]
            labels[lines[i]] = get_lines(lines, i)
            i += len(labels.get(lines[i]))

    print()

os.system("clear")
