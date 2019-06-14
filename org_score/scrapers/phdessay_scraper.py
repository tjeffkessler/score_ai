# Importing in each cell because of the kernel restarts.
import scrapy
import re
from datetime import datetime
from scrapy.crawler import CrawlerProcess

class EssaySpider(scrapy.Spider):
    # Naming the spider is important if you are running more than one spider of
    # this class simultaneously.
    name = "Essay"
    
    # URL(s) to start with.
    start_urls = [
        'https://phdessay.com/search/?s=climate+change',
        'https://phdessay.com/search/?s=addiction',
        'https://phdessay.com/search/?s=abortion',
        'https://phdessay.com/search/?s=ageism',
        'https://phdessay.com/search/?s=assisted+suicide',
        'https://phdessay.com/search/?s=artificial+intelligence',
        'https://phdessay.com/search/?s=bullying',
        'https://phdessay.com/search/?s=capitalism',
        'https://phdessay.com/search/?s=criminal+justice',
        'https://phdessay.com/search/?s=capital+punishment',
        'https://phdessay.com/search/?s=democracy',
        'https://phdessay.com/search/?s=deforestation',
        'https://phdessay.com/search/?s=death+penalty',
        'https://phdessay.com/search/?s=food+waste',
        'https://phdessay.com/search/?s=feminism',
        'https://phdessay.com/search/?s=gender+discrimination',
        'https://phdessay.com/search/?s=genetically+modified+organisms',
        'https://phdessay.com/search/?s=guns',
        'https://phdessay.com/search/?s=globalization',
        'https://phdessay.com/search/?s=gender+pay+gap',
        'https://phdessay.com/search/?s=genetic+testing',
        'https://phdessay.com/search/?s=health+care',
        'https://phdessay.com/search/?s=human+rights',
        'https://phdessay.com/search/?s=homelessness',
        'https://phdessay.com/search/?s=immigration',
        'https://phdessay.com/search/?s=marijuana+legalization',
        'https://phdessay.com/search/?s=mental+health',
        'https://phdessay.com/search/?s=medicare',
        'https://phdessay.com/search/?s=nuclear+power',
        'https://phdessay.com/search/?s=police',
        'https://phdessay.com/search/?s=religion',
        'https://phdessay.com/search/?s=racism',
        'https://phdessay.com/search/?s=race+and+ethnicity',
        'https://phdessay.com/search/?s=renewable+energy',
        'https://phdessay.com/search/?s=social+media',
        'https://phdessay.com/search/?s=same+sex+marriage',
        'https://phdessay.com/search/?s=socialism',
        'https://phdessay.com/search/?s=welfare',
        'https://phdessay.com/search/?s=water']


    # Use XPath to parse the response we get.
    def parse(self, response):
        # Iterate over every <article> element on the page.
        for essay in response.xpath('//div[contains(@class, "search-list-item")]'):
            # Find the link to the essay.            
            url = essay.xpath('a/@href').extract_first()
            if url is not None:
                # Yield a callback to follow the link.
                yield scrapy.Request(url, callback = self.parse_dir_contents)

        # Get the URL of the previous page.
        # next_page = response.xpath('//div[contains(@class, "wp-pagenavi")]')
        for j in range(1, 100):
            next_url = 'https://phdessay.com/search/?s=climate+change&page=' + str(j)
        # Recursively call the spider to run on the next page, if it exists.
            # Request the next page and recursively parse it the same way we did above
            yield scrapy.Request(next_url, callback=self.parse)
        
    def parse_dir_contents(self, response):
        i = 0
        name = response.xpath('//h1/text()').extract()
        tags = response.xpath('//a[contains(@class, "post-tags")]/text()').extract()
        for para in response.xpath('//div[contains(@class, "article-single-content")]/p'):
            i+=1
            yield {'Title': name[0], 'Paragraph': str(i), 'Text': para.xpath('text()').extract()[0], 'Tags': tags, 'URL': response.url}
            
# Tell the script how to run the crawler by passing in settings.
# The new settings have to do with scraping etiquette.
process = CrawlerProcess({
    'FEED_FORMAT': 'json',         # Store data in JSON format.
    'FEED_URI': 'phdessay.json',       # Name our storage file.
    'LOG_ENABLED': False,          # Turn off logging for now.
    'ROBOTSTXT_OBEY': True,
    'USER_AGENT': 'tjeffkessler (t.jeffkessler@gmail.com)',
    'AUTOTHROTTLE_ENABLED': True,
    'HTTPCACHE_ENABLED': True, 
    'DEBUG': True
})

# Start the crawler with our spider.
process.crawl(EssaySpider)
process.start()
print('Finished scraping at {}'.format(datetime.now()))

