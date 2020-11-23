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
```
