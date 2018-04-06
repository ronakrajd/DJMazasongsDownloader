import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from .ParseAlbum import ParseAlbum
from .ParseSingles import ParseSingles
import os

class ScrapeIndipopAlbums(scrapy.Spider):
    start_urls = ['https://www.djmaza.fun/category/indipop-albums/a'
        , 'https://www.djmaza.fun/category/indipop-albums/b'
        , 'https://www.djmaza.fun/category/indipop-albums/c'
        , 'https://www.djmaza.fun/category/indipop-albums/d'
        , 'https://www.djmaza.fun/category/indipop-albums/e'
        , 'https://www.djmaza.fun/category/indipop-albums/f'
        , 'https://www.djmaza.fun/category/indipop-albums/g'
        , 'https://www.djmaza.fun/category/indipop-albums/h'
        , 'https://www.djmaza.fun/category/indipop-albums/i'
        , 'https://www.djmaza.fun/category/indipop-albums/j'
        , 'https://www.djmaza.fun/category/indipop-albums/k'
        , 'https://www.djmaza.fun/category/indipop-albums/l'
        , 'https://www.djmaza.fun/category/indipop-albums/m'
        , 'https://www.djmaza.fun/category/indipop-albums/n'
        , 'https://www.djmaza.fun/category/indipop-albums/o'
        , 'https://www.djmaza.fun/category/indipop-albums/p'
        , 'https://www.djmaza.fun/category/indipop-albums/q'
        , 'https://www.djmaza.fun/category/indipop-albums/r'
        , 'https://www.djmaza.fun/category/indipop-albums/s'
        , 'https://www.djmaza.fun/category/indipop-albums/t'
        , 'https://www.djmaza.fun/category/indipop-albums/u'
        , 'https://www.djmaza.fun/category/indipop-albums/v'
        , 'https://www.djmaza.fun/category/indipop-albums/w'
        , 'https://www.djmaza.fun/category/indipop-albums/x'
        , 'https://www.djmaza.fun/category/indipop-albums/y'
        , 'https://www.djmaza.fun/category/indipop-albums/z']
    base_url = "http://www.djmaza.fun"
    name = "ScrapeIndipopAlbums"
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
            parseAlbum = ParseAlbum("indipop-albums")
            request = scrapy.Request(
                self.base_url + album_link,
                callback=parseAlbum.parseIndividualAlbum)
            yield request
            # album_list_ref = self.db.collection(u'albumslist').document(album_name)
            # self.batch.set(album_list_ref, {u'name': album_name})
