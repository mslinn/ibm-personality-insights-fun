#!/usr/bin/env python

# pip install --upgrade watson-developer-cloud

import os
from watson_developer_cloud import PersonalityInsightsV3

def insights(text):
  """ Analyze text using IBM Personality Insights.

  This code is based on the `IBM Watson Python SDK`_ docs.
  Environment variables must be set with Personality Insights authentication data before this function is invoked.

  Where do I get an API key? The `IBM API KEY`_ docs are confusing.

  .. _IBM Watson Python SDK:
        https://github.com/watson-developer-cloud/python-sdk
  .. _IBM API KEY:
        https://console.bluemix.net/docs/resources/service_credentials.html#service_credentials
  """

  insights = PersonalityInsightsV3(
    version = '2017-10-13',
    #username = os.environ.get("PI_USERNAME"),
    #password = os.environ.get("PI_PASSWORD"),
    iam_api_key = os.environ.get("PI_API_KEY")
  )

  return insights.profile(
    text,
    content_type = 'application/json',
    raw_scores = True,
    consumption_preferences = True
  )

text = """This text is too short and will cause a warning"""
insightfulText = insights(text)
print(json.dumps(insightfulText, indent=2))
