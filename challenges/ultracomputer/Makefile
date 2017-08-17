TARGET := a.out

all: $(TARGET)

$(TARGET): main.c magic.c
	gcc -o $@ $^  -fno-common -fno-zero-initialized-in-bss
	strip -w -s -K fini -K f[0-9]* $@
	python obfu.py

.PHONY: clean
clean:
	rm -f $(TARGET)
