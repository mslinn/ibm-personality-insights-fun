#!/usr/bin/env python

# pip install lxml requests html5lib
# pip install --upgrade watson-developer-cloud

import os, re, requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup, Comment
from watson_developer_cloud import DiscoveryV1
from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV3

def cleanSoup(html):
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

def fetch_posting(url):
  """Returns contents of <div class='container'></div>"""
  posting_page = requests.get(url)
  soup = cleanSoup(posting_page.content)
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

def insights(text):
  """See https://github.com/watson-developer-cloud/python-sdk"""

  #pi_url = "https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13"

  pi_username = os.environ.get("PI_USERNAME")
  pi_password = os.environ.get("PI_PASSWORD")
  #print("pi_username=" + pi_username)
  #print("pi_password=" + pi_password)

  personality_insights = PersonalityInsightsV3(
    version='2016-10-20',
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    # url='https://gateway.watsonplatform.net/personality-insights/api',
    username='YOUR SERVICE USERNAME',
    password='YOUR SERVICE PASSWORD')

    ## If service instance provides API key authentication
    # personality_insights = PersonalityInsightsV3(
    #     version='2016-10-20',
    #     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    #     url='https://gateway.watsonplatform.net/personality-insights/api',
    #     iam_api_key='your_api_key')

    with open(join(dirname(__file__), '../resources/personality-v3.json')) as profile_json:
    profile = personality_insights.profile(
      profile_json.read(), content_type='application/json',
      raw_scores=True, consumption_preferences=True)

    print(json.dumps(profile, indent=2))
    return profile

posting1 = fetch_posting('https://blog.mslinn.com/blog/2017/10/15/61')
posting2 = fetch_posting('https://blog.mslinn.com/blog/2008/04/28/cult-of-software-god')
combined_postings = posting1 + posting2
#print(combined_postings)
print(insights(combined_postings))
