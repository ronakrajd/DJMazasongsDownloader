import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from .ParseAlbum import ParseAlbum
from .ParseSingles import ParseSingles
import os

class ScrapeEnglishSingles(scrapy.Spider):
    start_urls = ['https://www.djmaza.fun/category/english-singles/a'
        , 'https://www.djmaza.fun/category/english-singles/b'
        , 'https://www.djmaza.fun/category/english-singles/c'
        , 'https://www.djmaza.fun/category/english-singles/d'
        , 'https://www.djmaza.fun/category/english-singles/e'
        , 'https://www.djmaza.fun/category/english-singles/f'
        , 'https://www.djmaza.fun/category/english-singles/g'
        , 'https://www.djmaza.fun/category/english-singles/h'
        , 'https://www.djmaza.fun/category/english-singles/i'
        , 'https://www.djmaza.fun/category/english-singles/j'
        , 'https://www.djmaza.fun/category/english-singles/k'
        , 'https://www.djmaza.fun/category/english-singles/l'
        , 'https://www.djmaza.fun/category/english-singles/m'
        , 'https://www.djmaza.fun/category/english-singles/n'
        , 'https://www.djmaza.fun/category/english-singles/o'
        , 'https://www.djmaza.fun/category/english-singles/p'
        , 'https://www.djmaza.fun/category/english-singles/q'
        , 'https://www.djmaza.fun/category/english-singles/r'
        , 'https://www.djmaza.fun/category/english-singles/s'
        , 'https://www.djmaza.fun/category/english-singles/t'
        , 'https://www.djmaza.fun/category/english-singles/u'
        , 'https://www.djmaza.fun/category/english-singles/v'
        , 'https://www.djmaza.fun/category/english-singles/w'
        , 'https://www.djmaza.fun/category/english-singles/x'
        , 'https://www.djmaza.fun/category/english-singles/y'
        , 'https://www.djmaza.fun/category/english-singles/z']
    base_url = "http://www.djmaza.fun"
    name = "ScrapeEnglishSingles"
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }

    def parse(self, response):
        list_pages = response.xpath('//ul[@class="pagination"]/li').extract()
        total_pages = len(list_pages)
        i = 1
        if total_pages == 0:
            print("Total Pages: " + total_pages.__str__())
            # self.parseArchivePage(response)
            request = scrapy.Request(
                response.request.url,
                callback=self.parseArchivePage)
            yield request
        while i <= total_pages - 1:
            request = scrapy.Request(
                response.request.url + "?page=" + i.__str__(),
                callback=self.parseArchivePage)
            yield request
            i = i + 1

    def parseArchivePage(self, response):
        print("called parseArchivePage")
        # print(response.xpath('//div[@class="archive-body"]/figure').extract())
        for album in response.xpath('//div[@class="archive-body"]/figure'):
            print((album.xpath(".//h3/a/text()").extract_first()).strip())
            album_link = (album.xpath(".//h3/a/@href").extract_first()).strip()
            parseAlbum = ParseAlbum("english-singles")
            request = scrapy.Request(
                self.base_url + album_link,
                callback=parseAlbum.parseIndividualAlbum)
            yield request
            # album_list_ref = self.db.collection(u'singleslist').document(album_name)
            # self.batch.set(album_list_ref, {u'name': album_name})
