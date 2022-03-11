CASM Assembler v1.0.0 By Cory Hall

CASM is a prototype assembler made in Python.

`example.asm` is an example program that prints "HELLO" to the screen, waits 1 second, then ends.

To run a program, run the `main.py` file, then type the program path.

eg: to run example.asm, type `example.asm`

REGISTERS:
    
    EAX - Accumilator Registers
        AX - General Purpose Register
        AL - General Purpose Register
        AH - Used for output in arithmetic instructions (ADD, SUB, DIV, MUL)

    EDX - Data Registers
        DX - Used for storing data to be used in OUT or OUTC
        DL - General Purpose Data Register
        DH - General Purpose Data Register

SYNTAX:
    
    To set a variable:

    <label> equ <value>

    To set a process: 
    
    _label
    <code>
    end

    section .code               - Marks the start of the executable code. Processes should be created BEFORE this line.
    
    call <label>                - Calls the specified process

    add <operand_1> <operand_2> - Adds the specified operands

    sub <operand_1> <operand_2> - Subtracts the specified operands

    div <operand_1> <operand_2> - Divides the specified operands

    mul <operand_1> <operand_2> - Multiplies the specified operands

    mov <destination> <source>  - Move the value of <source> into <destination>

    push <register/variable>    - Store the value of the specified register/variable in the stack.

    pop <register/variable>     - Set the value of the specified register/variable to what is stored in the stack.

    in                          - Get user input and store it to the EDX register

    out                         - Output the hex value of the EDX register

    outc                        - Output the ASCII character stored in EDX (eg: 0x48 = "H")

    end                         - Ends the process it is in.