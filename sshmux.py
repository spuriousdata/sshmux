#!/usr/bin/env python3

import sys
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue


def enqueue(host, fh, q):
    for line in iter(fh.readline, b''):
        q.put(f"{host}: {line.decode('utf8')}")
    fh.close()

def run(host, cmd):
    cmd = f'ssh {host} "{cmd}"'
    sys.stderr.write(f"Running: {cmd}\n")
    sys.stderr.flush()
    p = Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
    q = Queue()
    t = Thread(target=enqueue, args=(host, p.stdout, q), daemon=True)
    t.start()
    return q

def main():
    numargs = len(sys.argv)
    if numargs < 3 or ((numargs - 1) % 2) != 0:
        print(f"Usage: {sys.argv[0]} HOST[,HOST[,HOST] CMD [HOST[...] CMD [HOST[...] CMD]...]")
        return 1
    qs = []
    for host, cmd in zip(sys.argv[1::2], sys.argv[2::2]):
        if host.find(',') != -1:
            hosts = host.split(',')
            for h in hosts:
                qs.append(run(h, cmd))
        else:
            qs.append(run(host, cmd))

    while True:
        for q in qs:
            try:
                print(q.get_nowait(), end="")
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                pass


if __name__ == '__main__':
    main()

