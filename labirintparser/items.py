# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose



def get_photos_list(photos_list):
    photos_to_download = []
    for photo in photos_list:
        info = photo.split()
        if len(info) == 3:
            if info[1].startswith("//"):
                info[1] = 'https:' + info[1]
            photos_to_download.append(info[1])
        else:
            if info[0].startswith("//"):
                info[0] = 'https:' + info[0]
            photos_to_download.append(info[0])
    return photos_to_download

class LabirintparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=Compose(get_photos_list))
    author = scrapy.Field(output_processor=TakeFirst())

