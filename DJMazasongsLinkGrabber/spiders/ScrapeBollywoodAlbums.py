import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from .ParseAlbum import ParseAlbum
from .ParseSingles import ParseSingles
import os

class ScrapeBollywoodAlbums(scrapy.Spider):
    start_urls = ['https://www.djmaza.fun/category/bollywood-albums/a'
        , 'https://www.djmaza.fun/category/bollywood-albums/b'
        , 'https://www.djmaza.fun/category/bollywood-albums/c'
        , 'https://www.djmaza.fun/category/bollywood-albums/d'
        , 'https://www.djmaza.fun/category/bollywood-albums/e'
        , 'https://www.djmaza.fun/category/bollywood-albums/f'
        , 'https://www.djmaza.fun/category/bollywood-albums/g'
        , 'https://www.djmaza.fun/category/bollywood-albums/h'
        , 'https://www.djmaza.fun/category/bollywood-albums/i'
        , 'https://www.djmaza.fun/category/bollywood-albums/j'
        , 'https://www.djmaza.fun/category/bollywood-albums/k'
        , 'https://www.djmaza.fun/category/bollywood-albums/l'
        , 'https://www.djmaza.fun/category/bollywood-albums/m'
        , 'https://www.djmaza.fun/category/bollywood-albums/n'
        , 'https://www.djmaza.fun/category/bollywood-albums/o'
        , 'https://www.djmaza.fun/category/bollywood-albums/p'
        , 'https://www.djmaza.fun/category/bollywood-albums/q'
        , 'https://www.djmaza.fun/category/bollywood-albums/r'
        , 'https://www.djmaza.fun/category/bollywood-albums/s'
        , 'https://www.djmaza.fun/category/bollywood-albums/t'
        , 'https://www.djmaza.fun/category/bollywood-albums/u'
        , 'https://www.djmaza.fun/category/bollywood-albums/v'
        , 'https://www.djmaza.fun/category/bollywood-albums/w'
        , 'https://www.djmaza.fun/category/bollywood-albums/x'
        , 'https://www.djmaza.fun/category/bollywood-albums/y'
        , 'https://www.djmaza.fun/category/bollywood-albums/z']
    base_url = "http://www.djmaza.fun"
    name = "ScrapeBollywoodAlbums"
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
            parseAlbum = ParseAlbum("bollywood-albums")
            request = scrapy.Request(
                self.base_url + album_link,
                callback=parseAlbum.parseIndividualAlbum)
            yield request
            # album_list_ref = self.db.collection(u'albumslist').document(album_name)
            # self.batch.set(album_list_ref, {u'name': album_name})