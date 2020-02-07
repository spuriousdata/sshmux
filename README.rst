=========
sshmux
=========

Multiplex output from various ssh commands

------
example
------

sshmux.py host1,host2,host3 "tail -f /var/log/messages" host4 "tail -f /var/log/syslog"


