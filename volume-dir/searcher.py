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
    print('{}: {}; score={}; doc='.format(i, hits[i].doc, hits[i].score))
