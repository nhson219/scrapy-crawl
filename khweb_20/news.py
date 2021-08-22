# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import Join, MapCompose, TakeFirst


class News(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field(output_processor=TakeFirst())
    description = Field(output_processor=TakeFirst())
    content = Field(output_processor=TakeFirst())
    url_img = Field(output_processor=TakeFirst())
    identify_sign = Field(output_processor=TakeFirst())
    pass
