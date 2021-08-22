from itemloaders.processors import MapCompose
import scrapy
import re

from w3lib.html import remove_tags
from khweb_20.news import News
from scrapy.loader import ItemLoader


def format_me(self):
    return self.replace('\n', ' ').replace('  ', ' ').strip()


class BongDaPlusSpider(scrapy.Spider):
    name = "bongda"

    start_urls = [
        'https://www.bongda.com.vn/bong-da-anh/'
    ]

    # def start_request(self):
    #     urls = [
    #         'https://bongdaplus.vn/bong-da-anh/'
    #     ]
    #     print(1111)
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tmp = response.css('.list_top_news li')
        regexp = re.compile('(d\d*)(?=\.)')
        for item in tmp:
            news = ItemLoader(item=News(), response=response)
            news.default_input_processor = MapCompose(
                remove_tags, format_me)

            # title
            a_tag = item.css('a:first-child')
            a_link = a_tag.attrib

            # image url
            img_tag = a_tag.css('img')
            img_url = img_tag.attrib['src']

            # description
            paragraph = item.css('div.info_list_top_news > .sapo_news')
            description = paragraph.css('::text').get()

            # identifiy sign
            result = regexp.search(a_link['href'])

            news.add_value('title', a_link['title'])
            news.add_value('description', description)
            news.add_value('url_img', img_url)
            news.add_value('identify_sign', result.group())

            yield scrapy.Request(a_link['href'], callback=self.crawlContent, meta={'news': news})

    def crawlContent(self, response):
        content = response.xpath(
            './/div[@class="exp_content news_details"]//text()').extract()
        str = ""
        tmp = str.join(content)
        news = response.meta['news']
        news.add_value('content', tmp)
        return news.load_item()
