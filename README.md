## Flume

Nastartovanie 
```
/etc/bootstrap.sh -d
/opt/flume/bin/flume-ng agent -n agent -c conf -f /home/hadoop.conf -Dflume.root.logger=INFO,console
```

Odoslanie spravy 
```
nc localhost 1235
```

Indexovanie
```
hdfs dfs -cat /flume/events/* | python3 /home/indexer.py
```

Vyhladavanie
```
python3 /home/searcher.py 
python3 searcher.py 'must query location Bratislava' --stats method,protocol
python3 searcher.py 'must query response_code_string 404' 'must termrange date_time 14/Sep/2020:05:40:00 14/Sep/2020:06:40:00'
```
