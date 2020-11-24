FROM iisas/hadoop-spark-pig-hive:2.9.2

RUN apt install -y wget
RUN apt install -y curl
RUN apt install -y netcat
RUN apt install -y zookeeperd

# setup flume
RUN wget http://www-eu.apache.org/dist/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz
RUN mkdir /opt/flume
RUN tar xvzf apache-flume-1.9.0-bin.tar.gz --directory=/opt/flume --strip 1
ENV FLUME_HOME=/opt/flume/

ADD hdfs-site.xml /usr/local/hadoop/etc/hadoop/hdfs-site.xml

# # lucene
# RUN wget https://downloads.apache.org/lucene/java/8.7.0/lucene-8.7.0.tgz
# RUN mkdir /opt/lucene
# RUN tar xvzf lucene-8.7.0.tgz --directory=/opt/lucene --strip 1
# ENV LUCENE_HOME=/opt/lucene/
# ENV CLASSPATH=/opt/lucene/core/lucene-core-8.7.0.jar:/opt/lucene/queryparser/lucene-queryparser-8.7.0.jar:/opt/lucene/analysis/common/lucene-analyzers-common-8.7.0.jar:/opt/lucene/demo/lucene-demo-8.7.0.jar

# svn
RUN apt install -y subversion
RUN apt install -y libapache2-mod-svn
RUN svn co https://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc jcc

# ant
# RUN wget https://downloads.apache.org//ant/binaries/apache-ant-1.10.9-bin.tar.gz
# RUN mkdir /opt/ant
# RUN tar xvzf apache-ant-1.10.9-bin.tar.gz --directory=/opt/ant --strip 1
# ENV ANT_HOME=/opt/ant

RUN apt install -y ant 
RUN apt install -y python3-dev
RUN apt install -y python3-pip
RUN pip3 install setuptools --upgrade 

# pylucene 
RUN wget https://downloads.apache.org/lucene/pylucene/pylucene-8.6.1-src.tar.gz
RUN mkdir /opt/pylucene
RUN tar xvzf pylucene-8.6.1-src.tar.gz --directory=/opt/pylucene --strip 1
ADD setup.py /opt/pylucene/jcc/setup.py
RUN touch /opt/pylucene/jcc/setup.py
WORKDIR /opt/pylucene/jcc/
RUN python3 /opt/pylucene/jcc/setup.py build
RUN python3 /opt/pylucene/jcc/setup.py install
WORKDIR /opt/pylucene/
ADD Makefile /opt/pylucene/Makefile
RUN make
RUN make install

# # reset entrypoint to not close container in compose
ENTRYPOINT /etc/bootstrap.sh -d && tail -f /dev/null