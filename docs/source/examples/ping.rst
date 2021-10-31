Ping
====

Take the the UNIX :code:`ping -c3 dns.google` command, which has output like this:

.. code-block:: text

   PING dns.google (8.8.4.4) 56(84) bytes of data.
   64 bytes from dns.google (8.8.4.4): icmp_seq=1 ttl=54 time=11.7 ms
   64 bytes from dns.google (8.8.4.4): icmp_seq=2 ttl=54 time=12.5 ms
   64 bytes from dns.google (8.8.4.4): icmp_seq=3 ttl=54 time=11.7 ms
   
   --- dns.google ping statistics ---
   3 packets transmitted, 3 received, 0% packet loss, time 2002ms
   rtt min/avg/max/mdev = 11.719/11.973/12.465/0.347 ms

The desired parse result is this:

::

   {
       'ipaddr': '8.8.4.4',
       'target': 'dns.google',
       'replies': [
           {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 1, 'ttl': 54, 'latency': 11.7},
           {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 2, 'ttl': 54, 'latency': 12.5},
           {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 3, 'ttl': 54, 'latency': 11.7},
       ],
       'stats': {
           'transmitted': 3,
           'received': 3,
           'loss': 0,
           'time': 2002.0,
           'min': 11.719,
           'max': 12.465,
           'avg': 11.973,
           'mdev': 0.347,
       },
   }

A template solution is:

.. code-block:: text

   m> PING {{ target = hostname }} ({{ ipaddr = ipaddr }}) {{ integer }}({{ integer }}) bytes of data.
   m*(replies)> {{ len = integer }} bytes from {{ target = hostname }} ({{ ipaddr = ipaddr }}): icmp_seq={{ seq = integer }} ttl={{ ttl = integer }} time={{ latency = number }} ms
   m> 
   m> --- {{ target = hostname }} ping statistics ---
   m> {{ stats.transmitted = integer }} packets transmitted, {{ stats.received = integer }} received, {{ stats.loss = integer }}% packet loss, time {{ stats.time = number }}ms
   m> rtt min/avg/max/mdev = {{ stats.min = number }}/{{ stats.avg = number }}/{{ stats.max = number }}/{{ stats.mdev = number }} ms

In full:

   >>> import sttp
   >>> in_template = '''m> PING {{ target = hostname }} ({{ ipaddr = ipaddr }}) {{ integer }}({{ integer }}) bytes of data.
   ... m*(replies)> {{ len = integer }} bytes from {{ target = hostname }} ({{ ipaddr = ipaddr }}): icmp_seq={{ seq = integer }} ttl={{ ttl = integer }} time={{ latency = number }} ms
   ... m> 
   ... m> --- {{ target = hostname }} ping statistics ---
   ... m> {{ stats.transmitted = integer }} packets transmitted, {{ stats.received = integer }} received, {{ stats.loss = integer }}% packet loss, time {{ stats.time = number }}ms
   ... m> rtt min/avg/max/mdev = {{ stats.min = number }}/{{ stats.avg = number }}/{{ stats.max = number }}/{{ stats.mdev = number }} ms
   ... '''
   >>> in_text = '''PING dns.google (8.8.4.4) 56(84) bytes of data.
   ... 64 bytes from dns.google (8.8.4.4): icmp_seq=1 ttl=54 time=11.7 ms
   ... 64 bytes from dns.google (8.8.4.4): icmp_seq=2 ttl=54 time=12.5 ms
   ... 64 bytes from dns.google (8.8.4.4): icmp_seq=3 ttl=54 time=11.7 ms
   ... 
   ... --- dns.google ping statistics ---
   ... 3 packets transmitted, 3 received, 0% packet loss, time 2002ms
   ... rtt min/avg/max/mdev = 11.719/11.973/12.465/0.347 ms
   ... '''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct == {
   ...     'ipaddr': '8.8.4.4',
   ...     'target': 'dns.google',
   ...     'replies': [
   ...         {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 1, 'ttl': 54, 'latency': 11.7},
   ...         {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 2, 'ttl': 54, 'latency': 12.5},
   ...         {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 3, 'ttl': 54, 'latency': 11.7},
   ...     ],
   ...     'stats': {
   ...         'transmitted': 3,
   ...         'received': 3,
   ...         'loss': 0,
   ...         'time': 2002.0,
   ...         'min': 11.719,
   ...         'max': 12.465,
   ...         'avg': 11.973,
   ...         'mdev': 0.347,
   ...     },
   ... }, out_struct
