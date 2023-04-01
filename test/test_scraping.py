import unittest
from unittest.mock import patch

from imdb_scrape import scrape_movie_data


class TestMovieScraper(unittest.IsolatedAsyncioTestCase):
    async def test_scrape_movie_data(self):
        url = "https://www.imdb.com/title/tt0111161/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.36"
        }
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value.text.return_value = """<div class="ipc-metadata-list
            -item__content-container"> <a href="/event/ev0000003/1995/1/" class="ipc-metadata-list-item__label 
            ipc-metadata-list-item__label--link">Won 7 Oscars.</a> </div>"""
            num_oscars = await scrape_movie_data(url, headers)
            self.assertEqual(num_oscars, 7)
