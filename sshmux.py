import sys
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue


def enqueue(host, fh, q):
    for line in iter(fh.readline, b''):
        q.put(f"{host}: {line.decode('utf8')}")
    fh.close()


def main():
    if ((len(sys.argv) - 1) % 2) != 0:
        print(f"Usage: {sys.argv[0]} HOST CMD [HOST CMD [HOST CMD [HOST CMD]]...]")
        return 1
    qs = []
    for host, cmd in zip(sys.argv[1::2], sys.argv[2::2]):
        cmd = f'ssh {host} "{cmd}"'
        sys.stderr.write(f"Running: {cmd}\n")
        sys.stderr.flush()
        p = Popen(cmd, shell=True, stdout=PIPE, bufsize=1)
        q = Queue()
        qs.append(q)
        t = Thread(target=enqueue, args=(host, p.stdout, q), daemon=True)
        t.start()

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

