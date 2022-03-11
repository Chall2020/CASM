; This is a program that prints "hello" using ASCII codes, waits 1 second, then ends.

; start will be called at the top of the .code section
def start
clear
mov dx "Hello"
mov ah dx
outc

call wait_1_sec
clear

mov dx 0x00
call loop
end

def loop
inc dx
out

cmp dx 0x05
ce loop_done
cne loop
end

def loop_done
wait_1_sec
end

; wait_1_sec will pause the CPU for 1 second.
def wait_1_sec
wait 0x3E8
end

; Marks the top of the .code section, this signifies the start of the main code.
section .code

call start
