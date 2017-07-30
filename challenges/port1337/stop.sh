#!/bin/sh
kill $(cat .flag_server_pid)
kill $(cat .troll_server_pid)
rm .flag_server_pid
rm .troll_server_pid
