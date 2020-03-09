import scrapy
from ..items import Scrape3Item

class BookSpider(scrapy.Spider):
    name = 'scrape3' # the name of the spider to call when running in scrapy
    start_urls = ['http://books.toscrape.com/index.html'] # the start page of the site i want to scrape

    def parse(self, response): # the function that gets the 'href's' to the page containing the book information

        all_books = response.css('article.product_pod') # save the page html for parsing later
        urls = all_books.css('article.product_pod a::attr(href)').extract() # get the href's that take us out to the specific book pages
        for url in urls:
            url = response.urljoin(url) # use absolute referencing to get the book data page
            yield scrapy.Request(url=url, callback=self.parse_details) # save the result and pass it to the "parse_details" function later storing in our mongo database

           #follow pagination link
        next_page_url = response.css('li.next > a::attr(href)').extract_first() # keep following the links to the next page
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
  
        items = Scrape3Item()   # save the page data in the the items containers. for this part I had to study the structure of the page in order to use the 
                                # correct selectors-everything is css selectors

        book_title = response.css('h1::text').extract_first(),
        book_availability = response.css('td::text')[5].extract(),
        book_price = response.css('p.price_color::text').extract_first(),
        review_text = response.css('article.product_page > p::text').extract_first(),

        items['book_title'] = book_title
        items['book_availability'] = book_availability
        items['book_price'] = book_price
        items['review_text'] = review_text

        yield items


    #follow pagination link-this code takes us to the next page of books to parse the hrefs from
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)