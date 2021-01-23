'''
article_parser.py

CREATED:   21.01.2021 10:40
EDITED:    21.01.2021 10:40
PROJECT:   fama_processing
AUTHOR:    Noah Kamara (developer@noahkamara.com)
LICENSE:   Mozilla Public License 2.0
COPYRIGHT: Noah Kamara
'''


import requests
from readability import Document
from fama_models import Article
from .validation import Validation
from typing import Optional, List

class ArticleParser:
    """Article Parser Class"""

    @classmethod
    def parse(cls, article_url: str) -> Article:
        """Parses a news article at the given URL

        Args:
            article_url (str): URL of the News Article

        Raises:
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]

        Returns:
            Article: [description]
        """
        content = ""
        # Validate URL
        result = Validation.validate_url(article_url)
        if not result.valid:
            raise ValueError(f"URL failed Validation:\n\t{result.error}")

        # Fetch Content
        try:
            response = requests.get(article_url)
            content = response.text
        except Exception as e:
            raise ValueError(f"Server could not be reached:\n\t({e})")

        # Parse Content
        try:
            doc = Document(content)
        except Exception as e:
            raise ValueError(f"Article Parsing Failed:\n\t{e}")
        
        #TODO Implement HTML Parsing for paragraphs
        content = doc.summary()
        
        return Article(
            title=doc.title(),
            short_title=doc.short_title(),
            content=content
        )
