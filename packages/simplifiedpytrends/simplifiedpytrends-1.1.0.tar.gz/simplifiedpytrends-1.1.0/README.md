# simplified pytrends
[![PyPI](https://img.shields.io/pypi/v/simplifiedpytrends.svg)](https://pypi.python.org/pypi/simplifiedpytrends/)
[![Downloads](https://pepy.tech/badge/simplifiedpytrends/month)](https://pepy.tech/project/simplifiedpytrends)
[![Build Status](https://api.travis-ci.org/Drakkar-Software/simplifiedpytrends.svg?branch=master)](https://travis-ci.org/Drakkar-Software/simplifiedpytrends) 

Simplified version of https://github.com/GeneralMills/pytrends: removed pandas dependency.

## Introduction

Unofficial API for Google Trends

Allows simple interface for automating downloading of reports from Google Trends. Main feature is to allow the script to login to Google on your behalf to enable a higher rate limit. Only good until Google changes their backend again :-P. When that happens feel free to contribute!


## Table of contens

* [Installation](#installation)

* [API](#api)

  * [API Methods](#api-methods)

  * [Common API parameters](#common-api-parameters)

    * [Interest Over Time](#interest-over-time)

  * [Caveats](#caveats)

* [Credits](#credits)

## Installation

    pip install simplifiedpytrends

## Requirements

* Written for both Python 2.7+ and Python 3.3+
* Requires Requests


## API

### Connect to Google

    from simplifiedpytrends.request import TrendReq

    pytrends = TrendReq(hl='en-US', tz=360)

or if you want to use proxies as you are blocked due to Google rate limit:


    from simplifiedpytrends.request import TrendReq

    pytrends = TrendReq(hl='en-US', tz=360, proxies = {'https': 'https://34.203.233.13:80'})

Note: only https proxies will work, and you need to add the port number after the proxy ip address

### Build Payload
    kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

Parameters

* `kw_list`

  - *Required*
  - Keywords to get data for


## API Methods

The following API methods are available:

* [Interest Over Time](#interest-over-time): returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.

## Common API parameters

Many API methods use the following:

* `kw_list`

  - keywords to get data for
  - Example ```['Pizza']```
  - Currently supports only one parameter

    * Advanced Keywords

      - When using Google Trends dashboard Google may provide suggested narrowed search terms.
      - For example ```"iron"``` will have a drop down of ```"Iron Chemical Element, Iron Cross, Iron Man, etc"```.
      - Find the encoded topic by using the get_suggestions() function and choose the most relevant one for you.
      - For example: ```https://www.google.com/trends/explore#q=%2Fm%2F025rw19&cmpt=q```
      - ```"%2Fm%2F025rw19"``` is the topic "Iron Chemical Element" to use this with pytrends
      - You can also use `pytrends.suggestions()` to automate this.

* `cat`

  - Category to narrow results
  - Find available cateogies by inspecting the url when manually using Google Trends. The category starts after ```cat=``` and ends before the next ```&``` or view this [wiki page containing all available categories](https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories)
  - For example: ```"https://www.google.com/trends/explore#q=pizza&cat=71"```
  - ```'71'``` is the category
  - Defaults to no category

* `geo`

  - Two letter country abbreviation
  - For example United States is ```'US'```
  - Defaults to World
  - More detail available for States/Provinces by specifying additonal abbreviations
  - For example: Alabama would be ```'US-AL'```
  - For example: England would be ```'GB-ENG'```

* `tz`

  - Timezone Offset
  - For example US CST is ```'360'```

* `timeframe`

  - Date to start from
  - Defaults to last 5yrs, `'today 5-y'`.
  - Everything `'all'`
  - Specific dates, 'YYYY-MM-DD YYYY-MM-DD' example `'2016-12-14 2017-01-25'`
  - Specific datetimes, 'YYYY-MM-DDTHH YYYY-MM-DDTHH' example `'2017-02-06T10 2017-02-12T07'`
      - Note Time component is based off UTC

  - Current Time Minus Time Pattern:

    - By Month: ```'today #-m'``` where # is the number of months from that date to pull data for
      - For example: ``'today 3-m'`` would get data from today to 3months ago
      - **NOTE** Google uses UTC date as *'today'*
      - Seems to only work for 1, 2, 3 months only

    - Daily: ```'now #-d'``` where # is the number of days from that date to pull data for
      - For example: ``'now 7-d'`` would get data from the last week
      - Seems to only work for 1, 7 days only

    - Hourly: ```'now #-H'``` where # is the number of hours from that date to pull data for
      - For example: ``'now 1-H'`` would get data from the last hour
      - Seems to only work for 1, 4 hours only

* `gprop`

  - What Google property to filter to
  - Example ```'images'```
  - Defaults to web searches
  - Can be ```images```, ```news```, ```youtube``` or ```froogle``` (for Google Shopping results)


### Interest Over Time

    pytrends.interest_over_time()

Returns a sorted list of dict: containing "timestamp" and "data"



# Caveats

* This is not an official or supported API
* Google may change aggregation level for items with very large or very small search volume
* Google will send you an email saying that you had a new login after running this.
* Rate Limit is not publicly known, let me know if you have a consistent estimate
  * One user reports that 1,400 sequential requests of a 4 hours timeframe got them to the limit. (Replicated on 2 networks)
  * It has been tested, and 60 seconds of sleep between requests (successful or not) is the correct amount once you reach the limit.
* For certain configurations the dependency lib certifi requires the environment variable REQUESTS_CA_BUNDLE to be explicitly set and exported. This variable must contain the path where the ca-certificates are saved or a SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] error is given at runtime. 

# Credits

* Original pytrends lib:
  - https://github.com/GeneralMills/pytrends

* Major JSON revision ideas taken from pat310's JavaScript library

  - https://github.com/pat310/google-trends-api

* Connecting to google code heavily based off Stack Overflow post

  - http://stackoverflow.com/questions/6754709/logging-in-to-google-using-python

* With some ideas pulled from Matt Reid's Google Trends API

  - https://bitbucket.org/mattreid9956/google-trend-api/overview
