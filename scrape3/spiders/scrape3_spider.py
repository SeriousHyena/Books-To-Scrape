import scrapy
from ..items import Scrape2Item

class BookSpider(scrapy.Spider):
    name = 'scrape2'
    start_urls = ['http://books.toscrape.com/index.html']

    def parse(self, response):

        items = Scrape2Item()
        all_books = response.css('article.product_pod')

        for book in all_books:
           
            title = book.css('a::text').extract()
            price = book.css('div.product_price > p.price_color::text').extract()
            avail = book.css(' p.instock.availability::text').extract()
            review_text = book.css('article.product_page > p').extract_first()

            items['title'] = title
            items['price'] = price
            items['avail'] = avail
            items['review_text'] = review_text

            yield items

            all_books = response.css('article.product_pod')
        urls = all_books.css('article.product_pod a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

           #follow pagination link
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        yield {
            'review_text': response.css('article.product_page > p').extract_first(),
            
        }

    #follow pagination link
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)