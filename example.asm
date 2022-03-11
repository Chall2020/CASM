; This is a program that prints "hello" using ASCII codes, waits 1 second, then ends.

; start will be called at the top of the .code section
start:
    mov dx "Hello"
    mov ah dx
    outc

    call wait_1_sec

    mov dx 0x00
    call loop
    ret

loop:
    inc dx
    out

    cmp dx 0x05
    ce loop_done
    cne loop
    ret

loop_done:
    wait_1_sec
    ret

; wait_1_sec will pause the CPU for 1 second.
wait_1_sec:
    wait 0x3E8
    ret

; Marks the top of the .code section, this signifies the start of the main code.
section .code

call start
