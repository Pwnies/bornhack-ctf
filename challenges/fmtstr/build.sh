#!/bin/sh
gcc -O3 -pie -fPIC fmtstr.c -o fmtstr
docker build -t fmtstr .
