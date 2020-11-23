import sys, json
import lucene
from datetime import datetime

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, \
    FieldInfos, MultiFields, MultiTerms, Term
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory
from org.apache.lucene.document import Document, Field, StoredField, StringField, TextField
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

from java.nio.file import Path, Paths

def index_document(writer, log):
    doc = Document()

    doc.add(Field('host', log['host'], TextField.TYPE_STORED))
    # doc.add(Field('client_user_name_if_available', log['client_user_name_if_available'], TextField.TYPE_STORED))
    # doc.add(Field('date_time', log['date_time'], TextField.TYPE_STORED))
    # doc.add(Field('method', log['method'], TextField.TYPE_STORED))
    # doc.add(Field('request_path', log['request_path'], TextField.TYPE_STORED))
    # doc.add(Field('protocol', log['protocol'], TextField.TYPE_STORED))
    # doc.add(Field('response_code', log['response_code'], TextField.TYPE_STORED))
    # doc.add(Field('content_size', log['content_size'], TextField.TYPE_STORED))
    # doc.add(Field('request_referrer', log['request_referrer'], TextField.TYPE_STORED))
    # doc.add(Field('request_user_agent', log['request_user_agent'], TextField.TYPE_STORED))
    # doc.add(Field('router_name', log['router_name'], TextField.TYPE_STORED))
    # doc.add(Field('server_url', log['server_url'], TextField.TYPE_STORED))
    # doc.add(Field('request_duration', log['request_duration'], TextField.TYPE_STORED))
    
    # doc.add(Field("docid", str(1), StringField.TYPE_NOT_STORED))
    # doc.add(Field("owner", "unittester", StringField.TYPE_STORED))
    # doc.add(Field("search_name", "wisdom", StoredField.TYPE))
    # doc.add(Field("meta_words", "rabbits are beautiful", TextField.TYPE_NOT_STORED))

    writer.addDocument(doc)

lucene.initVM()

store = DirectoryReader.open(SimpleFSDirectory(Paths.get('/home/test-index')))
analyzer = StandardAnalyzer()
searcher = IndexSearcher(store)

# parser = QueryParser('request_path', analyzer)
parser = QueryParser('response_code', analyzer)

query = parser.parse('404')
results = searcher.search(query, 100)
hits = results.scoreDocs
# print(results.totalHits.value)
for i in range(min(results.totalHits.value, 10)):
    doc = searcher.doc(hits[i].doc)
    print('{}: {}; score={}; doc='.format(i, hits[i].doc, hits[i].score, doc.get("request_path")))
# print(results)
