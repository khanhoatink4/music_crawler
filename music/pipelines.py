import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem

from es_api import EsApi
from music.items import Music


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient()
        db = connection[settings['MONGODB_DB']]
        self.collection_music_nct = db[settings['MONGODB_COLLECTION_MUSIC_NCT']]
        self.es_api = EsApi(hosts=["http://localhost:9200/"])

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))

        if isinstance(item, Music):
            return self.store_music_nct(item, spider)

    def store_music_nct(self, item, spider):
        music_id = item['music_id']
        # self.es_api.add_data("dkbrowser", "music", music_id, dict(item))
        self.collection_music_nct.update({"music_id": music_id}, dict(item), upsert=True)
