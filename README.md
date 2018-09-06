# Fun With IBM Personality Insights

In this project I use Python 3 to play around with [IBM Personality Insights](https://console.bluemix.net/docs/services/personality-insights).
I used [IBM's free Lite service](https://console.bluemix.net/catalog/services/personality-insights),
which provides 1,000 API calls per month at no cost, and deploy to the US South region.

I enabled a Lite
[Personality Insights service instance](https://console.bluemix.net/catalog/services/personality-insights),
which only lasts 30 days.

![IBM Personality Insights description](personality_insights.png)

I followed the [Getting started](9https://console.bluemix.net/docs/services/personality-insights/getting-started.html#getting-started-tutorial)
instructions and referred to the
[API reference](https://www.ibm.com/watson/developercloud/personality-insights/api/).

The service name was automatically created: `Personality Insights-ca`

The Getting Started examples use `curl` to call methods of the HTTP interface.
Ubuntu's version of `curl` installed by default is the correct version.

I used <a href="https://stedolan.github.io/jq/"><code>jq</code></a> to pretty-print the returned JSON.

```
$ sudo apt install jq
```

[Step 1](https://console.bluemix.net/docs/services/personality-insights/getting-started.html#gettingStarted)
of the Getting Started instructions has a serious error: instead of providing the `apiKey`,
your `username:password` must be provided. 

```
export PI_USERNAME="999999-8888-7777-6666-12345678" # replace with your Personality Insights username
export PI_PASSWORD="zYxWv"                          # replace with your Personality Insights password
```

## Curl
The Getting Started instructions show a curl example, which I modified as shown.
I then wrote a simple Python equivalent, shown in the next section.

```
export PATH_OF_TEXT_TO_ANALYSE=./profile.txt
curl -sSX POST --user "$PI_USERNAME:$PI_PASSWORD" \
  --header "Content-Type: text/plain;charset=utf-8" \
  --header "Accept: application/json" \
  --data-binary @"$PATH_OF_TEXT_TO_ANALYSE" \
  "https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13" \
  jq .
```

Notice the leading `@` character before `$PATH_OF_TEXT_TO_ANALYSE`.
If you don't put that character there, the path is interpreted as the text analyze, instead of the filename of containing the text to analyze.

[Here is the JSON output.](example1a.json)

## Python

I found the 
[Python docstring for the constructor](https://github.com/watson-developer-cloud/python-sdk/blob/master/watson_developer_cloud/personality_insights_v3.py#L63-L102) 
to be helpful.
I got a little more ambitious with the Python version: it reads two blog postings I wrote, combines them, and
submits them for analysis. [Here is the resulting json](example1b.json).
