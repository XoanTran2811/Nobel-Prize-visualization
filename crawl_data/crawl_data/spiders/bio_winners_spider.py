import scrapy
import re

BASE_URL = 'https://en.wikipedia.org'

class NWinnerItemBio(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()


#scrape the image URLs and bio text
class NWinnerSpiderBio(scrapy.Spider):

    name = 'bio_winners'
    allowed_domains =['en.wikipedia.org']
    start_urls =['https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']

    #custom_settings = {'ITEM_PIPELINES':{'nobel_winners.pipelines.ImagesPipeline':1}}

    def parse (self, response):
        
        # filename = response.url.split('/')[-1]
        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('span[@class = "mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
                    #process the winners's bio page with the get_mini_bio method
                    request = scrapy.Request(
                        wdata['link'],
                        callback=self.get_mini_bio )

                    request.meta['item'] = NWinnerItemBio(**wdata)
                    yield request
    

    def get_mini_bio(self, response):
        """get the winner's bio-text and photo"""

        # BASE_URL_ESCAPED = 'http:\/\/en.wikipedia.org'
        item = response.meta['item']
        # cache image
        item['image_urls'] = []

        # Get the URL of the winner's picture, contained in the infobox table 
        img_src = response.xpath('//table[contains(@class,"infobox")]//img/@src')  
        if img_src:
            item['image_urls'] = ['https:' + img_src[0].extract()]
        
        # Get the paragraphs in the biography's body-text
        # If the paragraphs are empty (text() == False), then the normalize-space(.) command is used to force the contents of the paragraph (. represents the p-node in question)
        #to an empty string. This is to make sure any empty paragraph matches the stop-point marking the end of the intro section of the biography.
        paras = response.xpath('//*[@id="mw-content-text"]/div/p[3][text() or normalize-space(.)=""]').extract()
                                
        # Add introductory biography paragraphs till the empty breakpoint
        mini_bio = ''
        for p in paras:
            if p == '<p></p>':
                break
            mini_bio += p

        # correct for wiki-links
        mini_bio = mini_bio.replace('href="/wiki', 'href="' + BASE_URL + '/wiki')
        mini_bio = mini_bio.replace('href="#',  item['link'] + '#')
        item['mini_bio'] = mini_bio
        yield item