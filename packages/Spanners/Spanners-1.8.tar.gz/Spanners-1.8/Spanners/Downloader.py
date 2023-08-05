#!/usr/bin/env python3

import os, re, sys, requests, hashlib, shutil, io, urllib3, logging, arrow

from urllib.parse import quote_plus, urlparse
from bs4 import BeautifulSoup as BS

from Baubles.Logger import Logger

logger = Logger()
logger.setLevel(logging.INFO)

class Downloader(object):
	
	def __init__(self, cacheDir='.cache', fresh=False):
		#urllib3.disable_warnings()
		self.cacheDir = cacheDir
		self.fresh = fresh
		logger.debug('cacheDir='+self.cacheDir)
		
	def download(self, url, file=None):
		'''
		read from disk before downloading
		'''
		logger.debug('url='+url)
		
		if not file:
			parts = urlparse(url)
			
			query = ''
			if len(parts.query):
				logger.debug('query=%s'%parts.query)
				md = hashlib.md5()
				md.update(quote_plus(parts.query).encode('utf8'))
				query = '.%s'%md.hexdigest()
				
			file = '%s/%s%s%s'%(
				self.cacheDir,
				parts.netloc,
				parts.path,
				query
			)

		logger.debug('file='+file)
	
		dirName = os.path.dirname(file)
		if dirName and not os.path.isdir(dirName):
			os.makedirs(dirName)

		data = None

		if self.fresh or not os.path.isfile(file):
			logger.info('to cache '+file)
			response = requests.get(url, verify=True, stream=True)
			if response.status_code != 200:
				file = '%s=%s'%(file,response.status_code)
				logger.warning('url=%s, code=%s'%(url, response.status_code))
			with open(file,'wb') as output:
				response.raw.decode_content = True
				shutil.copyfileobj(response.raw, output)

		else:
			logger.info('from cache '+file)
		
		with open(file, 'rb') as input:
			data = io.BytesIO(input.read())
			
		return data.getvalue()


def main():
	downloader = Downloader(fresh=False)
	now = arrow.now()
	url = 'https://docs.python.org/3/library/hashlib.html' #?_=%s'%now
	html = downloader.download(url)
	bs = BS(html, 'html5lib')
	print('\n%s'%bs.find('title').text)
	#print(html)
	#s = str(html)
	#print('\n'.join(s.split('\\n')[:5]))

		
if __name__ == '__main__': main()

