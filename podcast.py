import requests
import os
import re
from bs4 import BeautifulSoup
import dateutil.parser

class Podcast:
	def __init__(self, name, rss_feed_url):
		self.name = name
		self.rss_feed_url = rss_feed_url
		
		self.download_directory = f'./downloads/{name}'
		if not os.path.exists(self.download_directory):
			os.mkdir(self.download_directory)

		self.transcription_directory = f'./transcripts/{name}'
		if not os.path.exists(self.transcription_directory):
			os.mkdir(self.transcription_directory)

	def get_items(self, limit=None):
		page = requests.get(self.rss_feed_url)
		soup = BeautifulSoup(page.text, 'xml')
		return soup.find_all('item')[:limit]

	def search_items(self, search, limit=None):
		matched_podcasts = []
		items = self.get_items()
		for podcast in items:
			if re.search(search, podcast.find('description').text, re.I):
				matched_podcasts.append(podcast)

		return matched_podcasts[:limit]