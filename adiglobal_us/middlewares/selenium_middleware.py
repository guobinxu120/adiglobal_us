from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from scrapy.http import TextResponse
from scrapy.exceptions import CloseSpider
from scrapy import signals
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
import json, csv
from collections import OrderedDict
from random import randint

class SeleniumMiddleware(object):

	total_count = 0

	def __init__(self, s):
		# self.exec_path = s.get('PHANTOMJS_PATH', './chromedriver.exe')
		self.exec_path = 'E:/chromedriver.exe'

###########################################################

	@classmethod
	def from_crawler(cls, crawler):
		obj = cls(crawler.settings)

		crawler.signals.connect(obj.spider_opened,
								signal=signals.spider_opened)
		crawler.signals.connect(obj.spider_closed,
								signal=signals.spider_closed)
		return obj

###########################################################

	def spider_opened(self, spider):
		try:
			self.d = init_driver(self.exec_path)
		except TimeoutException:
			CloseSpider('PhantomJS Timeout Error!!!')

###########################################################

	def spider_closed(self, spider):
		self.d.quit()
###########################################################

	def process_request(self, request, spider):
		if spider.use_selenium:
			print "############################ Received url request from scrapy #####"

			try:
				self.d.get(request.url)


			except TimeoutException as e:
				raise CloseSpider('TIMEOUT ERROR')

			f2 = open('urls.csv')
			csv_items = csv.DictReader(f2)

			product_urls = []
			for i, row0 in enumerate(csv_items):
				product_urls.append(row0['url'])
			f2.close()


			total_count = 0

			# sign in
			while True:
				try:
					email_edit = self.d.find_element_by_xpath('//*[@id="ctl00_PlaceHolderMain_ctl00_ctlLoginView_MainLoginView_MainLogin_UserName"]')
					pw_edit = self.d.find_element_by_xpath('//*[@id="ctl00_PlaceHolderMain_ctl00_ctlLoginView_MainLoginView_MainLogin_Password"]')
					login_button = self.d.find_element_by_xpath('//*[@id="ctl00_PlaceHolderMain_ctl00_ctlLoginView_MainLoginView_MainLogin_LoginButton"]')
					count = 1
					if email_edit and pw_edit and login_button:
						print "****************************************************************************************"
						time.sleep(1)
						email_edit.click()
						email_edit.send_keys("pcarson7")
						time.sleep(1)
						pw_edit.click()
						pw_edit.send_keys("Dil11lon")

						login_button.click()
						time.sleep(3)
						break
				except:
					time.sleep(3)


			f1 = open("urls_scraped.csv","wb")
			writer = csv.writer(f1, delimiter=',',quoting=csv.QUOTE_ALL)
			writer.writerow(['url'])

			f_unknown_fields = open("unknown_fields.csv","wb")
			writer_f_unknown_fields = csv.writer(f_unknown_fields, delimiter=',',quoting=csv.QUOTE_ALL)
			writer_f_unknown_fields.writerow(['field'])


			f_result = open("result_data.csv","wb")
			writer_result = csv.writer(f_result, delimiter=',',quoting=csv.QUOTE_ALL)

			fields = ['Name', 'Model', 'ADI', 'Price', 'Qty', 'Marketing Information', 'Main Features', 'Description','Category', 'Product Url', 'Image Url', 'ADI Part Number', 'Brand Name', 'Manufacturer',
									'Manufacturer Part Number', 'Product Line', 'Product Model', 'Product Series', 'Product Type', 'UPC', 'Weight',
									'Color', 'Depth', 'Height', 'Width', 'Material', 'Additional Information', 'Package Contents', 'Compatibility',
									'Standard Warranty', 'Application/Usage', 'field', 'Country of Origin', 'Features', 'Battery Capacity',
					  				'Battery Size', 'Output Voltage', 'Weight (Approximate)', 'Form Factor', 'Length', 'Device Support']

			writer_result.writerow(fields)

			part_count = 0

			for product_url in product_urls:
				# product_url = "https://adiglobal.us/Pages/Product.aspx?pid=SZ-304FS24U&Category=6880"
				self.d.get(product_url)

				resp1 = TextResponse(url=self.d.current_url,
									body=self.d.page_source,
									encoding='utf-8')
				resp1.request = request.copy()


				item = OrderedDict()
				# item['Name'] = ''
				# item['Model'] = ''
				# item['ADI'] = ''
				# item['Price'] = ''
				# item['Qty'] = ''
				# item['Product Url'] = ''
				# item['Image Url'] = ''
                #
				# # General Information
				# item['ADI Part Number'] = ''
				# item['Brand Name'] = ''
				# item['Manufacturer'] = ''
				# item['Manufacturer Part Number'] = ''
				# item['Product Line'] = ''
				# item['Product Model'] = ''
				# item['Product Series'] = ''
				# item['Product Type'] = ''
				# item['UPC'] = ''
				# item['Weight'] = ''
                #
				# # Physical Characteristics
				# item['Color'] = ''
				# item['Depth'] = ''
				# item['Height'] = ''
				# item['Width'] = ''
				# item['Material'] = ''
                #
				# # Miscellaneous
				# item['Additional Information'] = ''
				# item['Package Contents'] = ''
				# item['Compatibility'] = ''
                #
				# # Warranty
				# item['Standard Warranty'] = ''
                #
				# # Technical Information
				# item['Application/Usage'] = ''
				for key in fields:
					item[key] = ''

				############--------------  Put values for product.  -----------------##############
				while True:
					resp1 = TextResponse(url=self.d.current_url,
											body=self.d.page_source,
											encoding='utf-8')
					resp1.request = request.copy()
					if not resp1.xpath('//*[@class="productTitle"]/h1/text()').extract_first():

						time.sleep(5)
						self.d.refresh()
					else:

						break
				item['Name'] = resp1.xpath('//*[@class="productTitle"]/h1/text()').extract_first().encode('utf-8')
				item['Model'] = resp1.xpath('//*[@class="vendorNbr"]/text()').extract_first().split(':')[1].strip().encode('utf-8')
				item['ADI'] = resp1.xpath('//*[@class="partNbr"]/text()').extract_first().split(':')[1].strip().encode('utf-8')
				if resp1.xpath('//*[@class="col-value price  lprice"]/text()'):
					item['Price'] = resp1.xpath('//*[@class="col-value price  lprice"]/text()').re(r'[\d.,]+')[0]
				else:
					item['Price'] = resp1.xpath('//*[@class="col-value price  lprice"]/span/text()').re(r'[\d.,]+')[0]
				item['Qty'] = 1
				Marketing_Information = resp1.xpath('//*[@class="marketingdata"]/text()').extract_first()
				if Marketing_Information:
					item['Marketing Information'] = Marketing_Information.strip().encode('utf-8')

				Main_Features = resp1.xpath('//*[@class="sub-list0"]/text()').extract()
				if len(Main_Features) > 0:
					item['Main Features'] = '\n'.join(Main_Features).encode('utf-8')

				item['Product Url'] = product_url.encode('utf-8')
				item['Image Url'] = resp1.xpath('//*[@class="product-img-big"]/img/@src').extract_first().encode('utf-8')


				xpaths_for_upc = resp1.xpath('//*[@id="ctl00_SPWebPartManager1_g_a026af07_e6df_4702_b849_e22ce819b3db_ctl00_InformationContentsDiv"]/ul/li')
				for xpath0 in xpaths_for_upc:
					if xpath0.xpath('.//label/text()').extract_first() == 'UPC Code:':
						item['UPC'] = xpath0.xpath('.//span/text()').extract_first()
					elif xpath0.xpath('.//label/text()').extract_first() == 'Description:':
						item['Description'] = xpath0.xpath('.//span/text()').extract_first()
					elif xpath0.xpath('.//label/text()').extract_first() == ' Category:':
						item['Category'] = xpath0.xpath('.//span/text()').extract_first()

				#########  put data of General Information   ##########
				if resp1.xpath('//*[@id="spectab"]'):
					while True:
						self.d.find_element_by_xpath('//*[@id="spectab"]').click()

						respP = TextResponse(url=self.d.current_url,
											body=self.d.page_source,
											encoding='utf-8')
						respP.request = request.copy()

						if respP.xpath('//*[@id="specsectionresults"]/div'):
							for info_xpath in respP.xpath('//*[@id="specsectionresults"]/div'):
								key = info_xpath.xpath('.//div[1]/text()').extract_first()
								val = ''
								if info_xpath.xpath('.//div[2]/text()').extract_first():
									val = info_xpath.xpath('.//div[2]/text()').extract_first().encode('utf-8')
								else:
									if info_xpath.xpath('.//div[2]/ul/li/text()').extract():
										val = '\n'.join(info_xpath.xpath('.//div[2]/ul/li/text()').extract()).encode('utf-8')
									else:
										val = '\n'.join(info_xpath.xpath('.//div[2]/ul/ul/li/text()').extract()).encode('utf-8')
								if fields.__contains__(key):
									item[key] = val
								else:
									writer_f_unknown_fields.writerow([key])
							break
						else:
							time.sleep(1)
				# else:
				# 	xpaths_for_upc = resp1.xpath('//*[@id="ctl00_SPWebPartManager1_g_a026af07_e6df_4702_b849_e22ce819b3db_ctl00_InformationContentsDiv"]/ul/li')
				# 	for xpath0 in xpaths_for_upc:
				# 		if xpath0.xpath('.//label/text()').extract_first() == 'UPC Code:':
				# 			item['UPC'] = xpath0.xpath('.//span/text()').extract_first()

				writer.writerow([product_url])
				writer_result.writerow(item.values())

				part_count += 1
				if part_count == 40:
					time.sleep(10)
					part_count = 0

				total_count += 1
				print 'part_count: ' + str(part_count)
				print 'total_count: ' + str(total_count)






			f_result.close()
			f1.close()
			f_unknown_fields.close()

			####################----------------- Part to get urls of products -----------------#################################

			# self.d.get('https://adiglobal.us/Pages/Results.aspx?searchCat=&k=SDC&m=s')
			# time.sleep(1)
            #
			# f1 = open("urls.csv","wb")
			# writer = csv.writer(f1, delimiter=',',quoting=csv.QUOTE_ALL)
			# writer.writerow(['url'])
            #
			# count = 0
			# pagenum = 1
            #
			# while True:
            #
			# 	resp1 = TextResponse(url=self.d.current_url,
			# 						body=self.d.page_source,
			# 						encoding='utf-8')
			# 	resp1.request = request.copy()
            #
			# 	domain = 'https://adiglobal.us'
            #
			# 	product_urls = resp1.xpath('//*[@class="product-title ellipsisMultiLine"]/a/@href').extract()
            #
            #
            #
			# 	if product_urls:
            #
            #
            #
			# 		for product_href in product_urls:
			# 			if product_href.__contains__('/Pages/'):
			# 				url = domain + product_href
			# 			else:
			# 				url = domain + '/Pages/' + product_href
			# 			writer.writerow([url])
			# 			count += 1
			# 			print url
			# 			print count
            #
            #
			# 			# self.d.get(url)
			# 			#
			# 		resp1 = TextResponse(url=self.d.current_url,
			# 							body=self.d.page_source,
			# 							encoding='utf-8')
			# 		resp1.request = request.copy()
            #
			# 		next_pages = resp1.xpath('//*[@class="paging"]/a')
            #
			# 		if resp1.xpath('//*[@class="paging"]/a/text()').extract().__contains__('> Next'):
			# 			pagenum += 1
			# 			next_url = 'https://adiglobal.us/Pages/Results.aspx?c=0000&p=0000&m=s&searchCat=0000&k=SDC&pageSize=24&page={}&dm=g&s=b&rf=&dc='.format(pagenum)
			# 			self.d.get(next_url)
			# 			time.sleep(2)
			# 		else:
			# 			break
            #
			# f1.close()
			#######################################################################################################
			return None


###########################################################
###########################################################

def init_driver(path):

	chrome_options = Options()
	chrome_options.add_argument("window-size=1500,2000")
	# chrome_options.add_argument("window-position=-5000,0")
	d = webdriver.Chrome( chrome_options=chrome_options)
	# d = webdriver.PhantomJS(executable_path=path)
	d.set_page_load_timeout(120)

	return d