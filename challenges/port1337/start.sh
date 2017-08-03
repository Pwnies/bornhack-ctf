#!/bin/sh
socat sctp-listen:1337,fork exec:"cat flag" &
echo $! > .flag_server_pid
ncat -c "cat udp" -k -u -l 1337 &
echo $! > .udp_server_pid
socat tcp-listen:1337,fork exec:"cat tcp" &
echo $! > .tcp_server_pid
