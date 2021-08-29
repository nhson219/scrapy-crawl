from itemloaders.processors import MapCompose
import scrapy
import re

from w3lib.html import remove_tags
from khweb_20.news import News
from scrapy.loader import ItemLoader


def format_me(self):
    return self.replace('\n', ' ').replace('  ', ' ').strip()


class BongDaPlusSpider(scrapy.Spider):
    name = "bongda24h"

    start_urls = [
        'https://www.24h.com.vn/bong-da-ngoai-hang-anh-c149.html'
    ]

    # def start_request(self):
    #     urls = [
    #         'https://bongdaplus.vn/bong-da-anh/'
    #     ]
    #     print(1111)
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tmp = response.css(
            '.cate-24h-foot-home-latest-list > article.cate-24h-foot-home-latest-list__box')
        regexp = re.compile('(c\w*)(?=\.html)')
        for item in tmp:
            news = ItemLoader(item=News(), response=response)
            news.default_input_processor = MapCompose(
                remove_tags, format_me)
            item_new = item.css(
                'figure.cate-24h-foot-home-latest-list__ava')
            a_link = item_new.css('a').attrib
            img = item.css('a > img').attrib
            paragraph = item.css(
                'figcaption.cate-24h-foot-home-latest-list__info > div.cate-24h-foot-home-latest-list__sum')
            result = regexp.search(a_link['href'])

            news.add_value('title', a_link['title'])
            news.add_value('description', paragraph.css(
                '::text').get())
            news.add_value('url_img', img['data-original'])
            news.add_value('identify_sign', result.group())

            # get title
        #     print(a_link['title'])

            # get image
        #     print(img['data-original'])

            # get description
        #     print(paragraph.css('::text').get())

            # get inspection sign
        #     print(result.group())
            yield scrapy.Request("https://www.24h.com.vn/" + a_link['href'], callback=self.crawlContent, meta={'news': news})

    def crawlContent(self, response):
        content = response.xpath(
            './/article[@class="cate-24h-foot-arti-deta-info"]/p/text()').extract()
        str = ""
        tmp = str.join(content)
        news = response.meta['news']
        news.add_value('content', tmp)
        return news.load_item()
