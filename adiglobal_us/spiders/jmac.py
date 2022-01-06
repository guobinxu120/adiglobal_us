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

    name = "jmac"

    # use_selenium = False
    use_selenium = False

    nextCountJson = {}

    from_city = ''
    to_city = ''
    start_date = ''
    end_date = ''
    total_count = 0
    categories_data = None

    # f = open('proxy.txt')
    # datas = f.readlines()
    # w = open('proxy_list.txt', 'w')
    # for d in datas:
    #     da = d
    #     if not 'http' in d:
    #         da = 'http://' + da
    #     w.write(da)
    # w.close()
    # f.close()
    # models = {}




###########################################################

    def __init__(self, *args, **kwargs):
        super(adiglobal_usSpider, self).__init__(*args, **kwargs)
###########################################################

    def start_requests(self):
        yield Request('https://www.jmac.com/SearchResults.asp?search=sdc', callback=self.parse, meta={'index':1})
        # yield Request('https://adiglobal.us/Pages/Results.aspx?searchCat=&k=SDC&m=s', callback=self.parseCat)

    def parse(self, response):
        links = response.xpath('//*[@class="v-product__img"]/@href').extract()
        for link in links:
            yield Request(link, callback=self.parse_final)
        index = response.meta['index']
        if index <226:
            yield Request('https://www.jmac.com/SearchResults.asp?searching=Y&sort=5&search=sdc&show=30&page='+ str(index+1), callback=self.parse, meta={'index':index+1})
    def parse_final(self, response):
        item = OrderedDict()
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        item['image'] = response.xpath('//img[@itemprop="image"]/@src').extract_first()
        pdf_links = response.xpath('//div[@id="ProductDetail_TechSpecs_div"]/a/@href').extract()
        for i in range(3):
            try:
                item['pdf_link_'+str(i+1)] = pdf_links[i]
            except:
                continue
        item['price'] = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        item['jmac_description'] = '\n'.join(response.xpath('//td[@style="vertical-align: top;"]/text()').extract()).strip()
        item['Technical Specifications'] = ''
        item['Features'] = ''
        td_tags = response.xpath('//span[@id="product_description"]/table//tr/td')
        for i, tag in enumerate(td_tags):
            if i == 0:
                item['jmac_description'] = '\n'.join(tag.xpath('./text()').extract()).strip()
            else:
                key = tag.xpath('./b/inline/text()').extract_first().strip()
                if key:
                    item[key.replace(':', '')] = '\n'.join(tag.xpath('.//li/text()').extract()).strip()
        yield item
