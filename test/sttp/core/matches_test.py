"""Core matches module tests."""

import re
import logging

from sttp import core


logging.getLogger('sttp').setLevel('DEBUG')


def test_ipaddr_re():
    """Validate IP address matching against various valid and invalid addresses."""

    hostname_re = re.compile(f'^{core.matches.IPv4AddrCoreMatch()}$')

    valid = [
        '199.250.10.0',
        '250.250.10.0',
        '250.250.10.1',
        '250.250.10.10',
        '255.250.10.1',
        '8.8.4.4',
    ]

    invalid = [
        '250.350.10.1',
        '250.250.10.1000',
        '250.250.10.010',
        '250.250.10.01',
        '255.250.10.01',
        '256.250.10.1',
        '254.250.256.1',
    ]

    for ip in valid:
        assert hostname_re.match(ip) is not None, ip + ' should be valid'

    for ip in invalid:
        assert hostname_re.match(ip) is None, ip + ' should be invalid'


def test_number_re():
    """Validate number matching against various valid and invalid numbers."""

    number_re = re.compile(f'^{core.matches.NumberCoreMatch()}$')

    valid = [
        '3.1415',
        '1.0',
        '1.1',
        '1',
        '11',
        '001',
    ]

    invalid = [
        '1.1.1',
        '',
        'abc',
        'a',
        '1..1',
    ]

    for num in valid:
        assert number_re.match(num) is not None, num + ' should be valid'

    for num in invalid:
        assert number_re.match(num) is None, num + ' should be invalid'
