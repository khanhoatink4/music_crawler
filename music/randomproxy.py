import base64
import random
import re

from scrapy import log

from utils.hash_util import HashUtil


class RandomProxy(object):
    proxy_fail_count = {}

    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)

        self.proxies = {}
        for line in fin.readlines():
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)
            if parts:
                # Cut trailing @
                if parts.group(2):
                    user_pass = parts.group(2)[:-1]
                else:
                    user_pass = ''

                self.proxies[parts.group(1) + parts.group(3)] = user_pass
            else:
                self.proxies[line.strip()] = None

        fin.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return
        try:
            proxy_address = random.choice(self.proxies.keys())
            proxy_user_pass = self.proxies[proxy_address]

            request.meta['proxy'] = proxy_address
            if proxy_user_pass:
                basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
                request.headers['Proxy-Authorization'] = basic_auth
        except Exception as e:
            pass

    def process_exception(self, request, exception, spider):
        if 'proxy' in request.meta:
            proxy = request.meta['proxy']
            key = HashUtil.alphanumeric_hash(proxy)
            if key not in self.proxy_fail_count:
                self.proxy_fail_count[key] = 0
            self.proxy_fail_count[key] += 1
            if self.proxy_fail_count[key] > 10:
                log.msg('Removing failed proxy <%s>, %d proxies left' % (
                    proxy, len(self.proxies)))
                try:
                    del self.proxies[proxy]
                except ValueError:
                    pass
