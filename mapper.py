#!/usr/bin/env python3

import sys
import re

apache_access_log_pattern = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+)'

data = []
for line in sys.stdin:
    match = re.search(apache_access_log_pattern, line)
    
    if not match:
        continue

    curLog = {
        'host': match.group(1),
        'client_identd': match.group(2),
        'user_id': match.group(3),
        'date_time': match.group(4),
        'method': match.group(5),
        'endpoint': match.group(6),
        'protocol': match.group(7),
        'response_code': match.group(8),
        'content_size': match.group(9)
    }

    data.append(curLog)
    print(curLog)