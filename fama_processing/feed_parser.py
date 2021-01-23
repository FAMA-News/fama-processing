'''
feed_parser.py

CREATED:   21.01.2021 10:39
EDITED:    21.01.2021 10:39
PROJECT:   fama_processing
AUTHOR:    Noah Kamara (developer@noahkamara.com)
LICENSE:   Mozilla Public License 2.0
COPYRIGHT: Noah Kamara
'''


from typing import List
import feedparser
from fama_models import RSSFeed, RSSFeedItem
from .validation import Validation
from .article_parser import ArticleParser

class FeedParser:
    @classmethod
    def parse_feed(cls, feed_url: str) -> RSSFeed:
        result = Validation.validate_url(feed_url)
        if not result.valid:
            raise ValueError(
                f"URL failed Validation:\n\t{result.error}")

        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            raise ValueError("FeedParser Library returned error")

        return RSSFeed(
            title=parsed.feed.title,
            subtitle=parsed.feed.subtitle,
            language=parsed.feed.language,
            link=feed_url,
            description=parsed.feed.description,
            image=parsed.feed.image.href
        )

    @classmethod
    def parse_items(cls, feed_url: str) -> List[RSSFeedItem]:
        result = Validation.validate_url(feed_url)
        if not result.valid:
            raise ValueError(
                f"URL failed Validation:\n\t{result.error}")

        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            raise ValueError("FeedParser Library returned error")
        
        feed_items = []

        for item in parsed.entries:
            image = None
            for link in item.links:
                if "image" in link.type and Validation.validate_url(link.href).valid:
                    image = link.href
                    continue
            
            article = ArticleParser.parse(item.link)
            
            #TODO Implement HTML Parsing for paragraphs
            content = article.content

            feed_item = RSSFeedItem(
                title=item.title,
                link=item.link,
                content=content,
                image=image
            )
            feed_items.append(feed_item)
            
        return feed_items
