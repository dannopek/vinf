#!/usr/bin/python3

import sys
import json
import re
import socket, time
from io import BytesIO
# import geoip2.database as geoip

apache_access_log_pattern = '^(\S+) - (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+) "(\S+)" "(\S+)" (\S+) "(\S+)" "(\S+)"? (\S+)ms'
recv_bytes_count = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 1236))
sock.listen(2)
with BytesIO() as buffer:
    while True:
        conn, addr = sock.accept()
        try:
            while True:
                resp = conn.recv(recv_bytes_count)

                buffer.write(resp)
                buffer.seek(0)   
                start_index = 0
                for line in buffer:
                    start_index += len(line)
                    # print(line.decode('utf-8'))
                    match = re.search(apache_access_log_pattern, line.decode('utf-8'))
                    if not match:
                        remaining = line
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
                        'location': False
                    }
                    
                    # location = geo_lookup.city(curLog['host'])
                    # curLog['location'] = location.city.name

                    print(json.dumps(curLog))

                # print(start_index)
                if start_index:
                    buffer.seek(start_index)
                    remaining += buffer.read()
                    buffer.truncate(0)
                    buffer.seek(0)
                    buffer.write(remaining)
                    remaing = ''
                else:
                    buffer.seek(0, 2)
                
                if start_index < recv_bytes_count:
                    break
        except:
            print('fck')
            
        conn.close()
