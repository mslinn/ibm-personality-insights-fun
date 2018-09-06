#!/usr/bin/env python

import json
import os

from watson_developer_cloud import PersonalityInsightsV3


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

text = """Ipsum lorem. """ * 100
insightful_json = insights(text)
print(json.dumps(insightful_json, indent=2))
