FROM debian

RUN apt update
RUN apt upgrade

RUN wget http://www-eu.apache.org/dist/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz
RUN tar xvzf apache-flume-1.9.0-bin.tar.gz

RUN apt install openjdk-11-jdk
RUN export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64