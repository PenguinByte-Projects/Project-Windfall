.section .data
msg:
    .asciz "hello, world!\n"

.section .text
.globl _start

_start:
loop:
    movl $4, %eax
    movl $1, %ebx
    movl $msg, %ecx
    movl $14, %edx
    int $0x80
    jmp loop
