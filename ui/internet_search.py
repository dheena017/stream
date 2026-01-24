"""
Internet Search Module - DuckDuckGo Search Integration
Provides real-time web search capabilities for the chat interface
"""

import logging
from typing import Dict, List, Optional

import requests
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


class InternetSearchEngine:
    """
    Wrapper around DuckDuckGo search API for retrieving real-time information
    """

    def __init__(self, timeout: int = 10):
        """Initialize search engine with timeout configuration"""
        self.timeout = timeout
        self.ddgs = DDGS(timeout=timeout)

    def search(self, query: str, max_results: int = 5, detailed: bool = False, time_range: str = "Anytime", domain: str = None) -> List[Dict]:
        """
        Perform a web search using DuckDuckGo

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            detailed: Whether to fetch full text (unused in basic text search)
            time_range: Time filter (Anytime, Past Day, Past Week, Past Month)
            domain: Optional domain to restrict search to
        """
        try:
            # Domain filtering
            final_query = query
            if domain and domain.strip():
                final_query += f" site:{domain.strip()}"

            # Time filtering mapping
            time_map = {
                "Past Day": "d",
                "Past Week": "w",
                "Past Month": "m",
                "Anytime": None
            }
            time_param = time_map.get(time_range)

            logger.info(f"Searching for: {final_query} (Time: {time_param})")

            # Using backend='api' or 'html' is standard, typically 'api' is default.
            # timelimit argument expects 'd', 'w', 'm', 'y'
            results = self.ddgs.text(final_query, max_results=max_results, timelimit=time_param)

            if not results:
                logger.warning(f"No results found for: {final_query}")
                return []

            processed_results = []
            for result in results:
                processed_results.append({
                    'title': result.get('title', 'No title'),
                    'body': result.get('body', 'No description'),
                    'href': result.get('href', ''),
                    'source': self._extract_domain(result.get('href', ''))
                })

            logger.info(f"Found {len(processed_results)} results")
            return processed_results

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def search_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for news articles

        Args:
            query: News search query
            max_results: Maximum number of news results

        Returns:
            List of news result dictionaries
        """
        try:
            logger.info(f"Searching news for: {query}")
            results = self.ddgs.news(query, max_results=max_results)

            if not results:
                return []

            processed_results = []
            for result in results:
                processed_results.append({
                    'title': result.get('title', 'No title'),
                    'body': result.get('body', 'No description'),
                    'date': result.get('date', 'Unknown date'),
                    'source': result.get('source', 'Unknown source'),
                    'href': result.get('href', '')
                })

            return processed_results

        except Exception as e:
            logger.error(f"News search error: {str(e)}")
            return []

    def search_images(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for images

        Args:
            query: Image search query
            max_results: Maximum number of images

        Returns:
            List of image result dictionaries
        """
        try:
            logger.info(f"Searching images for: {query}")
            results = self.ddgs.images(query, max_results=max_results)

            if not results:
                return []

            processed_results = []
            for result in results:
                processed_results.append({
                    'title': result.get('title', 'No title'),
                    'image': result.get('image', ''),
                    'source': result.get('source', 'Unknown source'),
                    'url': result.get('url', '')
                })

            return processed_results

        except Exception as e:
            logger.error(f"Image search error: {str(e)}")
            return []

    def fetch_url_content(self, url: str, max_length: int = 2000) -> Optional[str]:
        """
        Fetch and extract text content from a URL

        Args:
            url: URL to fetch
            max_length: Maximum length of extracted text

        Returns:
            Extracted text content or None if fetch fails
        """
        try:
            logger.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Simple HTML text extraction
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self.skip_tags = {'script', 'style', 'meta', 'link'}
                    self.current_tag = None

                def handle_starttag(self, tag, attrs):
                    self.current_tag = tag

                def handle_data(self, data):
                    if self.current_tag not in self.skip_tags:
                        text = data.strip()
                        if text:
                            self.text.append(text)

            parser = TextExtractor()
            parser.feed(response.text)
            content = ' '.join(parser.text)[:max_length]

            logger.info(f"Successfully fetched {len(content)} characters from {url}")
            return content

        except Exception as e:
            logger.error(f"Content fetch error: {str(e)}")
            return None

    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '')
            return domain
        except:
            return 'Unknown'


def format_search_results_for_chat(results: List[Dict], search_type: str = "web") -> str:
    """
    Format search results into a readable string for chat context

    Args:
        results: List of search results
        search_type: Type of search (web, news, images)

    Returns:
        Formatted string of search results
    """
    if not results:
        return "No search results found."

    formatted = f"\n🔍 **Internet Search Results** ({search_type.upper()}):\n\n"

    for i, result in enumerate(results, 1):
        if search_type == "news":
            formatted += f"{i}. **{result.get('title', 'No title')}**\n"
            formatted += f"   📰 {result.get('source', 'Unknown')}\n"
            formatted += f"   📅 {result.get('date', 'Unknown date')}\n"
            formatted += f"   {result.get('body', 'No description')}\n"
            formatted += f"   🔗 {result.get('href', '')}\n\n"

        elif search_type == "images":
            formatted += f"{i}. {result.get('title', 'No title')}\n"
            formatted += f"   🖼️ {result.get('source', 'Unknown source')}\n"
            formatted += f"   🔗 {result.get('url', '')}\n\n"

        else:  # web search
            formatted += f"{i}. **{result.get('title', 'No title')}**\n"
            formatted += f"   📍 {result.get('source', 'Unknown')}\n"
            formatted += f"   {result.get('body', 'No description')}\n"
            formatted += f"   🔗 {result.get('href', '')}\n\n"

    return formatted


def create_search_context(search_results: List[Dict], query: str) -> str:
    """
    Create a context string from search results for AI processing

    Args:
        search_results: List of search results
        query: Original search query

    Returns:
        Formatted context string
    """
    if not search_results:
        return ""

    context = f"\n[REAL-TIME SEARCH RESULTS FOR: {query}]\n"
    context += "=" * 50 + "\n"

    for i, result in enumerate(search_results, 1):
        context += f"\nResult {i}:\n"
        context += f"Title: {result.get('title', 'N/A')}\n"
        context += f"Source: {result.get('source', 'N/A')}\n"
        context += f"Content: {result.get('body', result.get('content', 'N/A'))}\n"
        context += f"URL: {result.get('href', result.get('url', 'N/A'))}\n"

    context += "=" * 50 + "\n"
    return context
