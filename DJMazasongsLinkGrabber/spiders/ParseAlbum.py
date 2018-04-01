import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import os

class ParseAlbum:
    # cred = credentials.Certificate(os.getcwd() + "\\serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    cred = credentials.Certificate("/app/__main__.egg/DJMazasongsLinkGrabber/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()
    db = firestore.Client()
    db_doc = "temp"
    batch = db.batch()

    def __init__(self, db_doc):
        self.db_doc = db_doc

    def parseIndividualAlbum(self, response):
        # print("parsing")
        album_name = response.xpath('//div[@class="page-header bg-grey-full top-header"]/h1/text()').extract_first().split('-')[0].strip()
        album_ref = self.db.collection(self.db_doc).document(album_name)
        # self.batch.set(album_ref, {u'album_name': album_name})
        print(album_name)
        album_cover_path = response.xpath('//div[@class="col-sm-5 cover-section"]/img/@src').extract_first()
        # self.batch.set(album_ref, {u'album_cover_path': album_cover_path})
        try:
            zip_dwnld_190_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[0]
            zip_dwnld_320_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[1]
            # self.batch.set(album_ref, {u'album_zip_190_link': zip_dwnld_190_link})
            # self.batch.set(album_ref, {u'album_zip_320_link': zip_dwnld_320_link})
        except:
            zip_dwnld_190_link = ""
            zip_dwnld_320_link = ""
        self.batch.set(album_ref, {u'album_name': album_name,
                                   u'album_cover_path': album_cover_path,
                                   u'album_zip_190_link': zip_dwnld_190_link,
                                   u'album_zip_320_link': zip_dwnld_320_link})
        # self.chunk_size = self.chunk_size + 4
        print(album_cover_path)
        print(str(response.request.url))
        print(zip_dwnld_190_link)
        print(zip_dwnld_320_link)
        for track_list_tags in response.xpath('//div[@class="page-tracklist-body"]/ul'):
            i = 1
            # 		  print(track_list_tags.xpath('.//li/div/div/h3'))
            for track in track_list_tags.xpath('.//li'):
                song_name = track.xpath('.//div/div/h3/a/text()').extract_first().strip()
                album_songs_ref = self.db.collection(self.db_doc).document(album_name).collection(u'songs').document(song_name)
                song_artists = track.xpath('.//div/div/span/a/text()').extract()
                song_artists = list(map(str.strip, song_artists))
                song_number = i
                try:
                    song_190kbps_link = track.xpath('.//div/div[2]/a[2]/@href').extract_first()
                    song_320kbps_link = track.xpath('.//div/div[2]/a[3]/@href').extract_first()
                except:
                    song_190kbps_link = ""
                    song_320kbps_link = ""
                # 			  print(track.xpath('.//div/div[2]/a[3]/@href').extract_first())
                self.batch.set(album_songs_ref, {u'song_number': song_number,
                                           u'song_name': song_name,
                                           u'song_artists': song_artists,
                                           u'song_190kbps_link': song_190kbps_link,
                                        u'song_320kbps_link': song_320kbps_link})
                i = i + 1

            self.batch.commit()
            self.batch = self.db.batch()
            self.chunk_size = 0
            print("Writting complete.....")