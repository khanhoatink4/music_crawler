#!/usr/bin/env bash
#/bin/bash
kill -9 `ps -ef | grep "/usr/local/bin/scrapy" | cut -d' ' -f5 | head -n 1`
nohup scrapy crawl nct_crawler>music_crawler.log 2>&1 &