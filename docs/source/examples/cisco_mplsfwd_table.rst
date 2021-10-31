Cisco MPLS forwarding table example
===================================

Here the Cisco IOS-XR MPLS table output is:

::

   Sat Oct  6 09:34:54.543 UTC
   Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   Label  Label       or ID              Interface                    Switched    
   ------ ----------- ------------------ ------------ --------------- ------------
   123011 123011      Ac accept (im 4)   BE1          10.123.123.1    1234567890  
          123011      Ac accept (im 4)   BE123        10.234.234.22   0            (!)

Here three template examples are illustrated. First a naive version, but this leaves spaces
on the end of hte "prefix_or_id" fields:

::

   m> {{ cisco_iosxr_cmd_dt }}
   m> Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   m> Label  Label       or ID              Interface                    Switched    
   m> ------ ----------- ------------------ ------------ --------------- ------------
   m*> {{ local_label = re("(?:\d+|)") }}{{ ws }}{{ outgoing_label = non_ws }}{{ ws }}{{ prefix_or_id = re(".{18}") }}{{ ws }}{{ outgoing_ifname = non_ws }}{{ ws }}{{ next_hop = ipaddr }}{{ ws }}{{ bytes_switched = integer }}{{ ws }}{{ flags = re("(?:\S+|)") }}

Or, using the fixedwidth function:

::

   m> {{ cisco_iosxr_cmd_dt }}
   m> Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   m> Label  Label       or ID              Interface                    Switched    
   m> ------ ----------- ------------------ ------------ --------------- ------------
   m*> {{ local_label = fixedwidth(6) }}{{ ws }}{{ outgoing_label = fixedwidth(11) }}{{ ws }}{{ prefix_or_id = fixedwidth(18) }}{{ ws }}{{ outgoing_ifname = fixedwidth(12) }}{{ ws }}{{ next_hop = fixedwidth(15) }}{{ ws }}{{ int bytes_switched = fixedwidth(12) }}{{ flags = string | lstrip() }}

Or this would be fixed width column parsing without the fixedwidth column, which leaves a lot of
extra trailing white space on all columns, though you could tidy this up with the lstrip function:

::

   m> {{ cisco_iosxr_cmd_dt }}
   m> Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   m> Label  Label       or ID              Interface                    Switched    
   m> ------ ----------- ------------------ ------------ --------------- ------------
   m*> {{ local_label = re(".{6}") }}{{ ws }}{{ outgoing_label = re(".{11}") }}{{ ws }}{{ prefix_or_id = re(".{18}") }}{{ ws }}{{ outgoing_ifname = re(".{12}") }}{{ ws }}{{ next_hop = re(".{15}") }}{{ ws }}{{ int bytes_switched = re(".{12}") }}{{ flags = string }}

Here's the naive template demonstrated working:

   >>> import sttp
   >>>
   >>> in_template = '''m> {{ cisco_iosxr_cmd_dt }}
   ... m> Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   ... m> Label  Label       or ID              Interface                    Switched    
   ... m> ------ ----------- ------------------ ------------ --------------- ------------
   ... m*> {{ local_label = re("(?:\d+|)") }}{{ ws }}{{ outgoing_label = non_ws }}{{ ws }}{{ prefix_or_id = re(".{18}") }}{{ ws }}{{ outgoing_ifname = non_ws }}{{ ws }}{{ next_hop = ipaddr }}{{ ws }}{{ bytes_switched = integer }}{{ ws }}{{ flags = re("(?:\S+|)") }}
   ... '''
   >>>
   >>> in_text = '''Sat Oct  6 09:34:54.543 UTC
   ... Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   ... Label  Label       or ID              Interface                    Switched    
   ... ------ ----------- ------------------ ------------ --------------- ------------
   ... 123011 123011      Ac accept (im 4)   BE1          10.123.123.1    1234567890  
   ...        123011      Ac accept (im 4)   BE123        10.234.234.22   0            (!)
   ... '''
   >>>
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>>
   >>> assert out_struct == [{
   ...     'local_label':     '123011',
   ...     'outgoing_label':  '123011',
   ...     'prefix_or_id':    'Ac accept (im 4)  ',
   ...     'next_hop':        '10.123.123.1',
   ...     'outgoing_ifname': 'BE1',
   ...     'bytes_switched':  1234567890,
   ...     'flags':           '',
   ... }, {
   ...     'local_label':     '',
   ...     'outgoing_label':  '123011',
   ...     'prefix_or_id':    'Ac accept (im 4)  ',
   ...     'next_hop':        '10.234.234.22',
   ...     'outgoing_ifname': 'BE123',
   ...     'bytes_switched':  0,
   ...     'flags':           '(!)',
   ... }], out_struct


Here's the fixedwidth template demonstrated working:

   >>> import sttp
   >>>
   >>> in_template = '''m> {{ cisco_iosxr_cmd_dt }}
   ... m> Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   ... m> Label  Label       or ID              Interface                    Switched    
   ... m> ------ ----------- ------------------ ------------ --------------- ------------
   ... m*> {{ local_label = fixedwidth(6) }}{{ ws }}{{ outgoing_label = fixedwidth(11) }}{{ ws }}{{ prefix_or_id = fixedwidth(18) }}{{ ws }}{{ outgoing_ifname = fixedwidth(12) }}{{ ws }}{{ next_hop = fixedwidth(15) }}{{ ws }}{{ int bytes_switched = fixedwidth(12) }}{{ flags = string | lstrip() }}
   ... '''
   >>>
   >>> in_text = '''Sat Oct  6 09:34:54.543 UTC
   ... Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   ... Label  Label       or ID              Interface                    Switched    
   ... ------ ----------- ------------------ ------------ --------------- ------------
   ... 123011 123011      Ac accept (im 4)   BE1          10.123.123.1    1234567890  
   ...        123011      Ac accept (im 4)   BE123        10.234.234.22   0            (!)
   ... '''
   >>>
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>>
   >>> assert out_struct == [{
   ...     'local_label':     '123011',
   ...     'outgoing_label':  '123011',
   ...     'prefix_or_id':    'Ac accept (im 4)',
   ...     'next_hop':        '10.123.123.1',
   ...     'outgoing_ifname': 'BE1',
   ...     'bytes_switched':  1234567890,
   ...     'flags':           '',
   ... }, {
   ...     'local_label':     '',
   ...     'outgoing_label':  '123011',
   ...     'prefix_or_id':    'Ac accept (im 4)',
   ...     'next_hop':        '10.234.234.22',
   ...     'outgoing_ifname': 'BE123',
   ...     'bytes_switched':  0,
   ...     'flags':           '(!)',
   ... }], out_struct

Here's the DIY fixed width column template demonstrated working:

   >>> import sttp
   >>>
   >>> in_template = '''m> {{ cisco_iosxr_cmd_dt }}
   ... m> Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   ... m> Label  Label       or ID              Interface                    Switched    
   ... m> ------ ----------- ------------------ ------------ --------------- ------------
   ... m*> {{ local_label = re(".{6}") }}{{ ws }}{{ outgoing_label = re(".{11}") }}{{ ws }}{{ prefix_or_id = re(".{18}") }}{{ ws }}{{ outgoing_ifname = re(".{12}") }}{{ ws }}{{ next_hop = re(".{15}") }}{{ ws }}{{ int bytes_switched = re(".{12}") }}{{ flags = string }}
   ... '''
   >>>
   >>> in_text = '''Sat Oct  6 09:34:54.543 UTC
   ... Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
   ... Label  Label       or ID              Interface                    Switched    
   ... ------ ----------- ------------------ ------------ --------------- ------------
   ... 123011 123011      Ac accept (im 4)   BE1          10.123.123.1    1234567890  
   ...        123011      Ac accept (im 4)   BE123        10.234.234.22   0            (!)
   ... '''
   >>>
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>>
   >>> assert out_struct == [{
   ...     'local_label':     '123011',
   ...     'outgoing_label':  '123011     ',
   ...     'prefix_or_id':    'Ac accept (im 4)  ',
   ...     'next_hop':        '10.123.123.1   ',
   ...     'outgoing_ifname': 'BE1         ',
   ...     'bytes_switched':  1234567890,
   ...     'flags':           '',
   ... }, {
   ...     'local_label':     '      ',
   ...     'outgoing_label':  '123011     ',
   ...     'prefix_or_id':    'Ac accept (im 4)  ',
   ...     'next_hop':        '10.234.234.22  ',
   ...     'outgoing_ifname': 'BE123       ',
   ...     'bytes_switched':  0,
   ...     'flags':           ' (!)',
   ... }], out_struct
