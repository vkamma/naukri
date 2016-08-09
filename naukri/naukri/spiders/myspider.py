from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
from naukri.items import NaukriItem


class MySpider(Spider):
    name = 'job'
    allowed_domains = ['naukri.com', ]

    # Start on the main page
    start_urls =['http://www.naukri.com/jobs-by-location', ]

    def parse(self, response):

        """ This function parses a main page.
            @raises CloseSpider exception if the bandwidth of the response is very high
            @forloop loops the urls of the top cities in the response returned for the Request sent using urls in the start_urls
            @yields requests using urls parsed on the page and calls the parse_page() on every url
        """

        #self.logger.info('Parse function called on %s', response.url)

        if b'Bandwidth exceeded' in response.body:
            raise CloseSpider('bandwidth_exceeded')

        for href in response.css('.multiColumn.colCount_four a::attr(href)'):
            page_url = str(href.extract())
            yield Request(page_url, callback=self.parse_page)


    def parse_page(self, response):

        """ This function parses a jobs page.
            @raises CloseSpider exception if the bandwidth of the response is very high
            @forloop loops the job_urls in the response returned for the Request sent using urls requested by parse()
            @yields requests on job_urls parsed in the response and calls the parse_page()
            @forloop loops the urls in the response returned for the Request sent using urls requested by parse()
            @yields requests on next_page_urls parsed in the response and calls the parse_page()
        """

        #self.logger.info('Parse function called on %s', response.url)

        if b'Bandwidth exceeded' in response.body:
            raise CloseSpider('bandwidth_exceeded')

        for href in response.xpath('//*[@itemtype="http://schema.org/JobPosting"]/a/@href'):
            job_url = response.urljoin(href.extract())
            yield Request(job_url, callback=self.parse_post)

        for href in response.xpath('//div[@class="pagination"]/a/@href'):
            next_page_url = str(href.extract())
            yield Request(next_page_url, callback=self.parse_page)

    def parse_post(self, response):

        """ This function parses a job page.
            @raises CloseSpider exception if the bandwidth of the response is very high
            @url url of the response by the parse_page()
            @yields items 1
            @scrapes link desig org location of the job
        """

        #self.logger.info('Parse function called on %s', response.url)

        if b'Bandwidth exceeded' in response.body:
            raise CloseSpider('bandwidth_exceeded')
        url = response.xpath('//div[@class="hdsec"]/a/@href')
        item = NaukriItem()
        item['link'] = response.urljoin(url.extract()),
        item['desig'] = response.xpath('//h1[@itemprop="title"]/text()').extract(),
        item['org'] = response.xpath('//a[@class="pHead"]/text()').extract(),
        item['location'] = response.xpath('//div[@class="loc"]/a/text()').extract()
        yield item
