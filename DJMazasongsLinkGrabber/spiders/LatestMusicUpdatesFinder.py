import scrapy
import string
import urllib
from urllib.request import urlopen, urlretrieve, urlparse, Request
from urllib.parse import unquote
import os

class LatestMusicUpdatesFinder(scrapy.Spider):
    start_urls = ['http://www.djmaza.fun']
    base_url = "http://www.djmaza.fun"
    name = "LatestMusicUpdatesFinder"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    updates_links = list()
    updates_choice = 0
    download_choice = 0
    download_links = list()
    base_dir = "C:/Users/rrdoo/Music/Bollywood/"

    def parse(self, response):
        for update_tags in response.xpath('//div[@class="home-trend-body"]'):
            i = 1
            for update in update_tags.xpath('.//a'):
                print(i.__str__() + ". " + update.xpath('.//text()').extract_first().strip())
                self.updates_links.append(self.base_url + update.xpath('.//@href').extract_first())
                # print(self.base_url + update.xpath('.//@href').extract_first())
                i = i+1

        self.updates_choice = int(input("Enter Update number to download:")) - 1
        request = scrapy.Request(self.updates_links[self.updates_choice], callback=self.parseDownloadPage)
        yield request

    def parseDownloadPage(self, response):
        # print(response.xpath('//div[@class="page-meta-header bg-grey-full"]/h3/text()').extract_first().strip())
        if(response.xpath('//div[@class="page-meta-header bg-grey-full"]/h3/text()').extract_first().strip() == 'About Single'):
            self.parseDownloadPageForSingle(response)
        # else:
        #     self.parseDownloadPageForAlbum(self, response)

    def parseDownloadPageForSingle(self, response):
        i = 1
        # file_name = response.xpath('//div[@class="page-down-header bg-grey-full"]/h3/text()').extract_first().strip().split(':')[0]
        # print(file_name)
        songMetaTags = response.xpath('//div[@class="page-meta-body"]/ul/li');
        # print(songMetaTags[3])
        album_name = songMetaTags[3].xpath('.//div/a/text()').extract_first().strip()
        for downloadLinkTags in response.xpath('//div[@class="col-xs-6 text-center page-down-btns"]'):
            print(i.__str__() + ". " + ''.join(downloadLinkTags.xpath('.//a/text()').extract()).strip())
            self.download_links.append(downloadLinkTags.xpath('.//a/@href').extract_first())
            i = i + 1

        self.check_and_create_album(album_name)
        self.download_choice = int(input("Select Quality to download in: ")) - 1
        print(self.download_links[self.download_choice])
        url = unquote(self.download_links[self.download_choice])
        file_name = url.split('/')[-1]
        self.downloadFile(url, file_name)
    # def parseDownloadPageForAlbum(self, response):
    #
    #     return

    def check_and_create_album(self, album_name):
        new_dir = self.base_dir + album_name
        if os.path.exists(new_dir):
            self.base_dir = new_dir + '/'
        else:
            os.makedirs(new_dir)
            self.base_dir = new_dir + '/'

    def downloadFile(self, link, filename):
        if filename == "":
            filename = "temp.mp3";
        # print(link)
        self.request = Request(link, headers=self.headers)
        print ("File size: {} MB (0 means unknown)".format(str(self.get_size(link) / 10.0 ** 6)[:5]))
        print ("Downloading...")
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urlretrieve(link, self.base_dir + filename)
        except:
            print ("404: Couldn't download file")
        print("Done!")

    def get_size(self, link):
        try:

            print(urlopen(self.request).headers.get("Content-Length"))
            return int(urlopen(self.request).headers.get("Content-Length"))
        except:
            return 0