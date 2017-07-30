#!/bin/sh

docker build -t debugpcap .

tcpdump -i docker0 'tcp port 1234' -G 5 -w debug.pcap &
docker run --rm -d --name debuggee --cap-add SYS_PTRACE --security-opt seccomp:unconfined debugpcap ./debuggee.sh
docker run --rm --name debugger --link debuggee debugpcap ./debugger.sh
sleep 7
