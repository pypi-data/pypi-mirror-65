#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'weibo_2_album'

import cached_url
import yaml
from bs4 import BeautifulSoup
from telegram_util import AlbumResult as Result
from telegram_util import getWid

prefix = 'https://m.weibo.cn/statuses/show?id='

def getRetweetCap(json):
	json = json.get('retweeted_status')
	if not json:
		return ''
	return json.get('longText', {}).get('longTextContent') or \
		json.get('retweeted_status', {}).get('text', '')

def isprintable(s):
    try: 
    	s.encode('utf-8')
    except UnicodeEncodeError: return False
    else: return True

def getPrintable(s):
	return ''.join(x for x in s if isprintable(x))

def getCap(json):
	text = getPrintable(json['text'] + '\n\n' + getRetweetCap(json))
	b = BeautifulSoup(text, features="lxml")
	for elm in b.find_all('a'):
		if not elm.get('href'):
			continue
		md = '[%s](%s)' % (elm.text, elm['href'])
		elm.replaceWith(BeautifulSoup(md, features='lxml').find('p'))
	line = BeautifulSoup(str(b).replace('<br/>', '\n'), features='lxml').text.strip()
	return line

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
	r.imgs = getImages(json) or getImages(json.get('retweeted_status', {}))
	r.cap_html = json['text']
	r.title = json['status_title']
	r.cap = getCap(json)
	r.video = json.get('page_info', {}).get('media_info', {}).get(
		'stream_url_hd', '')
	return r

	

