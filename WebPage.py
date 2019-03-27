#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
To use with different domains, WebPage must be subclassed before it is instantiated.
>>> class MonzoPage(WebPage):
...     def __repr__(self):
...         return '''MonzoPage('{}')'''.format(self.urlstr)
...
>>> class StarlingPage(WebPage):
...     def __repr__(self):
...         return '''StarlingPage('{}')'''.format(self.urlstr)
...
>>> monzo = MonzoPage('monzo.com')
>>> starling = StarlingPage('starlingbank.com')
>>> MonzoPage.domain
'monzo.com'
>>> StarlingPage.domain
'starlingbank.com'
>>> assert WebPage.domain is None

Without an explicit scheme, WebPage defaults to HTTPS. An empty URL path defaults to '/'.
>>> monzo
MonzoPage('https://monzo.com/')

Once instantiated, a WebPage class does not allow subsequent instances of different domains
>>> monzo_me = MonzoPage('monzo.me')
>>> assert monzo_me is None

Equivalent URLs will return the same object.
>>> careers = MonzoPage('http://monzo.com/careers/')
>>> jobs    = MonzoPage('https://monzo.com/careers/#jobs')
>>> assert careers is jobs # same object!

The canonical URL can be retrieved using the `urlstr` getter. Non-differentiating information is dropped from the URL.
>>> jobs.urlstr
'http://monzo.com/careers/'
"""

from sys import stderr
from urllib.parse import urlparse

class WebPage:
    '''
    A class to store information about a web page, including links to other web pages.
    This effectively makes this class a Graph.
    It enforces the single-domain requirement, and avoids duplicate creation by returning the existing instance.
    You cannot have WebPage objects for different domains (but you can get around this by subclassing WebPage).
    Also, it is hashable, ignoring data that is unlikely to indicate a different page (e.g. http v. https).

    TODO: It is worth considering using a class factory, rather than a single class with this many class attributes.
    '''

    domain, site, _config = None, None, None
    # site is a dict of all (unique) web pages; saves us having to traverse the graph, as hash-based searches are fast.
    # _config is a reference to the config in the importing module

    def __new__(cls, urlstr):
        if cls.site and cls._config and len(cls.site) >= cls._config.max_pages:
            if cls._config.verbose: print('Refusing creation of new WebPage, as max_pages reached.', file=stderr)
            return None # refuse creation of WebPage if we reached the max_pages limit (and catch this early)
        self = super().__new__(cls)
        if not urlstr.startswith('http'):
            urlstr = 'https://' + urlstr
        _p = urlparse(urlstr)
        self.scheme = _p.scheme
        self.relative_part = _p.path
        if self.relative_part == '':
            self.relative_part = '/'
        if _p.params: self.relative_part += ';' + _p.params
        if _p.query : self.relative_part += '?' + _p.query
        if cls.domain is None:
            cls.domain = _p.netloc
        elif cls.domain != _p.netloc:
            return None # refuse creation of WebPage of different domain
        if cls.site is None:
            cls.site = {}
        # If this page already exists, return that instance (drop `self`)
        if hash(self) in cls.site:
            return cls.site[hash(self)]

        # Otherwise finish initialising `self` and return it
        self.links = []
        self.info = None
        cls.site[hash(self)] = self
        return self

    @property
    def config(self):
        return copy(self._config)

    @config.setter
    def config(self, config):
        type(self)._config = config

    @property
    def urlstr(self):
        '''Canonical string representation of the URL'''
        return self.scheme + '://' + self.domain + self.relative_part

    def __repr__(self):
        return '''WebPage('{}')'''.format(self.urlstr)

    def __eq__(self, other):
        '''Only compare relative parts of URLs. URLs of different domains
        will be marked as invalid, and should never be compared.'''
        return self.relative_part == other.relative_part

    def __hash__(self):
        '''Return hash of relative part of URL'''
        return hash(self.relative_part)
