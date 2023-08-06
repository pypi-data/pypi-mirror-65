Python 3 Migration Issues with Foolscap
=======================================

flogtool dump
-------------

Foolscap log events can contain arbitrary JSON-serializable properties. These
are stored in memory, retrieved from a "logport", delivered automatically to
a "gatherer", and written to disk in "flogfiles". A live application's log
events can be followed and displayed by "flogtool tail", which can also write
them to a flogfile. Flogfiles can be displayed to stdout with "flogtool
dump", or can be viewed in a web browser with "flogtool web-viewer".

"flogtool dump" renders event properties with "print". JSON deserialization
yields unicode property names and values. As a result, running dump under py2
causes dictionary events to be displayed with extra ``u''`` prefixes:

    v5ztk3fw#189 23:55:47.648: get_stats() -> {u'stats': {u'cpu_monitor.total': 0.6067410000000001, u'node.uptime': 167.47867012023926, u'cpu_monitor.1min_avg': 0.0007499415462132355}, u'counters': {u'downloader.bytes_downloaded': 47405, u'mutable.files_retrieved': 1, u'downloader.files_downloaded': 1, u'mutable.bytes_retrieved': 262}}

Running "flogtool dump" under py3 does not show these prefixes:

    v5ztk3fw#189 23:55:47.648: get_stats() -> {'stats': {'cpu_monitor.total': 0.6067410000000001, 'node.uptime': 167.47867012023926, 'cpu_monitor.1min_avg': 0.0007499415462132355}, 'counters': {'downloader.bytes_downloaded': 47405, 'mutable.files_retrieved': 1, 'downloader.files_downloaded': 1, 'mutable.bytes_retrieved': 262}}

flogtool tail
-------------

"flogtool tail" receives the event dictionaries without first saving them as
JSON. tail under py27 does not show these prefixes.

TODO: "flogtool tail" (under py3) cannot connect to a py27 tahoe node
(running either old or new foolscap).

* `flogtool dump` under py27 now shows
