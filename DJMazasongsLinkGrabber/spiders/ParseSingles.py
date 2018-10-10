import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import datetime
import os

from DJMazasongsLinkGrabber.spiders.ParseAlbum import ParseAlbum


class ParseSingles:
    # cred = credentials.Certificate(os.getcwd() + "\\serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    db = firestore.Client()
    db_doc = "temp"
    batch = db.batch()
    singles_dict = dict()

    def __init__(self, db_doc):
        self.db_doc = db_doc

    def parseSingles(self, response):
        song_190kbps_link = None
        song_320kbps_link = None
        if "Album" in response.xpath('//div[@class="page-meta"]/div[@class="page-meta-header bg-grey-full"]/h3/text()').extract_first().strip():
            parseAlbum = ParseAlbum("new_updates")
            parseAlbum.parseIndividualAlbum(response)
            return
        song_name = response.xpath('//div[@class="page-header bg-grey-full top-header"]/h1/text()').extract_first().strip().split('-')[0]
        song_name = song_name.strip()
        song_cover_path = response.xpath('//div[@class="col-sm-5 cover-section"]/img/@src').extract_first()
        songMetaTags = response.xpath('//div[@class="page-meta-body"]/ul/li')
        try:
            song_artists = songMetaTags[0].xpath('.//div[2]/a/text()').extract()
            song_artists = list(map(str.strip, song_artists))
            song_duration = songMetaTags[-1].xpath('.//div[2]/a/text()').extract_first()
            # print(response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]').extract())
            song_190kbps_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[
                0]
            song_320kbps_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[
                1]
        except:
            # self.log_fo.write("Cannot Find Album name for :" + song_name)
            print("")
        # print(song_name)
        # print(song_artists)
        # print(song_190kbps_link)
        # print(song_320kbps_link)
        # print(song_duration)
        single_song_detail_dict = {
            u'song_name': song_name,
            u'song_artists': song_artists,
            u'song_190kbps_link': song_190kbps_link,
            u'song_320kbps_link': song_320kbps_link,
            u'song_cover_path': song_cover_path,
            u'song_url': str(response.request.url),
            u'create_ts': datetime.datetime.now()}
        }
        self.singles_dict[song_name] = single_song_detail_dict
        singles_song_ref = self.db.collection(self.db_doc).document("singles").document(song_name)
        self.batch.set(singles_song_ref, self.singles_dict[song_name])
        self.batch.commit()
