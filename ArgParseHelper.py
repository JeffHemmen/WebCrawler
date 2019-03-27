#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def main():
    parser = argparse.ArgumentParser(description="A simple Web Crawler.")
    parser.add_argument('entrypoint', metavar='URL', help='The initial URL at which to start crawling.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print additional information to stderr.')
    parser.add_argument('--max-pages', dest='max_pages', type=int, default=256, help='''The maximum number of webpages
                                                                                     to crawl. Subsequent pages will
                                                                                     be ignored.''')
    parser.add_argument('--max-depth', dest='max_depth', type=int, help='''The maximum number of \'hops\'
                                                                                     to follow. Links on pages already
                                                                                     MAX_DEPTH deep will be ignored.''')
    parser.add_argument('--traversal', dest='traversal', default='BF', help='''Values=BF|DF. The traversal approach for
                                                                               the website. 'BF' for breadth-first
                                                                               (default). 'DF' for depth-first.''')

    args = parser.parse_args()

    if args.max_depth:
        raise NotImplementedError('The MAX_DEPTH feature is not yet implemented.')

    return args