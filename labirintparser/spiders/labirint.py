import scrapy
from labirintparser.items import LabirintparserItem
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse

class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.labirint.ru/search/{kwargs.get('search')}"]
        #https://www.labirint.ru/search/%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%B8%D0%B2/?stype=0

    def parse(self, response):
        links = response.xpath("//div[@class='product need-watch watched']")
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        # loader = ItemLoader(item=LabirintparserItem(), response=response)
        # loader.add_xpath('name', "//a[@class='product-title-link']/text()")
        # loader.add_xpath('price', "//span[@class='price-val']/text()")
        # loader.add_xpath('author', "//div[@class='product-author']//span/text()")
        # loader.add_xpath('photos',"//img[@class='book-img-cover']@scr")
        # # loader.add_xpath('photos', "//picture[@class='product-poster__main-picture']/source[1]/@srcset | "
        # #                            "//picture[@class='product-poster__main-picture']/source[1]/@data-srcset")
        # loader.add_value('link', response.url)
        # yield loader.load_item()

        name = response.xpath("//a[@class='product-title-link']/text()").get()
        price = response.xpath("//span[@class='price-val']/text()").get()
        author = response.xpath("//div[@class='product-author']//span/text()").get()
        photos = response.xpath("//img[@class='book-img-cover']@scr").getall()
        yield LabirintparserItem(name=name, price=price, author=author, photos=photos)
