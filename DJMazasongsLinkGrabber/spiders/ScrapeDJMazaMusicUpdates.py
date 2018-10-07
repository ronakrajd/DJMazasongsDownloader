import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from .ParseAlbum import ParseAlbum
from .ParseSingles import ParseSingles
import os

class ScrapeDJMazaMusicUpdates(scrapy.Spider):
    # cred = credentials.Certificate(os.getcwd() + "\\serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    # db = firestore.Client()
    start_urls = ['http://www.djmaza.ms']
    base_url = "http://www.djmaza.ms"
    name = "ScrapeDJMazaMusicUpdates"
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }

    def parse(self, response):
        i = 1
        for update_tags in response.xpath('//div[@class="home-trend-body"]/ul/li'):
            print(i.__str__() + ". " + update_tags.xpath('.//a/text()').extract_first().strip())
            if "Albums" in update_tags.xpath('.//div[2]/span/text()').extract_first().strip().split():
                parseAlbum = ParseAlbum("new_updates")
                request = scrapy.Request(
                    self.base_url + update_tags.xpath('.//a/@href').extract_first(),
                    callback=parseAlbum.parseIndividualAlbum)
                yield request
            if "Singles" in update_tags.xpath('.//div[2]/span/text()').extract_first().strip().split():
                parseSingles = ParseSingles("new_updates")
                request = scrapy.Request(
                    self.base_url + update_tags.xpath('.//a/@href').extract_first(),
                    callback=parseSingles.parseSingles)
                yield request
            i = i + 1
