FROM debian

RUN dpkg --add-architecture mips
RUN apt-get update
RUN apt-get install -qy busybox-static:mips qemu-user-static socat

RUN mkdir -p /chroot/bin
RUN mkdir -p /chroot/usr/bin

RUN busybox --install /chroot/bin
RUN cp /usr/bin/qemu-mips-static /chroot/usr/bin/qemu-mips-static

ENV USER mips
ENV PORT 1337

RUN useradd $USER

COPY enter-chroot /
COPY run /
COPY start /chroot
COPY firstmips /chroot

CMD ["/run", "/enter-chroot"]
