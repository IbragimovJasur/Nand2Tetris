// Draws line 16-bit wide (column) in n (R0) rows start from 0
// Set value to R0 before using.
// Ex. R0=50, program draws 16-bit wide line to first 50 rows


@R0
D=M
@n
M=D    // n = RO

@SCREEN
D=A
@addr    // pointer
M=D    // addr = screen (16384 - screen's base address in RAM)


(LOOP)
    @n
    D=M
    @END
    D;JLE    // if n<=0 goto END

    // set address to addr pointer value
    // then RAM[addr] is automatical selected because A=addr
    // therefore we can set RAM[addr] to -1
    @addr
    A=M
    M=-1    // RAM[addr] = -1

    @32
    D=A
    @addr
    M=M+D    // addr = addr + 32
    @n
    M=M-1

    @LOOP
    0;JMP


(END)
    @END
    0;JMP
