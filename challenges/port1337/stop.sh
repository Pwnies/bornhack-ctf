#!/bin/sh
kill $(cat .flag_server_pid)
kill $(cat .tcp_server_pid)
kill $(cat .udp_server_pid)
rm .flag_server_pid
rm .tcp_server_pid
rm .udp_server_pid
