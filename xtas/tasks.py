from __future__ import absolute_import

import json
import nltk
from rawes import Elastic
from urllib import urlencode
from urllib2 import urlopen

from xtas.celery import app

es = Elastic()


@app.task
def fetch_es(idx, typ, id, field):
    """Get a single document from Elasticsearch."""
    return es[idx][typ][id].get()['_source'][field]


@app.task
def tokenize(text):
    return nltk.word_tokenize(text)


@app.task
def semanticize(lang, text):
    if not lang.isalpha():
        raise ValueError("not a valid language: %r" % lang)
    url = 'http://semanticize.uva.nl/api/%s?%s' % (lang,
                                                   urlencode({'text': text}))
    return json.loads(urlopen(url).read())['links']


@app.task
def untokenize(tokens):
    return ' '.join(tokens)
