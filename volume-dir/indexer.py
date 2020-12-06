import sys, json
import lucene
from datetime import datetime
import unicodedata

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, \
    FieldInfos, MultiFields, MultiTerms, Term, MultiFields
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory
from org.apache.lucene.document import Document, Field, StoredField, StringField, TextField, IntPoint, NumericDocValuesField,\
     DateTools, SortedDocValuesField
from org.apache.lucene.util import BytesRef
from org.apache.lucene.facet import FacetField

from java.nio.file import Path, Paths
from common import handleDate


def index_document(writer, log):
    doc = Document()

    doc.add(SortedDocValuesField('host', BytesRef(log['host'])))
    doc.add(Field('host', log['host'], TextField.TYPE_STORED))
    doc.add(Field('client_user_name_if_available', log['client_user_name_if_available'], TextField.TYPE_STORED))
    date = handleDate(log['date_time'])
    doc.add(SortedDocValuesField('date_time', BytesRef(date)))
    doc.add(Field('date_time', date, StringField.TYPE_STORED))

    doc.add(SortedDocValuesField('method', BytesRef(log['method'])))
    # doc.add(FacetField('method', log['method']))
    doc.add(Field('method', log['method'], TextField.TYPE_STORED))

    doc.add(SortedDocValuesField('request_path', BytesRef(log['request_path'])))
    doc.add(Field('request_path', log['request_path'], TextField.TYPE_STORED))
    doc.add(SortedDocValuesField('protocol', BytesRef(log['protocol'])))
    doc.add(Field('protocol', log['protocol'], StringField.TYPE_STORED)) 
    doc.add(SortedDocValuesField('response_code', BytesRef(str(log['response_code']))))
    response_code = str(log['response_code']) if log['response_code'] else 'None'
    doc.add(Field('response_code_string', response_code, StringField.TYPE_STORED))
    doc.add(IntPoint('response_code', log['response_code']))
    doc.add(SortedDocValuesField('content_size', BytesRef(log['content_size'])))
    doc.add(IntPoint('content_size', log['content_size']))
    doc.add(Field('request_referrer', log['request_referrer'], TextField.TYPE_NOT_STORED))
    doc.add(Field('request_user_agent', log['request_user_agent'], TextField.TYPE_NOT_STORED))
    doc.add(Field('router_name', log['router_name'], TextField.TYPE_NOT_STORED))
    doc.add(Field('server_url', log['server_url'], TextField.TYPE_STORED))
    doc.add(SortedDocValuesField('request_duration', BytesRef(log['request_duration'])))
    doc.add(IntPoint('request_duration', log['request_duration']))

    location = str(log['location']) if log['location'] else 'None'
    location_ascii_free = unicodedata.normalize('NFKD', location).encode('ascii','ignore').decode('ascii')
    doc.add(SortedDocValuesField('location', BytesRef(location_ascii_free)))
    # doc.add(Field('location_raw', location, StringField.TYPE_STORED))
    doc.add(Field('location', location, TextField.TYPE_STORED))

    writer.addDocument(doc)

lucene.initVM()

store = SimpleFSDirectory(Paths.get('/home/index'))
analyzer = StandardAnalyzer()

ltc_analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
config = IndexWriterConfig(ltc_analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(store, config)

start_time = datetime.now()
i = 0
for line in sys.stdin:
    log = json.loads(line)
    index_document(writer, log)

    i += 1
    if i % 25000 == 0:
        print(i)

writer.close()

end_time = datetime.now()
print('Indexed in {}'.format(end_time - start_time))