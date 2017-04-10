# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import random
import logging
import time

from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from music.utils.hash_util import HashUtil
from music.items import Music


class NCTSpider(CrawlSpider):
    name = 'nct_crawler'
    allowed_domains = ['nhaccuatui.com']
    start_urls = []
    list_url = [
        # http://www.nhaccuatui.com/bai-hat/nhac-tre-moi.3.html
        "http://www.nhaccuatui.com/bai-hat/nhac-tre-moi.",
        "http://www.nhaccuatui.com/bai-hat/tru-tinh-moi.",
        "http://www.nhaccuatui.com/bai-hat/remix-viet-moi.",
        "http://www.nhaccuatui.com/bai-hat/rap-viet-moi.",
        "http://www.nhaccuatui.com/bai-hat/tien-chien-moi.",
        "http://www.nhaccuatui.com/bai-hat/nhac-trinh-moi.",
        "http://www.nhaccuatui.com/bai-hat/thieu-nhi-moi.",
        "http://www.nhaccuatui.com/bai-hat/rock-viet-moi.",
        "http://www.nhaccuatui.com/bai-hat/cach-mang-moi.",
        "http://www.nhaccuatui.com/bai-hat/pop-moi.",
        "http://www.nhaccuatui.com/bai-hat/rock-moi.",
        "http://www.nhaccuatui.com/bai-hat/electronicadance-moi.",
        "http://www.nhaccuatui.com/bai-hat/rbhip-hoprap-moi.",
        "http://www.nhaccuatui.com/bai-hat/bluesjazz-moi.",
        "http://www.nhaccuatui.com/bai-hat/country-moi.",
        "http://www.nhaccuatui.com/bai-hat/latin-moi.",
        "http://www.nhaccuatui.com/bai-hat/indie-moi.",
        "http://www.nhaccuatui.com/bai-hat/au-my-khac-moi.",
        "http://www.nhaccuatui.com/bai-hat/nhac-han-moi.",
        "http://www.nhaccuatui.com/bai-hat/nhac-hoa-moi.",
        "http://www.nhaccuatui.com/bai-hat/nhac-nhat-moi.",
        "http://www.nhaccuatui.com/bai-hat/nhac-thai-moi.",
        "http://www.nhaccuatui.com/bai-hat/beat-moi.",
        "http://www.nhaccuatui.com/bai-hat/khong-loi-moi.",
        "http://www.nhaccuatui.com/bai-hat/the-loai-khac-moi."
    ]
    random.shuffle(start_urls)

    def __init__(self, name=None):
        super(NCTSpider, self).__init__(name)

    def start_requests(self):
        logging.info("start request")
        for url in self.list_url:
            for id in xrange(1, 5):
                new_url = url + str(id) + ".html"
                yield Request(url=new_url,
                              callback=lambda r: self.parse_page(r),
                              method="GET")

    def parse_page(self, response):
        list_music = response.xpath(
            '//div[@class="item_content"]//a[@class="name_song"]/@href').extract()
        for music in list_music:
            yield Request(url=music,
                          callback=lambda r: self.parser_page_detail(r),
                          method='GET')

    def parser_page_detail(self, response):
        song_name = response.xpath(
            '//div[@class="name_title"]/h1/text()').extract_first()
        song_singer = response.xpath(
            '//div[@class="name_title"]/h2/a/text()').extract_first()
        image = response.xpath('//link[@rel="image_src"]/@href').extract_first()
        updated_at = int(time.time())
        author = response.xpath('//p[@class="name_post"]/text()').extract_first()
        author = str(author).split("Nhạc sĩ: ")
        if len(author) == 2:
            author = author[1].split("\n")[0]
        else:
            author = ""
        list_description = response.xpath('//p[@class="pd_lyric trans"]//text()').extract()
        desciption = ""
        for i in xrange(1, len(list_description)):
            desciption += list_description[i]
        category = response.xpath('//div[@class="topbreadCrumb"]//a/text()').extract()[1]
        if len(str(category).split("Bài hát ")) > 1:
            category = str(category).split("Bài hát ")[1]
        else:
            category = ""
        music = Music()
        music["url"] = response.url
        music["music_id"] = HashUtil.alphanumeric_hash(response.url)
        music["author"] = author
        music["category"] = category
        music["updated_at"] = updated_at
        music["description"] = desciption
        music["title"] = song_name
        music["singer"] = song_singer
        music["image"] = image
        music["site_name"] = "nhaccuatui"
        yield music


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'Safari/537.36 '
    })

    process.crawl(NCTSpider)
    process.start()  # the script will block here until the crawling is finished
