from itemloaders.processors import MapCompose
import scrapy
import re

from w3lib.html import remove_tags
from khweb_20.news import News
from scrapy.loader import ItemLoader


def format_me(self):
    return self.replace('\n', ' ').replace('  ', ' ').strip()


class BongDaPlusSpider(scrapy.Spider):
    name = "bongdaplus"

    start_urls = [
        'https://bongdaplus.vn/bong-da-anh/'
    ]

    # def start_request(self):
    #     urls = [
    #         'https://bongdaplus.vn/bong-da-anh/'
    #     ]
    #     print(1111)
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tmp = response.css('.lastestbox > .newslst > .lst li.news')
        regexp = re.compile('(\d*)(?=\.)')
        for item in tmp:
            news = ItemLoader(item=News(), response=response)
            news.default_input_processor = MapCompose(
                remove_tags, format_me)
            a_link = item.css('a:first-child').attrib
            img = item.css('a:first-child img').attrib
            paragraph = item.css('p.desc')
            result = regexp.search(a_link['href'])

            news.add_value('title', a_link['title'])
            news.add_value('description', paragraph.css(
                '::text').get())
            news.add_value('url_img', img['data-src'])
            news.add_value('identify_sign', result.group())

            # get title
            # print(a_link['title'])

            # get image
            # print(img['data-src'])

            # get description
            # print(paragraph.css('::text').get())

            # get inspection sign
            # print(result.group())
            yield scrapy.Request("https://bongdaplus.vn/" + a_link['href'], callback=self.crawlContent, meta={'news': news})

    def crawlContent(self, response):
        content = response.xpath(
            './/div[@id="postContent"]/p/text()').extract()
        str = ""
        tmp = str.join(content)
        news = response.meta['news']
        news.add_value('content', tmp)
        return news.load_item()
