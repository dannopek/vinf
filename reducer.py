#!/usr/bin/env python3

import sys

for line in sys.stdin:
    print(line, end = '')


# hadoop jar ./share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
#  -file /tmp/mapper.py \
#  -mapper /tmp/mapper.py \
#  -file /tmp/reducer.py  \
#  -reducer /tmp/reducer.py  \
#  -input input/access.log \
#  -output input/output