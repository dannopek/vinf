import sys, json
import argparse
import lucene
from datetime import datetime
from common import handleDate, luceneStringToDate, getSortableColumns
import json
import unicodedata

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, \
    FieldInfos, MultiFields, MultiTerms, Term, PointValues, IndexReader
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory
from org.apache.lucene.document import Document, Field, StoredField, StringField, TextField, IntRange, IntPoint
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, Query, MatchAllDocsQuery, TermRangeQuery, Sort, SortField, BooleanQuery, \
    BooleanClause
from org.apache.lucene.facet import Facets, FacetsCollector
from org.apache.lucene.search.spell import LuceneDictionary
from org.apache.lucene.util import QueryBuilder, BytesRef
from org.apache.lucene.search.grouping import GroupingSearch

from java.nio.file import Path, Paths

parser = argparse.ArgumentParser(description='Log searcher.')
parser.add_argument('search', nargs='*',
                    help="Search query in format 'must|should|filter|must_not query|intrange|termrange <field_name> field_value)'* Posible field names: host, client_user_name_if_available, date_time, method, request_path, protocol, response_code, content_size, request_referrer, request_user_agent, router_name, server_url, request_duration")
parser.add_argument('--stats', default=False,
                    help='Show all values of given field with number of occurences ("protocol", "response_code_string", "method", "location").')
parser.add_argument('--ndocs', dest='ndocs', default=10, type=int,
                    help='Number of documents to return')
parser.add_argument('--offset', dest='offset', default=0, type=int,
                    help='Position from where to show result')
parser.add_argument('--sort', choices=getSortableColumns().extend('agg'), default=False,
                    help='Field by which sort documents')
parser.add_argument('--sort-direction', dest='sortDirection', choices=['asc', 'desc'], default='asc',
                    help='Field by which sort documents')
args = parser.parse_args()

# print(args.search)
# print(args.ndocs)
# print(args.offset)
# exit()

lucene.initVM()

store = DirectoryReader.open(SimpleFSDirectory(Paths.get('/home/test-index')))
analyzer = StandardAnalyzer()
searcher = IndexSearcher(store)

def docToString(doc):
    return json.dumps({
        'host': doc.get('host'),
        'method': doc.get('method'),
        'response_code': doc.get('response_code_string'),
        'protocol': doc.get('protocol'),        
        'date_time': luceneStringToDate(doc.get('date_time')),
        'request_path': doc.get('request_path'),
        'location': doc.get('location'),
    })


def getQueryBuiler():
    # builder = QueryBuilder(analyzer)
    boolean_query = BooleanQuery.Builder()

    # print(args.search)

    if len(args.search) == 0:
        boolean_query.add(MatchAllDocsQuery(), BooleanClause.Occur.MUST)
        return boolean_query
    
    for i in range(len(args.search)):
        curSearch = args.search[i].split(' ')

        if curSearch[1] == 'query':
            parser = QueryParser(curSearch[2], analyzer)
            query = parser.parse(curSearch[3])
        elif curSearch[1] == 'intrange':
            query = IntPoint.newRangeQuery(curSearch[2], curSearch[3], curSearch[4])
        elif curSearch[1] == 'termrange':
            lowerDate = handleDate(curSearch[3], '%d/%b/%Y:%H:%M:%S')
            upperDate = handleDate(curSearch[4], '%d/%b/%Y:%H:%M:%S')
            query = TermRangeQuery.newStringRange(curSearch[2], lowerDate, upperDate, True, True)

        if curSearch[0] == 'must':
            boolean_query.add(query, BooleanClause.Occur.MUST)
        elif curSearch[0] == 'should':
            boolean_query.add(query, BooleanClause.Occur.SHOULD)
        elif curSearch[0] == 'filter':
            boolean_query.add(query, BooleanClause.Occur.FILTER)
        elif curSearch[0] == 'must_not':
            boolean_query.add(query, BooleanClause.Occur.MUST_NOT)
        else:
            print('raise exception')
            # raise Exception
    # exit()
    # parser = QueryParser('method1', analyzer)
    # query = parser.parse('options')
    # boolean_query.add(query, BooleanClause.Occur.MUST)

    # parser = QueryParser('response_code', analyzer)
    # query = IntPoint.newRangeQuery('response_code', 200, 300)
    # boolean_query.add(query, BooleanClause.Occur.MUST)

    # lowerDate = handleDate("19/Jul/2020:05:40:00 +0000")
    # upperDate = handleDate("19/Jul/2020:06:45:04 +0000")
    # query = TermRangeQuery.newStringRange("date_time", lowerDate, upperDate, True, True)
    # boolean_query.add(query, BooleanClause.Occur.MUST)


    return boolean_query


def search():
    boolean_query = getQueryBuiler()

    final_query = boolean_query.build()
    if args.sort:
        sort = Sort(SortField(args.sort, SortField.Type.STRING, args.sortDirection == 'desc'))
        results = searcher.search(final_query, args.ndocs, sort)
    else:
        results = searcher.search(final_query, args.ndocs)

    return results

def printSearchResults(results):
    hits = results.scoreDocs
    totalHits = results.totalHits.value
    offset = min(totalHits, args.offset)
    print('Found {:d} results, showing result from {} to {} position.'.format(totalHits, offset, offset + min(totalHits, args.ndocs)))
    for i in range(args.offset, min(totalHits, args.ndocs)):
        doc = searcher.doc(hits[i].doc)
        fields = doc.toString()
        print('{}: {}; doc={}'.format(i, hits[i].doc, docToString(doc)))

def getDocCount(field_name, field_value):
    freq = store.docFreq(Term(field_name, field_value))
    return freq

def printAggregationSearch(field_name):
    print('Values for field "{}".'.format(field_name))
    
    groupingSearch = GroupingSearch(field_name)
    groupingSearch.setAllGroups(True)

    if args.sort != 'agg':
        sort = Sort(SortField(field_name, SortField.Type.STRING))
        groupingSearch.setGroupSort(sort)

    query = getQueryBuiler().build()
    result = groupingSearch.search(searcher, query, args.offset, 2500) #args.ndocs

    totalGroupCount = result.totalGroupCount
    print('Total groups count: {} Total docs count {}'.format(totalGroupCount, result.totalHitCount))

    aggGroups = []
    groups = result.groups
    for i in range(len(groups)):
        charCodes = groups[i].groupValue.toString()[1:-1].split(' ')
        for j in range(len(charCodes)):
            if charCodes[j] == '':
                charCodes[j] = 45
            else:
                charCodes[j] = int(charCodes[j], 16) # % 128
        groupName = str(bytearray(charCodes), 'utf-8')
        aggGroups.append({'name': groupName, 'value': int(groups[i].totalHits.value)})
    
    if args.sort == 'agg':
        aggGroups = sorted(aggGroups, key=lambda k: k['value'], reverse=True) 

    table_line = ''.join(['-' for i in range(27)])
    print(table_line)
    print('| {:10} | {:10} |'.format('Value', 'Count'))
    print(table_line)
    groups = result.groups
    for i in range(min(args.ndocs, len(aggGroups))):
        print('| {:10} | {:10,d} |'.format(aggGroups[i]['name'], aggGroups[i]['value']))
    print(table_line)
    print()

if args.stats:
    stats = args.stats.split(',')
    for i in range(len(stats)):
        printAggregationSearch(stats[i])
else:
    results = search()
    printSearchResults(results)

# printAggregationSearch('method')
# printAggregationSearch('response_code')
# printAggregationSearch('location')
# printAggregationSearch('date_time')


store.close()
