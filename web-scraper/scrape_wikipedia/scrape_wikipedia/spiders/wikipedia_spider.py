import scrapy

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines'
    ]

    def parse(self, response):
        for link in response.css('.contentsPage__section a'):
            yield {
                'link': link.css('a::attr(href)')[0].get()
            }