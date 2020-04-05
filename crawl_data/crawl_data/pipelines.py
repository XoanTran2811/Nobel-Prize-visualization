# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

""" Let's write a little pipelin to reject genderless Nobel Prize winners 
   (so we can omit prizes given to organizations rather than individuals
   using our existing nwinners_full spider to deliver the items
"""
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

"""
class NobelWinnersPipeline(object):
    def process_item(self, item, spider):
        return item


class DropNonPersons(object):
    if not item['gender']:
        raise DropItem('No gender for %s' %item['name'])
    return item

"""
class NobelImagesPipeline(ImagesPipeline):
    
    # this takes any image URLs craped by our nwinners_minibio spider and generates an HTTP request for their content
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print(image_url)
            yield scrapy.Request(image_url)

    # after the image URL requests have been made, the results are delivered to the item_completed method
    def item_completed(self, results, item, info):
        """This Python list-comprehension filters the list of result tuples (of form [(True, Image), (False, Image) ...]) for those that
        were successful and stores their file paths relative to the directory specified by the IMAGES_STORE variable in settings.py."""
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths[0]
           
        return item

