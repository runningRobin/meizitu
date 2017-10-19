import scrapy
from scrapy import selector
import urllib
import os


class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domain = ['meizitu.com']
    start_url = 'http://www.meizitu.com/a/more_{page}.html'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    referer = 'http://www.meizitu.com'
    headers = {'User-Agent': user_agent, 'Referer': referer}
    download_path = 'D:/meizitu.com/'

    def start_requests(self):
        for page in range(1, 73):
            yield scrapy.Request(url=self.start_url.format(page=page), headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response):
        lists = response.selector.xpath('//ul[@class="wp-list clearfix"]/li/div/div/a')
        for url in lists:
            info_url = url.xpath('@href').extract()[0]
            yield scrapy.Request(url=info_url, headers=self.headers, method='GET', callback=self.detail_parse)

    def detail_parse(self, response):
        all_img = response.selector.xpath('//div[@id="picture"]/p/img')
        for img_url in all_img:
            img_url = img_url.xpath('@src').extract()[0]
            name = img_url[-18:-4].replace('/', '')

            myheaders = [('User - Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'), ]
            opener = request.build_opener()
            opener.addheaders = myheaders
            request.install_opener(opener)

            try:
                urllib.request.urlretrieve(img_url, self.download_path + name + '.jpg')
                print('%s download successful!' % img_url)
            except:
                print('%s download failed!' % img_url)