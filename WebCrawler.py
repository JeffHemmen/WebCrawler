#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin

from IterTree import IterTree
from WebPage import WebPage
from WebPageVisualiser import WebPageVisualiser


re_title = re.compile(r'<title>(.*?)</title>')
re_href  = re.compile(r'href="(.+?)"')

config = None # set by command-line parser. Populate manually if using this as an imported module.

def parse_and_return_links(webpage) -> iter(WebPage):
    '''Generator function.
    Compiles and and sets the `info` dictionary (see `finally`).
    Then yields valid WebPage instances which are linked to in this page.

    Sets the following fields in `info`:
    - For successful calls (HTTP 200-299)
        * requested_url
        * effective_url
        * redirected_url (if applicable)
        * http_code
        * content_type
        * title (if found)
    - For calls raising HTTPError (HTTP >= 300)
        * requested_url
        * effective_url
        * redirected_url (if applicable)
        * http_code
        * reason
   - For calls raising URLError
        * requested_url
        * http_code as None
        * reason
    '''

    pageinfo = {}
    pageinfo['requested_url'] = webpage.urlstr
    try:
        with urlopen(webpage.urlstr) as uo:
            http_code = uo.code
            pageinfo['http_code'] = http_code
            redirect_url = uo.geturl()
            if webpage.urlstr != redirect_url:
                pageinfo['effective_url'] = redirect_url
                pageinfo['redirected_to'] = redirect_url
                # Need to check for redirect to different domain!
            else:
                pageinfo['effective_url'] = webpage.urlstr
            content_type = uo.headers.get_content_type()
            pageinfo['content_type'] = content_type
            if content_type != 'text/html':
                return

            # Should be a valid web page in HTML after this point

            # Go through the page line by line
            #   set the title if found; then stop looking for it
            #   save all href's in a set (avoid duplicates)
            enc = uo.headers.get_content_charset('utf-8')
            lines = (byteline.decode(enc) for byteline in uo)
            found_title = False
            links = set()

            for line in lines:
                if not found_title:
                    re_title_match = re_title.search(line)
                    if re_title_match:
                        pageinfo['title'] = re_title_match.group(1)
                        found_title = True
                re_href_matches = re_href.finditer(line)
                for match in re_href_matches:
                    links.add(match.group(1))

            # Go through all href's in the set
            #   convert them into absolute URLs
            #   discard ones from a different domain
            #   discard ones unlikely to be HTML pages (should make this parametriseable)
            for link in links:
                link_page = WebPage(urljoin(redirect_url, link))
                if link_page:
                    webpage.links.append(link_page)
                    yield link_page



    except HTTPError as e:
        pageinfo['http_code'] = e.code
        pageinfo['reason'] = e.reason
        redirect_url = e.geturl()
        if webpage.urlstr != redirect_url:
            pageinfo['effective_url'] = redirect_url
            pageinfo['redirected_to'] = redirect_url
        else:
            pageinfo['effective_url'] = webpage.urlstr
    except URLError as e:
        pageinfo['http_code'] = None
        pageinfo['reason'] = e.reason
    finally:
        webpage.info = pageinfo



def build_graph(entrypoint_url):

    entrypoint = WebPage(entrypoint_url)
    entrypoint.config = config
    to_do = IterTree(entrypoint)
    to_do_iter = to_do.get_iterator(config.traversal)
    for item in to_do_iter:
        if config.verbose: print('Item: ' + repr(item.data), file=sys.stderr)
        for linked_page in parse_and_return_links(item.data):
            if linked_page in to_do.data_set:
                continue # Do not add duplicates onto the to_do tree
            item.add_child(linked_page)
            if config.verbose: print('    Adding child: ' + repr(linked_page), file=sys.stderr)
    return entrypoint

def main(entrypoint_url):
    graph = build_graph(entrypoint_url)
    wpv = WebPageVisualiser(graph)
    wpv.print()


if __name__ == '__main__':
    import ArgParseHelper
    config = ArgParseHelper.main() # global variable
    if config.verbose: print(repr(config), file=sys.stderr)
    main(config.entrypoint)