# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy import Request
from urlparse import urlparse
from json import loads
from datetime import datetime, timedelta
# import json
import re, csv
from random import randint
from collections import OrderedDict

class adiglobal_usSpider(scrapy.Spider):

	name = "adiglobal_us_spider"

	# use_selenium = False
	use_selenium = True

	nextCountJson = {}

	from_city = ''
	to_city = ''
	start_date = ''
	end_date = ''
	total_count = 0
	categories_data = None

###########################################################

	def __init__(self, *args, **kwargs):
		super(adiglobal_usSpider, self).__init__(*args, **kwargs)
###########################################################

	def start_requests(self):
		yield Request('https://adiglobal.us/Pages/WebRegistration.aspx', callback=self.parse)
		# yield Request('https://adiglobal.us/Pages/Results.aspx?searchCat=&k=SDC&m=s', callback=self.parseCat)

	def parseCat(self, response):
		domain = 'https://adiglobal.us'

		product_urls = response.xpath('//*[@class="product-title ellipsisMultiLine"]/a/@href').extract()

		if product_urls:
			for product_href in product_urls:
				url = domain + product_href

				item = OrderedDict()
				item['url'] = url
				yield item

		# next_pages = response.xpath('//*[@class="paging"]/a')
        #
		# for
        #
		# pass

