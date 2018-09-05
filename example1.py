#!/usr/bin/env python

# pip install lxml requests html5lib

from lxml import html
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import re

def cleanSoup(html):
  # from https://stackoverflow.com/a/49440655/553865
  soup = BeautifulSoup(html, "html5lib")
  [x.extract() for x in soup.find_all('script')]
  [x.extract() for x in soup.find_all('style')]
  [x.extract() for x in soup.find_all('meta')]
  [x.extract() for x in soup.find_all('noscript')]
  [x.extract() for x in soup.find_all('div', id='disqus_thread')]
  [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
  return soup

def fetch_posting(url):
  "Returns contents of <div class='container'></div>"
  page = requests.get(url)
  soup = cleanSoup(page.content)
  try:
    container = soup.find('div', class_='container').get_text()
  except urllib.request.URLError as e:
    if hasattr(e, 'reason'):
      print('Failed to reach a server.')
      print('Reason: ', e.reason)
    elif hasattr(e, 'code'):
      print('The server couldn\'t fulfill the request.')
      print('Error code: ', e.code)
      return ""
  else: # everything is fine
    return re.sub("(\t| )+" , " ", re.sub("(\n|\r)+" , "\n", container))

print(fetch_posting('https://blog.mslinn.com/blog/2017/10/15/61'))
print(fetch_posting('https://blog.mslinn.com/blog/2008/04/28/cult-of-software-god'))
