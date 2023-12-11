// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(READ)
    @SCREEN
    D=A
    @addr
    M=D    // addr = SCREEN
    @24575
    D=A
    @final_addr
    M=D    // final_addr = 24575

    @KBD
    D=M    // keyboard value
    @WHITE
    D;JEQ    // if keyboard == 0 goto WHITE
    @BLACK
    0;JMP    // else goto BLACK

(WHITE)
    @addr
    A=M
    D=M
    @READ
    D;JEQ    // if RAM[addr] == 0, means screen is already white goto READ

    @final_addr
    D=M
    @addr
    D=D-M
    
    @READ
    D;JEQ    // if final_addr - addr == 0 goto READ

    @addr
    A=M
    M=0    // RAM[addr] = 0

    @addr
    M=M+1    // addr += 1

    @WHITE
    0;JMP


(BLACK)
    @addr
    A=M
    D=M
    @READ
    D;JLT    // if RAM[addr] < 0, means screen is already black goto READ

    @final_addr
    D=M
    @addr
    D=D-M
    
    @READ
    D;JEQ    // if final_addr - addr == 0 goto READ

    @addr
    A=M
    M=-1    // RAM[addr] = -1

    @addr
    M=M+1    // addr += 1

    @BLACK
    0;JMP
