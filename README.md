# WebCrawler—Monzo tech test

## Dependencies

WebCrawler only uses modules from the Python Standard Library, and runs with Python 3.5 and later.  

## Usage
```
usage: WebCrawler.py [-h] [-v] [--max-pages MAX_PAGES] [--max-depth MAX_DEPTH]
                     [--traversal TRAVERSAL]
                     URL

A simple Web Crawler.

positional arguments:
  URL                   The initial URL at which to start crawling.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print additional information to stderr.
  --max-pages MAX_PAGES
                        The maximum number of webpages to crawl. Subsequent
                        pages will be ignored.
  --max-depth MAX_DEPTH
                        The maximum number of 'hops' to follow. Links on pages
                        already MAX_DEPTH deep will be ignored.
  --traversal TRAVERSAL
                        Values=BF|DF. The traversal approach for the website.
                        'BF' for breadth-first (default). 'DF' for depth-
                        first.
```

## Output format
This is customisable, but each webpage is displayed according to the following example:
```
[200] Monzo – The bank of the future
 URL: https://monzo.com/
```
where `200` is the HTTP status code, and `Monzo – The bank of the future` the page title.

Pages linked to by another page are listed below the latter, at a higher level of indentation. This creates a simple tree view.  
Where a linked page is already displayed somewhere else, a shorter `Link to` mention of that page is given under its referrer page(s).

In the simplest case of only two pages, referencing each other, the output would look thus:
```
[200] Monzo – The bank of the future
 URL: https://monzo.com/

          [200] Monzo – Blog
           URL: https://monzo.com/blog
                    + Link to: https://monzo.com
```

Please see `sample_output.txt.gz` for the output of the following command:  
```./WebCrawler.py https://archer.fandom.com/wiki/Archer_Wiki --max-pages 2048```

## Notes and Thoughts
### Concurrency
WebCrawler does _not_ currently have concurrency—and I would love to discuss with you why, and how we could go about this.
### Testing
Unit Tests are provided as part of the Python Docstring.  
Run `python3 -m doctest <module>.py`.  
No other tests (integration, end-to-end, ...) are provided, as this is very tricky, because it requires external infrastructure or simulation thereof.
### Logging
No fancy logging is currently implemented.
If `-v` is passed as an argument, some debug output is printed to stderr.
The
### Robots.txt and Public Websites
WebCrawler ignores `robots.txt` files. Please use discretion when running it against public websites. It is recommended to test WebCrawler against a locally hosted website (not provided).  
You will find WebCrawler is disallowed from accessing many websites (e.g. websites fronted by CloudFlare—_hint, hint_). This is most likely due to the User-Agent header. It is a conscious decision not to circumvent this, so as not to antagonise the internet.
### Retry logic
No retry logic is currently implemented.
### HTTP Redirects
In the current implementation:
* redirects (if any) are automatically followed
* if a page has been redirected, the `redirected_url` info field is set
* pages are distinguished based on their originally queries URL; if one page redirects to another, they are still considered different, and duplicated can be created this way

This handling of redirects can create some funniness in the output (cf. `sample_output.txt.gz`).  
Various strategies have pros and cons in different situations—I am happy to discuss this in a hangout session.
