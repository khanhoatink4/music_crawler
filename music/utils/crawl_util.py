# -*- coding: utf-8 -*-
import json

from lxml.html import parse


class CrawlUtil:
    def __init__(self):
        pass

    @staticmethod
    def crawl_content(url):
        parsed = parse(url)
        if parsed is None:
            return None
        doc = parsed.getroot()
        if doc is None:
            return None
        return doc.text_content()

    @staticmethod
    def crawl_json(url):
        content = CrawlUtil.crawl_content(url)
        return None if (content is None) else json.loads(content)
