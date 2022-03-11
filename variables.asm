section .code

clear

; VARIABLES
var equ 0x44
var2 equ 0x20

; Moving variables into registers in order to perform arithmetic processes
mov ax var
mov al var2

; Add the two variables
add ax al

; Move the sum of var + var2 into the dx register for output.
mov dx ah

; Outputs the sum of var + var2
out
