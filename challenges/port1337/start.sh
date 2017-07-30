#!/bin/sh
socat sctp-listen:1337,fork exec:"cat flag" &
echo $! > .flag_server_pid
socat tcp-listen:1337,fork exec:"cat tcp" &
echo $! > .troll_server_pid

