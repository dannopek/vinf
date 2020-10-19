#!/usr/bin/python3

import sys
import re

apache_access_log_pattern = '^(\S+) - (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+) "(\S+)" "(\S+)" (\S+) "(\S+)" "(\S+)"? (\S+)ms'

for line in sys.stdin:
    match = re.search(apache_access_log_pattern, line)
    
    if not match:
        continue

    curLog = {
        'host': match.group(1),
        'client_user_name_if_available': match.group(2),
        'date_time': match.group(3),
        'method': match.group(4),
        'request_path': match.group(5),
        'protocol': match.group(6),
        'response_code': match.group(7),
        'content_size': match.group(8),
        'request_referrer': match.group(9), # always -
        'request_user_agent': match.group(10), # always -
        'number_of_requests_received_since_started': match.group(11),
        'router_name': match.group(12),
        'server_url': match.group(13),
        'request_duration': match.group(14),
    }

    # print(line)
    print(curLog)
