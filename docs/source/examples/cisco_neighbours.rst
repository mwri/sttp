
Cisco "show neighbors" example
==============================

Here the Cisco IOS-XR output from the "show neighbors" command is:

::

   Sat Oct  6 09:34:54.543 UTC

   IS-IS WIBBLE neighbors:
   System Id      Interface        SNPA           State Holdtime Type IETF-NSF
   wibble.dedee   BE123            *PtoP*         Up    11       L2   Capable 
   dibble.sibble  BE45             *PtoP*         Up    22       L2   Capable 
   whoopy.ticker  BE6              *PtoP*         Up    33       L2   Capable 
   do0.ripper     BE7              *PtoP*         Up    44       L2   Capable 
   dd1.ticker     BE8              *PtoP*         Up    55       L2   Capable 
   dd1.simple     BE9              *PtoP*         Up    66       L2   Capable 
   do0.wimple     Gi333            *PtoP*         Up    77       L2   Capable 
   do0.widget     TenGi444         *PtoP*         Up    88       L2   Capable 

   Total neighbor count: 8

This is parsed with this template:

::

   m> {{ cisco_iosxr_cmd_dt }}
   m> 
   m> IS-IS WIBBLE neighbors:
   m> System Id      Interface        SNPA           State Holdtime Type IETF-NSF
   m*(neighbours)> {{ system_id = fixedwidth(15) }}{{ interface = fixedwidth(17) }}{{ fixedwidth(15) }}{{ state = fixedwidth(6) }}{{ holdtime = fixedwidth(9) }}{{ type = fixedwidth(5) }}{{ ietf_nsf = fixedwidth(8) }}
   m> 
   m> Total neighbor count: {{ total = integer }}

Here's the working example:

   >>> import sttp
   >>>
   >>> in_template = '''m> {{ cisco_iosxr_cmd_dt }}
   ... m> 
   ... m> IS-IS WIBBLE neighbors:
   ... m> System Id      Interface        SNPA           State Holdtime Type IETF-NSF
   ... m*(neighbours)> {{ system_id = fixedwidth(15) }}{{ interface = fixedwidth(17) }}{{ fixedwidth(15) }}{{ state = fixedwidth(6) }}{{ holdtime = fixedwidth(9) }}{{ type = fixedwidth(5) }}{{ ietf_nsf = fixedwidth(8) }}
   ... m> 
   ... m> Total neighbor count: {{ total = integer }}
   ... '''
   >>>
   >>> in_text = '''Sat Oct  6 09:34:54.543 UTC
   ... 
   ... IS-IS WIBBLE neighbors:
   ... System Id      Interface        SNPA           State Holdtime Type IETF-NSF
   ... wibble.dedee   BE123            *PtoP*         Up    11       L2   Capable 
   ... dibble.sibble  BE45             *PtoP*         Up    22       L2   Capable 
   ... whoopy.ticker  BE6              *PtoP*         Up    33       L2   Capable 
   ... do0.ripper     BE7              *PtoP*         Up    44       L2   Capable 
   ... dd1.ticker     BE8              *PtoP*         Up    55       L2   Capable 
   ... dd1.simple     BE9              *PtoP*         Up    66       L2   Capable 
   ... do0.wimple     Gi333            *PtoP*         Up    77       L2   Capable 
   ... do0.widget     TenGi444         *PtoP*         Up    88       L2   Capable 
   ... 
   ... Total neighbor count: 8
   ... '''
   >>>
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>>
   >>> assert out_struct == {
   ...     'total': 8,
   ...     'neighbours': [
   ...         {'system_id': 'wibble.dedee',
   ...             'interface': 'BE123',
   ...             'state': 'Up', 'holdtime': '11',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'dibble.sibble',
   ...             'interface': 'BE45',
   ...             'state': 'Up', 'holdtime': '22',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'whoopy.ticker',
   ...             'interface': 'BE6',
   ...             'state': 'Up', 'holdtime': '33',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'do0.ripper',
   ...             'interface': 'BE7',
   ...             'state': 'Up', 'holdtime': '44',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'dd1.ticker',
   ...             'interface': 'BE8',
   ...             'state': 'Up', 'holdtime': '55',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'dd1.simple',
   ...             'interface': 'BE9',
   ...             'state': 'Up', 'holdtime': '66',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'do0.wimple',
   ...             'interface': 'Gi333',
   ...             'state': 'Up', 'holdtime': '77',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...         {'system_id': 'do0.widget',
   ...             'interface': 'TenGi444',
   ...             'state': 'Up', 'holdtime': '88',
   ...             'type': 'L2', 'ietf_nsf': 'Capable'},
   ...     ]
   ... }
