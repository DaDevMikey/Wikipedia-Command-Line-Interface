import aiohttp
import asyncio
from urllib.parse import quote
from .config import Config

class WikiAPI:
    def __init__(self, language=Config.DEFAULT_LANGUAGE):
        self.language = language
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            'User-Agent': Config.USER_AGENT
        })
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search(self, query, limit=5):
        """Search Wikipedia articles"""
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'srlimit': limit
        }
        
        async with self.session.get(Config.get_api_url(self.language), params=params) as response:
            data = await response.json()
            return data['query']['search']
    
    async def get_article(self, title):
        """Get full article content"""
        params = {
            'action': 'query',
            'prop': 'extracts|extlinks|images',
            'titles': title,
            'format': 'json',
            'explaintext': 1,
            'exsectionformat': 'wiki'
        }
        
        async with self.session.get(Config.get_api_url(self.language), params=params) as response:
            data = await response.json()
            pages = data['query']['pages']
            return next(iter(pages.values()))
    
    async def get_image_info(self, title):
        """Get image information"""
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'imageinfo',
            'iiprop': 'url',
            'format': 'json'
        }
        
        async with self.session.get(Config.get_api_url(self.language), params=params) as response:
            data = await response.json()
            pages = data['query']['pages']
            page = next(iter(pages.values()))
            return page.get('imageinfo', [{}])[0].get('url')
