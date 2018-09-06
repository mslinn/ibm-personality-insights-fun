#!/usr/bin/env python

# pip install lxml requests html5lib
# pip install --upgrade watson-developer-cloud

from __future__ import print_function
import os, re, requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup, Comment
from watson_developer_cloud import DiscoveryV1
import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV3

def _clean_soup(html):
  soup = BeautifulSoup(html, "html5lib")

  for tag in ['script', 'style', 'meta', 'noscript']:
    for element in soup.find_all(tag):
      element.decompose()

  for element in soup.find_all('div', id='disqus_thread'):
    element.decompose()

  for element in soup.find_all('a', class_='dsq-brlink'):
    element.decompose()
  #for element in soup.find_all(text=lambda text:isinstance(text, Comment)):
    #element.decompose()
  return soup

def _fetch_posting(url):
  """Returns contents of <div class='container'></div>"""
  posting_page = requests.get(url)
  soup = _clean_soup(posting_page.content)
  try:
    container = soup.find('div', class_='container').get_text()
  except urllib.request.URLError as e:
    puts("""The server couldn't reach #{url}.""")
    if hasattr(e, 'reason'):
      print('Reason: ', e.reason)
    elif hasattr(e, 'code'):
      print('Error code: ', e.code)
    return ""
  else: # everything is fine
    return re.sub("(\t| )+" , " ", re.sub("(\n|\r)+" , "\n", container)).strip()

def insights(user_text):
  """ Analyze text using IBM Personality Insights.

  ``pip install --upgrade watson-developer-cloud``

  This code is based on the `IBM Watson Python SDK`_ docs.
  Environment variables must be set with Personality Insights authentication data before this function is invoked.

  Where do I get or generate an API key? The `IBM API KEY`_ docs are confusing.

  .. _IBM Watson Python SDK:
        https://github.com/watson-developer-cloud/python-sdk
  .. _IBM API KEY:
        https://console.bluemix.net/docs/resources/service_credentials.html#service_credentials
  """

  insights = PersonalityInsightsV3(
    version = '2017-10-13',
    username = os.environ.get("PI_USERNAME"),
    password = os.environ.get("PI_PASSWORD")
    #iam_api_key = os.environ.get("PI_API_KEY")
  )

  return insights.profile(
    user_text,
    content_type = 'text/plain;charset=utf-8',
    raw_scores = True,
    consumption_preferences = True
  )

posting1 = _fetch_posting('https://blog.mslinn.com/blog/2017/10/15/61')
posting2 = _fetch_posting('https://blog.mslinn.com/blog/2008/04/28/cult-of-software-god')
combined_postings = posting1 + posting2
insightful_json = insights(combined_postings)
print(json.dumps(insightful_json, indent=2))
