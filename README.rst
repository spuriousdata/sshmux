=========
sshmux
=========

Multiplex output from various ssh commands

------
example
------

sshmux.py host1 "tail -f /var/log/messages" host2 "tail -f /var/log/messages" host3 "tail -f /var/log/messages"


