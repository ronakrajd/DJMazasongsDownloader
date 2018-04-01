import scrapy
import string
from scrapy.crawler import CrawlerProcess
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import os
import json
from google.oauth2 import service_account


class ParseAlbum:
    # cred = credentials.Certificate(os.getcwd() + "\\serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    info = json.loads({
  "type": "service_account",
  "project_id": "songslibrary-b17ec",
  "private_key_id": "04c0dc22c120ec95aa45a240950c09ded8bf02ad",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCyMMR7ctGjtEkL\nEdMXwpwz6M7LD8YBb6MjDdYijRuAnx/u6rd5qqCM34BpT3Wbc6Krdg5fJXH0rdZQ\nruqiPbO0p6I/cZ4Sz5mJtCKOVdggfOz6lYr+FoiH8Jz3D5CvVKATd563weK2WPmT\nXsbmvMgnRUzYgtTueHUsZejn6OgG3ZEnJVzJ9cymazNjeWKvY2ENkn+pAy2hRCx8\nJiuIAnFgMHjekMZYeVkayW5e2ssEr+Olwvnm04yVe9DXaCD8czpMJxv9sAid8V3s\n+ZhTAalKdJg4yk+MFjSKHKeuF/NCm7pzKbcuFUFlx6gsfHsUN7RkXA0w0MhkJ+NH\nopzS/qc1AgMBAAECggEAWOkNeN1jLjBMS/oyXoYrw5jz6g1uSpQmDd0fDjFjWivL\n1r4GG26gWnpAzAsqTw0FS1GGPUJlWGWO7MZCa/6mlssYIVjzO0abwUKBBY1e4GMF\nKcmJR1v99vp/j6UUF+/9SYljyCO1mC/QJBDj5QioRDQHcnbhgTXYnXUiH+kuMRHy\n2a57Q6SGnynN5g9FpIwEFmSdA1Yjxx2zBlSyM2QtqbQtZDNZi67Clp05ivpJO0K0\nc0MBtS9tCLFyVLm50tbwyO4TsgGtLKlbX2sxbpqYrVOGgBBQ8zzfhswBdmwGFJGt\nvdeiTb9hbzm2zunMuUzjjGcUlB0Vh++NTB6KMPr2VwKBgQDcBnE3BffIC0RX4xiZ\niN1p/p9n6N0t/Vd2aKDRlE1feL4M8AP4M7zb84AeViED15D4L3Hb4rWmhVFQ0/x8\nC+t6Yocg8f8VxxKneCrGDRYRufSg8O7KWgHma5NzKCGAdhcne65j0Xfjzap5eoaM\nW/NDpDbfjJHAkaA//xvkI+WutwKBgQDPU0IkwTX4lW79aojs6b6Yp1kOtXsRRbYS\n+3Q32o0LsGe3GG5onyJsXa9fin+ODeeV3D3z+I+JjSRxxZDpfo0dfjuf33HfNthC\n/F0so/sjM0poYlLYF6+9jvZtmjUm3ElfIBn+vjp5FGVsuWql/rddqH5ywU4HcUox\naiLFWr0tcwKBgHpLjmQiCg6DzLH5BTRZsY/3ugycj0u/s/yZvUGgZ704NJKmWd58\ni23KE51JDELBb8+zN1sb0RHEqmT93ynnyjQVTbyPJdSp+QFitousvGaP8JwALwoE\nK2gyxRtN5AkuGkKU6WKMDFJvf2DULLMZbMZdIS7ySBU8HFFV79/H4CNTAoGAY70C\nDPyGIliBVJhz1sV8U6PuTA0yb1TCCs+9UUFqqTzsKEEwnFQyEz/epm/SfVxjFM0n\nYL8rDllANxt8Y1fmO1IHDRpJhcC0uUT+7gLVRlHecekbQanjeaXVF1UgTNmc0o52\n8v5A0w7k3DE3BTRMslnkuwATsbDmqG8O2zKT39ECgYBPtpyIuWSDDKQ1jMZjEpuY\n+d3ocjVjyZEMRAksDgYkVb9Al9uL6Lit0hJem6Y+Hg7uWF9yTfqgzW8meKZP1YbT\newf809ITrwyLea98d1dhrzn2F1hVuCL+GzXLmiGHq0d8TeTOnGoBqqioWQqX2JsW\n1TrtiKtPUOBcPdMT5Kq5eA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-js0nh@songslibrary-b17ec.iam.gserviceaccount.com",
  "client_id": "114423172587306927942",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-js0nh%40songslibrary-b17ec.iam.gserviceaccount.com"
})
    cred = service_account.Credentials.from_service_account_info(info)
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