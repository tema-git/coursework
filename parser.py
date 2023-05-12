from os import listdir
from os.path import isfile, join
from parsel import Selector
import pandas as pd
import re

def parser(file):
    with open('C:/coursework/pars/pars/spiders/data/river/full/'+file, 'r', encoding="utf8", errors='ignore') as fp:
        data = fp.read()

    result = {
        'journal': '',
        'title': '',
        'ISSN': '',
        'DOI': '',
        'authors': [],
        'affilations': [],
        'date': '',
        'pages': '',
        'abstract': '',
        'raw_url': '',
        'keywords': []

    }

    selector = Selector(text=data)

    #DOI
    s = selector.xpath('//meta[@name="DC.Identifier.DOI" or @name="DOI"]')
    if (s):
        result['DOI'] = s.attrib['content']
    else:
        print(file + "doi")

    #title
    s = selector.xpath('//meta[@name="DC.Title" or @name="dc.title"]')
    if (s):
        s = s.attrib['content']
        result['title'] = " ".join(s.split())
    else:
        print(file + 'title')

    #journal
    s = selector.xpath('//meta[@name="DC.Source" or @name="prism.publicationName"]')
    if (s):
        s = s.attrib['content']
        result['journal'] = " ".join(s.split())
    else:
        print(file + 'journal')

    #ISSN
    s = selector.xpath('//meta[@name="DC.Source.ISSN"]')
    if (s):
        result['ISSN'] = s.attrib['content']
    else:
        print(file + 'issn')


    #year
    s = selector.xpath('//meta[@name="DC.Date.created" or @name="citation_date"]')
    if (s):
        s = s.attrib['content']
        result['date'] = s
    else:
        print(file + 'date')

    #pages
    s = selector.xpath('//meta[@name="pageNumber"]')
    if (s):
        s = s.attrib['content']
        result['pages'] = s
    else:
        s1 = selector.xpath('//meta[@name="citation_firstpage"]')
        s2 = selector.xpath('//meta[@name="citation_lastpage"]')
        if s1 and s2:
            s1 = s1.attrib['content']
            s2 = s2.attrib['content']
            if '–' in s1:
                result['pages'] = str(s1)
            else:
                result['pages'] = str(s1)+'-'+str(s2)
        else:
            print(file+'pages')


    #abstract
    s = selector.xpath('//meta[@name="DC.Description"]')
    if (s):
        s = s[0].attrib['content']
        result['abstract'] = s
    else:
        print(file + 'abstract')

    #url
    s = selector.xpath('//meta[@name="DC.Identifier.URI"]')
    if (s):
        s = s.attrib['content']
        result['raw_url'] = s
    else:
        print(file + 'url')

    #keywords
    s = selector.xpath('//meta[@name="citation_keywords"]')
    for i in s:
        if (i):
            i = i.attrib['content']
            result['keywords'].append(i)
        else:
            print(file + 'keywords')


    #authos n affilations
    s = selector.xpath('//meta[@name="citation_author"]')
    for i in s:
        if (i):
            i = i.attrib['content']
            result['authors'].append(i)
        else:
            print(file + 'author')

    s = selector.xpath('//meta[@name="citation_author_institution"]')
    for i in s:
        if (i):
            i = i.attrib['content']
            result['affilations'].append(i)
        else:
            print(file + 'affilation')

    return (result)

answer = []
mypath = 'C:/coursework/pars/pars/spiders/data/river/full'
all = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in all:
    answer.append(parser(i))

pd.DataFrame(answer).to_csv('C:/coursework/pars/parser/output_river.csv')