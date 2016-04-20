import scrapy
import urllib

from rmp_scraper.items import ProfessorItem

class ProfessorSpider(scrapy.Spider):
    name = "rmp_scraper"
    allowed_domains = ["ratemyprofessors.com"]
    university = "Add University Name Here" # ex. Pennsylvania State University
    searchUrl = "http://www.ratemyprofessors.com/search.jsp?query=" + urllib.quote_plus(university)
    start_urls = [searchUrl]

    def parse(self, response):
        for href in response.xpath('//*[@id="searchResultsBox"]/div/ul/li/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_prof_page)

        next_page = response.css("#searchResultsBox > div.result-pager > div > a.nextLink::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_next)

    def parse_next(self, response):
        for href in response.xpath('//*[@id="searchResultsBox"]/div/ul/li/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_prof_page)

        next_page = response.css("#searchResultsBox > div.result-pager > div > a.nextLink::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_next)

    def parse_prof_page(self, response):
        item = ProfessorItem()
        item['url'] = response.url
        item['fname'] = response.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/h1/span[1]/text()').extract_first(default='n/a').strip()
        item['fname2'] = response.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/h1/span[2]/text()').extract_first(default='n/a').strip()
        item['lname'] = response.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/h1/span[3]/text()').extract_first(default='n/a').strip()
        item['campus'] = response.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[2]/h2/a/text()').extract_first(default='n/a').strip()
        item['quality'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[1]/div[1]/div/text()').extract_first(default='n/a').strip()
        item['avg'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/text()').extract_first(default='n/a').strip()
        item['help'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/text()').extract_first(default='n/a').strip()
        item['clarity'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/text()').extract_first(default='n/a').strip()
        item['easiness'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/text()').extract_first(default='n/a').strip()
        item['chili'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[1]/div[3]/div/figure/img/@src').extract_first(default='n/a').strip()

        # GET 3 COMMENTS
        comment_text = response.css('td.comments > p::text').extract()
        comment_text = comment_text[:3]

        for i in range(len(comment_text)):
            comment_text[i] = comment_text[i].strip()

        # GET 3 COMMENT TYPES
        comment_type = response.css('span.rating-type::text').extract()
        comment_type = comment_type[:3]

        for i in range(len(comment_type)):
            comment_type[i] = comment_type[i].strip().upper()

        # GET 3 COMMENT COURSES
        comment_course = response.css('td.class > span.name > span::text').extract()
        comment_course = comment_course[:3]

        for i in range(len(comment_course)):
            comment_course[i] = comment_course[i].strip()

        item['comment_text'] = comment_text
        item['comment_type'] = comment_type
        item['comment_course'] = comment_course
        item['tag'] = response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[2]/div[2]/span[1]/text()').extract_first(default='n/a').strip()
        yield item