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
        'https://www.studymoose.com/climate-change',
        'https://studymoose.com/addiction',
        'https://studymoose.com/abortion',
        'https://studymoose.com/ageism',
        'https://studymoose.com/assisted-suicide',
        'https://studymoose.com/artificial-intelligence',
        'https://studymoose.com/bullying',
        'https://studymoose.com/capitalism',
        'https://studymoose.com/criminal-justice',
        'https://studymoose.com/capital-punishment',
        'https://studymoose.com/democracy',
        'https://studymoose.com/deforestation',  
        'https://studymoose.com/death-penalty',
        'https://studymoose.com/food-waste',
        'https://studymoose.com/feminism',
        'https://studymoose.com/gender-discrimination',
        'https://studymoose.com/genetically-modified-organisms',
        'https://studymoose.com/guns',
        'https://studymoose.com/globalization',
        'https://studymoose.com/gender-wage-gap-essay-topics',
        'https://studymoose.com/genetic-testing',
        'https://studymoose.com/health-care',
        'https://studymoose.com/human-rights',
        'https://studymoose.com/homelessness',
        'https://studymoose.com/immigration',
        'https://studymoose.com/legalization-of-marijuana',
        'https://studymoose.com/mental-health',
        'https://studymoose.com/medicare',
        'https://studymoose.com/nuclear-power',
        'https://studymoose.com/police',
        'https://studymoose.com/religion',
        'https://studymoose.com/racism',
        'https://studymoose.com/race-and-ethnicity',
        'https://studymoose.com/renewable-energy',
        'https://studymoose.com/social-media',
        'https://studymoose.com/same-sex-marriage',
        'https://studymoose.com/socialism',
        'https://studymoose.com/welfare',
        'https://studymoose.com/water',
    ]

    # Use XPath to parse the response we get.
    def parse(self, response):
        
        # Iterate over every <article> element on the page.
        for essay in response.xpath('//div[contains(@class, "tag-essay")]'):
            # Find the link to the essay.            
            url = essay.xpath('a/@href').extract_first()
            if url is not None:
                # Yield a callback to follow the link.
                yield scrapy.Request(url, callback = self.parse_dir_contents)

        # Get the URL of the previous page.
        next_page = response.xpath('//div[contains(@class, "wp-pagenavi")]')
        next_url = next_page.xpath('a[contains(@class, "nextpostslink")]/@href').extract()[0]
        
        # Recursively call the spider to run on the next page, if it exists.
        if next_url is not None:
            # Request the next page and recursively parse it the same way we did above
            yield scrapy.Request(next_url, callback=self.parse)
        
    def parse_dir_contents(self, response):
        i = 0
        name = response.xpath('//article/h1/text()').extract()
        tags = response.xpath('//a[contains(@class, "post-tags")]/text()').extract()
        for para in response.xpath('//article/p'):
            i+=1
            yield {'Title': name[0], 'Paragraph': str(i), 'Text': para.xpath('text()').extract()[0], 'Tags': tags, 'URL': str(response.url)}
            
# Tell the script how to run the crawler by passing in settings.
# The new settings have to do with scraping etiquette.
process = CrawlerProcess({
    'FEED_FORMAT': 'json',         # Store data in JSON format.
    'FEED_URI': 'studymoose.json',       # Name our storage file.
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
print('Finally Done!')
