SECTIONS
{
        .shellcode (0) : {
                *(.start)
                *(.text)
                *(.text.*)
                *(.data)
                *(.data.*)
                *(.rodata)
                *(.rodata.*)
                *(.bss)
                *(COMMON)
                payload = .;
        }

        .relocations : {
                *(.rela)
                *(.rela.*)
                *(.rel)
                *(.rel.*)
        }

        /DISCARD/ : {
                *(.note)
                *(.reginfo)
                *(.MIPS.abiflags)
                *(.eh_frame)
        }

        ASSERT(!SIZEOF(.relocations), "Cannot create shellcode with relocations")
}
