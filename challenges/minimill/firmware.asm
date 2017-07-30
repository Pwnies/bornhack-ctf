label entry
    const main
    relpc 2
    jmp %1
    halt 1


# belt [ret, char]
label putchar
    const 0xff02
    sw %0, %2
    jmp %1


# belt [ret]
label getchar
    const 0xff00
    lw %0
    jmp %2


# belt [ret, ptr]
label puts
    adjsp 6
    sw.sp 0, %0
    sw.sp 2, %1
    sw.sp 4, %2

    label puts_loop
        lw.sp 4
        addi %0, 1
        sw.sp 4, %0
        lb %1
        equi %0, 0
        const puts_out
        const puts_putchar
        mux %2, %1, %0
        jmp %0

    label puts_putchar
        const putchar
        or %5, %5
        const puts_loop
        jmp %2

    label puts_out

    const putchar
    const 0x0a
    relpc 2
    jmp %2
    
    lw.sp 2
    lw.sp 0
    setsp %0
    jmp %1 


label gets
    adjsp 6
    sw.sp 0, %0
    sw.sp 2, %1
    sw.sp 4, %2

    label gets_loop
        const getchar
        relpc 2
        jmp $1
        equi $0, 10
        const gets_out
        relpc 4
        mux $2, $1, $0
        jmp $0
        lw.sp 4
        sb $0, %5
        addi $0, 1
        sw.sp 4, $0
        const gets_loop
        jmp %0

    label gets_out
    lw.sp 4
    const 0
    sb $1, $0
    
    lw.sp 2
    lw.sp 0
    setsp %0
    jmp %1 


# belt [ret, ptr, size]
label crypto
    adjsp 12
    sw.sp 0, %0
    sw.sp 2, %1

    sw.sp 4, %2
    sw.sp 6, %3

    const 0x4123
    sw.sp 8, %0
    const 0x5533
    sw.sp 10, %0

    label crypto_loop
        # if(size == 0) goto crypto_out
        lw.sp 6
        subi %0, 1
        sw.sp 6, %0
        equi %1, 0
        const crypto_out
        relpc 4
        mux %2, %1, %0
        jmp %0

        lw.sp 10
        lw.sp 8
        lw.sp 4
        addi %0, 1
        sw.sp 4, %0
        lb %1
        # belt [pt_byte, ptr+1, ptr, x, y]
        xor %0, %4
        add %0, %4
        # belt [ct_byte, _, pt_byte, ptr+1, ptr]
        sb %4, %0

        lw.sp 8
        roli %0, 1
        sw.sp 8, %0
        
        lw.sp 10
        rori %0, 7
        add %0, %3
        xor %0, %3
        sw.sp 10, %0

        const crypto_loop
        jmp %0
        
    label crypto_out
    lw.sp 2
    lw.sp 0
    setsp %0
    jmp %1

# belt [ptr]
label strlen
    adjsp 8
    sw.sp 0, %0
    sw.sp 2, %1
    sw.sp 4, %2
    const 0
    sw.sp 6, %0

    label strlen_loop
        lw.sp 4
        addi $0, 1
        sw.sp 4, $0
        lb $1
        equi $0, 0
        const strlen_out
        relpc 4
        mux $2, $1, $0
        jmp $0
        lw.sp 6
        addi $0, 1
        sw.sp 6, $0
        const strlen_loop
        jmp $0
    
    label strlen_out
    lw.sp 6
    lw.sp 2
    lw.sp 0
    setsp %0
    or $2, $2
    jmp %2


# belt [ret, ptr1, ptr2, size]
label memcmp
    adjsp 12
    sw.sp 0, %0
    sw.sp 2, %1

    sw.sp 4, %2
    sw.sp 6, %3
    sw.sp 8, %4

    const 0
    sw.sp 10, $0
    
    label memcmp_loop
        lw.sp 8
        subi $0, 1
        sw.sp 8, $0
        equi $1, 0
        const memcmp_out
        relpc 4
        mux $2, $1, $0
        jmp $0
        
        lw.sp 4
        addi $0, 1
        sw.sp 4, $0

        lw.sp 6
        addi $0, 1
        sw.sp 6, $0

        lb $3
        lb $2
        xor $0, $1
        
        lw.sp 10
        or $0, $1
        sw.sp 10, $0

        const memcmp_loop
        jmp $0
        
    label memcmp_out
    lw.sp 10

    lw.sp 2
    lw.sp 0
    setsp %0
    neqi $2, 0
    jmp %2


# belt [ret]
label main
    adjsp 6
    sw.sp 0, %0
    sw.sp 2, %1

    const puts
    const input_flag
    relpc 2
    jmp %2

    const gets
    const 0x1000
    relpc 2
    jmp %2

    const strlen
    const 0x1000
    relpc 2
    jmp %2

    addi $0, 1

    sw.sp 4, %0

    const crypto
    lw.sp 4
    const 0x1000
    relpc 2
    jmp %3

    const memcmp
    lw.sp 4
    const 0x1000
    const flag_data
    relpc 2
    jmp $4

    equi $0, 0
    const good_flag
    const bad_flag
    mux $2, $1, $0
    
    const puts
    or $1, $1
    relpc 2
    jmp $2
    
    lw.sp 2
    lw.sp 0
    setsp %0
    jmp %1 

label input_flag
    data 73, 110, 112, 117, 116, 32, 102, 108, 97, 103, 58, 0

label good_flag
    data 70, 108, 97, 103, 32, 105, 115, 32, 103, 111, 111, 100, 0

label bad_flag
    data 70, 108, 97, 103, 32, 105, 115, 32, 98, 97, 100, 0

label flag_data
