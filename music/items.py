import scrapy
from scrapy.item import Field


class Music(scrapy.Item):
    site_name = Field()
    music_id = Field()
    title = Field()
    url = Field()
    singer = Field()
    category = Field()
    description = Field()
    updated_at = Field()
    author = Field()
    image = Field()
