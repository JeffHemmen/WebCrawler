#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple, deque

INDENT_BLOCK = '          '

class WebPageVisualiser:
    def __init__(self, entrypoint):
        self.entrypoint = entrypoint
        self._already_displayed = {entrypoint}
        self.OK_format_strs        = ['[{http_code}] {title}',  ' URL: {requested_url}']
        self.HTTPError_format_strs = ['[{http_code}] {reason}', ' URL: {requested_url}']
        self.URLError_format_strs  = ['[ERR] {reason}']
        self.defaultinfo = {'http_code': 'N/A', 'reason': '<No reason found.>', 'title': '<Untitled webpage>', 'requested_url': 'Unknown URL.'}

    def render_page(self, webpage, indent_level=0):
        if webpage.info['http_code'] is None:
            format_strs = self.URLError_format_strs
        elif 200 <= webpage.info['http_code'] < 300:
            format_strs = self.OK_format_strs
        else:
            format_strs = self.HTTPError_format_strs
        retstr = ''
        info = {**self.defaultinfo, **webpage.info}
        for i, format_str in enumerate(format_strs):
            retstr += INDENT_BLOCK * indent_level
            try: retstr += format_str.format(**info)
            except KeyError: retstr += '{Error: missing attributes in webpage info.}'
            if i != len(format_strs) - 1:
                retstr += '\n'
        return retstr

    def render_small_link(self, webpage, indent_level=0):
        retstr  = INDENT_BLOCK * indent_level
        retstr += INDENT_BLOCK + '+ Link to: '
        retstr += webpage.info['effective_url']
        return retstr

    def print(self):
        PagePrintNode = namedtuple('PagePrintNode', ['webpage', 'indent_level'])
        first_ppn = PagePrintNode(self.entrypoint, 0)
        scheduled_or_processed = set()
        q = deque([first_ppn]) # used as a FIFO queue
        while len(q):
            next = q.popleft() # FIFO
            webpage = next.webpage
            indent_level = next.indent_level

            small_links = []
            for link in webpage.links:
                if link in scheduled_or_processed:
                    small_links.append(link)
                else:
                    q.append(PagePrintNode(link, indent_level + 1)) # push to queue
                    scheduled_or_processed.add(link)
            print(self.render_page(webpage, indent_level))
            for small_link in small_links:
                print(self.render_small_link(small_link, indent_level))
            print()


