test_null_mov:
    mov dx 0x00
    cmp dx 0x00

    mov dl "null mov"
    ce test_passed
    cne test_failed
    ret

test_null_cmp:
    cmp 0x00 0x00
    mov dl "null cmp"
    ce test_passed
    cne test_failed
    ret

test_null_var:
    test_var equ 0x00
    mov dl "null var"
    cmp test_var 0x00
    ce test_passed
    cne test_failed
    ret

test_null_stack:
    mov al 0x00
    push al
    pop al
    cmp al 0x00
    mov dl "null stack pointer"
    ce test_passed
    cne test_failed
    ret

test_cmp:
    cmp 0x02 0x02
    mov dl "cmp"
    ce test_passed
    cne test_failed
    ret

test_mov:
    mov al 0x04
    cmp al 0x04
    mov dl "mov"
    ce test_passed
    cne test_failed

test_var:
    test_var equ 0x06
    cmp test_var 0x06
    mov dl "var"
    ce test_passed
    cne test_failed
    ret

test_stack:
    mov al 0x03
    push al
    pop al
    cmp al 0x03
    mov dl "stack"
    ce test_passed
    cne test_failed
    ret

test_passed:
    mov dx "Test passed:"
    outc
    inc bh
    mov dx dl
    outc
    ret

test_failed:
    mov dx "Test failed:"
    outc
    mov dx dl
    outc
    ret

new_line:
    mov dx 0x20
    outc
    ret

test:
    call test_null_cmp
    call new_line
    call test_null_mov
    call new_line
    call test_null_var
    call new_line
    call test_null_stack
    call new_line
    call test_cmp
    call new_line
    call test_mov
    call new_line
    call test_var
    call new_line
    call test_stack
    ret

section .code
clear

mov bh 0x00
call test

call new_line
mov dx "Tests Passed:"
outc
mov dx bh
out