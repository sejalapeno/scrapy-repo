import scrapy

class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.in"]
    #start_urls = ["https://www.audible.in/search/"]

    def start_requests(self):
        yield scrapy.Request(url="https://www.audible.in/search/",
                       callback=self.parse,
                       headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'})
    def parse(self, response):
        product_container = response.xpath('//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')
        #product_container = response.xpath('//div[@class="adbl-impression-container "]/li')
        #product_container=response.xpath('//*[@id="product-list-a11y-skiplink-target"]')
        #product_container=response.xpath('//*[@id="center-3"]/div/div')
        for product in product_container:
            #book_title=product.xpath('.//h3[contains(@class,"bc-heading")]/a/text()').get()
            book_title=product.xpath('.//li[@class="bc-list-item"]/h3/a/text()').get()
            book_author=product.xpath('.//li[contains(@class,"authorLabel")]/span/a/text()').getall()
            book_length=product.xpath('.//li[contains(@class,"runtimeLabel")]/span/text()').get()

            yield{
                'title':book_title,
                'author':book_author,
                'length':book_length,
                'user_agent':response.request.headers['User-Agent']
            }

            pagination=response.xpath(
                '//ul[contains(@class,"pagingElements")]'
            )

            next_page_url=pagination.xpath('.//span[contains(@class,"nextButton")]/a/@href').get()
            
            if next_page_url:
                yield response.follow(url=next_page_url,callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'})