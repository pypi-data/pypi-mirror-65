#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'weibo_2_album'

import cached_url
import yaml
from bs4 import BeautifulSoup
from telegram_util import AlbumResult as Result
from telegram_util import getWid

prefix = 'https://m.weibo.cn/statuses/show?id='

def getCap(json):
	text = json['text']
	b = BeautifulSoup(text, features="lxml")
	for elm in b.find_all('a'):
		if not elm.get('href'):
			continue
		md = '[%s](%s)' % (elm.text, elm['href'])
		elm.replaceWith(BeautifulSoup(md, features='lxml').find('p'))
	return BeautifulSoup(str(b).replace('<br/>', '\n'), features='lxml').text.strip()

def enlarge(url):
	return url.replace('orj360', 'large')
	
def getImages(json):
	return [enlarge(x['url']) for x in json.get('pics', [])]

def get(path):
	wid = getWid(path)
	r = Result()
	try:
		json = yaml.load(cached_url.get(prefix + wid), Loader=yaml.FullLoader)
	except:
		return r
	json = json['data']
	r.imgs = getImages(json)
	r.cap_html = json['text']
	r.title = json['status_title']
	r.cap = getCap(json)
	r.video = json.get('page_info', {}).get('media_info', {}).get(
		'stream_url_hd', '')
	return r

	

