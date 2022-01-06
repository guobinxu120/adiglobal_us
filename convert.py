# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urlparse import urlparse
import sys
import re, os, requests, urllib
from scrapy.utils.response import open_in_browser
from collections import OrderedDict
import time
from shutil import copyfile
import json, re, csv

f = open('re1_1.csv')
csv_items = csv.DictReader(f)
models = []

for i, row in enumerate(csv_items):
    models.append(row)


f1 = open("import.csv","wb")
writer = csv.writer(f1, delimiter=';',quoting=csv.QUOTE_ALL)
header = 'Product ID;Image;Name;Reference;Category;Price (tax excl.);Price (tax incl.);Quantity;Status;Position'
writer.writerow(header.split(';'))

for i, row in enumerate(models):
    line = []
    productid = i+1
    line.append(productid)

    img = row['image_id1']
    line.append(img)

    name = row['title']
    line.append(name)

    # Reference = row['Reference']
    line.append('')

    Category = row['category1']
    line.append(Category)

    price = None
    if row['non_discounted_price']:
        Price = float(row['non_discounted_price'])
    line.append(Price)

    Price_tax = row['non_discounted_price']
    line.append(Price)

    Quantity = 0
    line.append(Quantity)

    Status = 0
    line.append(Status)

    Position = 1
    line.append(Position)

    writer.writerow(line)
f1.close()