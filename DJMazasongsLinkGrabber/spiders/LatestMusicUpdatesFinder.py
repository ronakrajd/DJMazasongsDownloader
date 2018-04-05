#
# import scrapy
# import string
# import urllib
# from urllib.request import urlopen, urlretrieve, urlparse, Request
# from urllib.request import urlopen, urlretrieve, urlparse, Request
# from urllib.parse import unquote
# import os
# from scrapy.crawler import CrawlerProcess
# import sys
# import time
# from mutagen.mp3 import MP3
# from mutagen.id3 import ID3, APIC, error
# import firebase_admin
# from firebase_admin import credentials
# from google.cloud import firestore
#
# class LatestMusicUpdatesFinder(scrapy.Spider):
#     # cred = credentials.Certificate(os.getcwd() + "\\serviceAccountKey.json")
#     # firebase_admin.initialize_app(cred)
#     # db = firestore.Client()
#     start_urls = ['http://www.djmaza.fun']
#     base_url = "http://www.djmaza.fun"
#     albums_base_url = "https://www.djmaza.fun/category/bollywood-albums/"
#     # punjabi_albums_base_url = ""
#     name = "LatestMusicUpdatesFinder"
#     headers = {
#         'User-Agent':
#             'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
#     }
#     updates_links = list()
#     tracks_190_links = list()
#     tracks_320_links = list()
#     song_choice_list = list()
#     updates_choice = 0
#     download_choice = 0
#     song_choice = 0
#     curr_char = 'a'
#     download_links = list()
#     base_dir = "C:/Users/rrdoo/Music/Bollywood/"
#     log_fo = open("Failed Files.log", "a")
#     available_albums_fo = open("AvailableAlbums.log", "w")
#     opener = urllib.request.build_opener()
#     opener.addheaders = [(
#         'User-Agent',
#         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
#     )]
#     urllib.request.install_opener(opener)
#     chunk_size = 0
#     batch = db.batch()
#     singles_dict = dict()
#
#     def parse(self, response):
#         self.main_response = response
#         i = 1
#         for update_tags in response.xpath('//div[@class="home-trend-body"]/ul/li'):
#             print(i.__str__() + ". " + update_tags.xpath('.//a/text()').extract_first().strip())
#             if "Albums" in update_tags.xpath('.//div[2]/span/text()').extract_first().strip().split():
#                 self.db_doc = "new_updates"
#                 request = scrapy.Request(
#                     self.base_url + update_tags.xpath('.//a/@href').extract_first(),
#                     callback=self.parseIndividualAlbum)
#                 yield request
#             self.updates_links.append(self.base_url + update_tags.xpath('.//a/@href').extract_first())
#             i = i + 1
#         # print(response.xpath('//div[@class="home-slider-body"]/figure'))
#         for update_tags in response.xpath('//div[@class="home-slider-body"]/figure'):
#             for update in update_tags.xpath('.//h3/a'):
#                 # print(update)
#                 print(i.__str__() + ". " +
#                       update.xpath('.//text()').extract_first().strip())
#                 self.updates_links.append(
#                     self.base_url + update.xpath('.//@href').extract_first())
#                 # print(self.base_url + update.xpath('.//@href').extract_first())
#                 i = i + 1
#         print(i.__str__() + ". " + "Indipop Albums Links Load")
#         i = i + 1
#         print(i.__str__() + ". " + "Bollywood Albums Links Load")
#         i = i + 1
#         print(i.__str__() + ". " + "Punjabi Albums Links Load")
#         i = i + 1
#         print(i.__str__() + ". " + "Punjabi Singles Links Load")
#         self.updates_choice = int(
#             input("Enter Update number to download:")) - 1
#         if self.updates_choice == i-4:
#             self.db_doc = "indipop_albums"
#             self.albums_base_url = "https://www.djmaza.fun/category/indipop-albums/"
#             request = scrapy.Request(
#                 self.albums_base_url + 'a',
#                 callback=self.parseBollywoodAlbumPages)
#             yield request
#         elif self.updates_choice == i-3:
#             self.db_doc = "bollywood_albums"
#             request = scrapy.Request(
#                 self.albums_base_url + 'a',
#                 callback=self.parseBollywoodAlbumPages)
#             yield request
#         elif self.updates_choice == i - 2:
#             self.db_doc = "punjabi_albums"
#             self.albums_base_url = "https://www.djmaza.fun/category/punjabi-albums/"
#             request = scrapy.Request(
#                 self.albums_base_url + 'a',
#                 callback=self.parseBollywoodAlbumPages)
#             yield request
#         elif self.updates_choice == i - 1:
#             self.db_doc = "punjabi_single"
#             self.albums_base_url = "https://www.djmaza.fun/category/punjabi-singles/"
#             print("Starting write to DB")
#             request = scrapy.Request(
#                 self.albums_base_url + 'a',
#                 callback=self.parseBollywoodAlbumPages)
#             yield request
#             print("Finished write to DB")
#         else:
#             request = scrapy.Request(
#                 self.updates_links[self.updates_choice],
#                 callback=self.parseDownloadPage)
#             yield request
#
#     def parseDownloadPage(self, response):
#         print(response.xpath('//div[@class="page-meta-header bg-grey-full"]/h3/text()').extract_first().strip())
#         print("Classifying Updates.....")
#         if (response.xpath(
#                 '//div[@class="page-meta-header bg-grey-full"]/h3/text()')
#                     .extract_first().strip() == 'About Single'):
#             print("Update found to be Singles")
#             self.parseDownloadPageForSingle(response)
#         if (response.xpath(
#                 '//div[@class="page-meta-header bg-grey-full"]/h3/text()')
#                     .extract_first().strip() == 'About Album'):
#             print("Update found to be Album")
#             self.parseDownloadPageForAlbum(response)
#         choice = input("Want to go to main screen(Y/N): ")
#         if choice == 'y' or choice == 'Y':
#             print("choice entered: " + choice)
#             self.parse(self.main_response)
#
#     def parseDownloadPageForSingle(self, response):
#         i = 1
#         file_name = response.xpath('//div[@class="page-down-header bg-grey-full"]/h3/text()').extract_first().strip().split(':')[0]
#         # print(file_name)
#         songMetaTags = response.xpath('//div[@class="page-meta-body"]/ul/li')
#         album_name = "Unclassified"
#         # print(songMetaTags[3])
#         try:
#             album_name = songMetaTags[3].xpath(
#             './/div/a/text()').extract_first().strip()
#         except IndexError:
#             self.log_fo.write("Cannot Find Album name for :" + file_name)
#         for downloadLinkTags in response.xpath(
#                 '//div[@class="col-xs-6 text-center page-down-btns"]'):
#             print(i.__str__() + ". " + ''.join(
#                 downloadLinkTags.xpath('.//a/text()').extract()).strip())
#             self.download_links.append(
#                 downloadLinkTags.xpath('.//a/@href').extract_first())
#             i = i + 1
#
#         self.check_and_create_album(album_name)
#         self.download_choice = int(
#             input("Select Quality to download in: ")) - 1
#         print(self.download_links[self.download_choice])
#         url = unquote(self.download_links[self.download_choice])
#         file_name = url.split('/')[-1]
#         self.downloadFile(url, file_name)
#
#     def parseDownloadPageForAlbum(self, response):
#         # # 	  print("Update found is Album")
#         album_name = response.xpath('//div[@class="page-header bg-grey-full top-header"]/h1/text()').extract_first().split('-')[0]
#         # # 	  print(album_name)
#         for track_list_tags in response.xpath('//div[@class="page-tracklist-body"]/ul'):
#             i = 1
#             # 		  print(track_list_tags.xpath('.//li/div/div/h3'))
#             for track in track_list_tags.xpath('.//li'):
#                 print(i.__str__() + ". " + track.xpath('.//div/div/h3/a/text()').extract_first().strip())
#                 self.tracks_190_links.append(track.xpath('.//div/div[2]/a[2]/@href').extract_first())
#                 self.tracks_320_links.append(track.xpath('.//div/div[2]/a[3]/@href').extract_first())
#                 # 			  print(track.xpath('.//div/div[2]/a[3]/@href').extract_first())
#                 i = i + 1
#         self.check_and_create_album(album_name.strip(), self.base_url + response.xpath('//div[@class="col-sm-5 cover-section"]/img/@src').extract_first())
#         # 	  choice_string = input("Select song to download: ")
#         # 	  print(choice_string)
#         # 	  self.song_choice_list = choice_string.split()
#         self.song_choice_list = [int(x) for x in input("Select song to download: ").split()]
#         for song_choice in self.song_choice_list:
#             print(self.tracks_320_links[song_choice-1])
#             if self.tracks_320_links[song_choice-1] is None:
#                 url = unquote(self.tracks_190_links[song_choice - 1])
#                 file_name = url.split('/')[-1]
#                 self.downloadFile(self.tracks_190_links[song_choice - 1], file_name)
#             else:
#                 url = unquote(self.tracks_320_links[song_choice-1])
#                 file_name = url.split('/')[-1]
#                 self.downloadFile(self.tracks_320_links[song_choice-1], file_name)
#
#     def check_and_create_album(self, album_name, cover_image_link):
#         new_dir = self.base_dir + album_name
#         if os.path.exists(new_dir):
#             self.base_dir = new_dir + '/'
#         else:
#             os.makedirs(new_dir)
#             self.base_dir = new_dir + '/'
#         if os.path.isfile(self.base_dir + 'cover.jpg') is False:
#             try:
#                 urlretrieve(cover_image_link, self.base_dir + 'cover.jpg', self.reporthook)
#             except:
#                 print("Couldn't download cover image......")
#
#     def downloadFile(self, link, filename):
#         if filename == "":
#             filename = "temp.mp3"
#         # print(link)
#         self.request = Request(link, headers=self.headers)
#         file_sizze = self.get_size(link)
#         if file_sizze <= 1000:
#             print("Unknown size of file. Skipping.........")
#             self.log_fo.write("File Name: " + filename + '\n')
#             self.log_fo.write("Fetched URL: " + link + '\n')
#             self.log_fo.write("Received file size: " + str(file_sizze) + '\n')
#             print("File size: {} MB (0 means unknown)".format(
#                 str(file_sizze / 10.0 ** 6)[:5]))
#             return
#         print("File size: {} MB (0 means unknown)".format(
#             str(file_sizze / 10.0 ** 6)[:5]))
#         print("Downloading..." + filename)
#         try:
#             urlretrieve(link, self.base_dir + filename, self.reporthook)
#         except:
#             print("404: Couldn't download file")
#
#         with open(self.base_dir + 'cover.jpg', 'rb') as f:
#             img_data = f.read()
#         mp3_file = MP3(self.base_dir + filename, ID3=ID3)
#         try:
#             mp3_file.add_tags()
#         except:
#             pass
#         mp3_file.tags.add(
#             APIC(
#                 encoding=1,
#                 mime='image/png',
#                 type=3,
#                 desc=u'Cover',
#                 data=img_data
#             )
#         )
#         mp3_file.save()
#         print("Done!")
#
#     def get_size(self, link):
#         try:
#             print(urlopen(self.request).headers.get("Content-Length"))
#             return int(urlopen(self.request).headers.get("Content-Length"))
#         except:
#             return 0
#
#     def reporthook(self, count, block_size, total_size):
#         global start_time
#         if count == 0:
#             start_time = time.time()
#             return
#         duration = (time.time() - start_time) or 0.01
#         progress_size = int(count * block_size)
#         speed = int(progress_size / (1024 * duration))
#         percent = min(int(count * block_size * 100 / total_size), 100)
#         sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" % (
#         percent, progress_size / (1024 * 1024), speed, duration))
#         sys.stdout.flush()
#
#     def parseBollywoodAlbumPages(self, response):
#         list_pages = response.xpath('//ul[@class="pagination"]/li').extract()
#         total_pages = len(list_pages)
#         i = 1
#         if total_pages == 0:
#             print("Total Pages: " + total_pages.__str__())
#             # self.parseArchivePage(response)
#             request = scrapy.Request(
#                 self.albums_base_url + self.curr_char ,
#                 callback=self.parseArchivePage)
#             yield request
#         while i <= total_pages - 1:
#             request = scrapy.Request(
#                 self.albums_base_url + self.curr_char + "?page=" + i.__str__(),
#                 callback=self.parseArchivePage)
#             yield request
#             i = i + 1
#         self.curr_char = chr(ord(self.curr_char) + 1)
#         if self.curr_char != 'z':
#             request = scrapy.Request(
#                 self.albums_base_url + self.curr_char,
#                 callback=self.parseBollywoodAlbumPages)
#             yield request
#         else:
#             print("Writting to Firestore.......")
#             self.batch.commit()
#             print("Writting complete........")
#
#     def parseArchivePage(self, response):
#         print("called parseArchivePage")
#         # print(response.xpath('//div[@class="archive-body"]/figure').extract())
#         for album in response.xpath('//div[@class="archive-body"]/figure'):
#             print((album.xpath(".//h3/a/text()").extract_first()).strip())
#             album_link = (album.xpath(".//h3/a/@href").extract_first()).strip()
#             if self.db_doc != "punjabi_single":
#                 request = scrapy.Request(
#                     self.base_url + album_link,
#                     callback=self.parseIndividualAlbum)
#                 yield request
#             else:
#                 request = scrapy.Request(
#                     self.base_url + album_link,
#                     callback=self.parseSingles)
#                 yield request
#             album_name = (album.xpath(".//h3/a/text()").extract_first()).strip()
#             self.available_albums_fo.write((album.xpath(".//h3/a/text()").extract_first()).strip() + "\n")
#             # album_list_ref = self.db.collection(u'albumslist').document(album_name)
#             # self.batch.set(album_list_ref, {u'name': album_name})
#         self.batch.commit()
#         self.batch = self.db.batch()
#         self.chunk_size = 0
#
#
#     def parseIndividualAlbum(self, response):
#         # print("parsing")
#         album_name = response.xpath('//div[@class="page-header bg-grey-full top-header"]/h1/text()').extract_first().split('-')[0].strip()
#         album_ref = self.db.collection(self.db_doc).document(album_name)
#         # self.batch.set(album_ref, {u'album_name': album_name})
#         print(album_name)
#         album_cover_path = response.xpath('//div[@class="col-sm-5 cover-section"]/img/@src').extract_first()
#         # self.batch.set(album_ref, {u'album_cover_path': album_cover_path})
#         try:
#             zip_dwnld_190_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[0]
#             zip_dwnld_320_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[1]
#             # self.batch.set(album_ref, {u'album_zip_190_link': zip_dwnld_190_link})
#             # self.batch.set(album_ref, {u'album_zip_320_link': zip_dwnld_320_link})
#         except:
#             zip_dwnld_190_link = ""
#             zip_dwnld_320_link = ""
#         self.batch.set(album_ref, {u'album_name': album_name,
#                                    u'album_cover_path': album_cover_path,
#                                    u'album_zip_190_link': zip_dwnld_190_link,
#                                    u'album_zip_320_link': zip_dwnld_320_link})
#         self.chunk_size = self.chunk_size + 4
#         print(album_cover_path)
#         print(str(response.request.url))
#         print(zip_dwnld_190_link)
#         print(zip_dwnld_320_link)
#         for track_list_tags in response.xpath('//div[@class="page-tracklist-body"]/ul'):
#             i = 1
#             # 		  print(track_list_tags.xpath('.//li/div/div/h3'))
#             for track in track_list_tags.xpath('.//li'):
#                 song_name = track.xpath('.//div/div/h3/a/text()').extract_first().strip()
#                 album_songs_ref = self.db.collection(self.db_doc).document(album_name).collection(u'songs').document(song_name)
#                 song_artists = track.xpath('.//div/div/span/a/text()').extract()
#                 song_artists = list(map(str.strip, song_artists))
#                 song_number = i
#                 try:
#                     song_190kbps_link = track.xpath('.//div/div[2]/a[2]/@href').extract_first()
#                     song_320kbps_link = track.xpath('.//div/div[2]/a[3]/@href').extract_first()
#                 except:
#                     song_190kbps_link = ""
#                     song_320kbps_link = ""
#                 # 			  print(track.xpath('.//div/div[2]/a[3]/@href').extract_first())
#                 self.batch.set(album_songs_ref, {u'song_number': song_number,
#                                            u'song_name': song_name,
#                                            u'song_artists': song_artists,
#                                            u'song_190kbps_link': song_190kbps_link,
#                                         u'song_320kbps_link': song_320kbps_link})
#                 i = i + 1
#
#             self.batch.commit()
#             self.batch = self.db.batch()
#             self.chunk_size = 0
#             print("Writting complete.....")
#
#     def parseSingles(self, response):
#         song_190kbps_link = None
#         song_320kbps_link = None
#         song_name = response.xpath('//div[@class="page-header bg-grey-full top-header"]/h1/text()').extract_first().strip().split('-')[0]
#         song_name = song_name.strip()
#         song_cover_path = response.xpath('//div[@class="col-sm-5 cover-section"]/img/@src').extract_first()
#         songMetaTags = response.xpath('//div[@class="page-meta-body"]/ul/li')
#         try:
#             song_artists = songMetaTags[0].xpath('.//div[2]/a/text()').extract()
#             song_artists = list(map(str.strip, song_artists))
#             song_duration = songMetaTags[-1].xpath('.//div[2]/a/text()').extract_first()
#             # print(response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]').extract())
#             song_190kbps_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[
#                 0]
#             song_320kbps_link = response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]/a/@href').extract()[
#                 1]
#         except IndexError:
#             self.log_fo.write("Cannot Find Album name for :" + song_name)
#         # print(song_name)
#         # print(song_artists)
#         # print(song_190kbps_link)
#         # print(song_320kbps_link)
#         # print(song_duration)
#         single_song_detail_dict = {
#             u'song_name': song_name,
#             u'song_artists': song_artists,
#             u'song_190kbps_link': song_190kbps_link,
#             u'song_320kbps_link': song_320kbps_link,
#             u'song_cover_path': song_cover_path,
#             u'song_url': str(response.request.url)
#         }
#         self.singles_dict[song_name] = single_song_detail_dict
#         singles_song_ref = self.db.collection(self.db_doc).document(song_name)
#         self.batch.set(singles_song_ref, self.singles_dict[song_name])
#         self.batch.commit()
#
#     def close(spider, reason):
#         print("Write complete")
#
# # process = CrawlerProcess({
# #     'USER_AGENT':
# #         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# # })
# #
# # process.crawl(LatestMusicUpdatesFinder)
# # process.start()