## Flume

Nastartovanie 
```
/apache-flume-1.9.0-bin/bin/flume-ng agent -n agent -c conf -f ./../helloworld.conf -Dflume.root.logger=INFO,console
```

Odoslanie spravy 
```
curl -X POST -H 'Content-Type: application/json; charset=UTF-8' -d '[{"headers":{"header.key":"header.value"}, "body":"hello world"}]' http://localhost:1234
```