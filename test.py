'''
test.py

CREATED:   22.01.2021 1:47
EDITED:    22.01.2021 1:47
PROJECT:   fama_processing
AUTHOR:    Noah Kamara (developer@noahkamara.com)
LICENSE:   Mozilla Public License 2.0
COPYRIGHT: Noah Kamara
'''

from fama_processing import FeedParser

feed = FeedParser.parse_items("https://www.spiegel.de/schlagzeilen/index.rss")
for i in feed:
    print(i.content)
    break