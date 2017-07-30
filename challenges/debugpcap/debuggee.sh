#!/bin/sh
gdbserver --once 0.0.0.0:1234 /bin/cat flag
