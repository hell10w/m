#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from logging import basicConfig, INFO
import sys

sys.path.insert(0, '/opt/feed2maildir/')
import rss


def main():
    feeds = rss.load_json('/generated/feeds')
    if not feeds:
        return

    cache_path = '/feeds-cache'
    for prefix, url in feeds:
        content = rss.fetch_feed(url, cache_path)
        if not content:
            continue

        items = rss.parse_feed(content)
        items = rss.add_prefix(items, prefix)
        if not items:
            continue

        rss.to_maildir(items, ('/feeds', ), cache=cache_path)


if __name__ == '__main__':
    basicConfig(level=INFO)
    main()
