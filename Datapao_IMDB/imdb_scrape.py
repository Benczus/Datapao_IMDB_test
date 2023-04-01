import asyncio
import random

import aiohttp as aiohttp
import pandas as pd
from bs4 import BeautifulSoup

from oscar_rewarder import rewards_oscars
from penalizer import penalize_movie_score

user_agents_list = [
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
]


async def scrape_movie_data(movie_url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(movie_url, headers=headers) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            try:
                num_oscars = int(
                    [
                        a.text
                        for a in soup.find_all(
                            class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link"
                        )
                        if "Oscar" in a.text
                    ][0]
                    .split("Won ")[1]
                    .split(" ")[0]
                )
            except IndexError:
                num_oscars = 0
            except Exception as e:
                print(e)
    return num_oscars


async def scrape_imdb_top20():
    url = "https://www.imdb.com/chart/top/"
    headers = {"User-Agent": random.choice(user_agents_list)}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            movies = soup.select("tbody.lister-list tr")
            movie_data = []
            tasks = []
            for movie in movies[:20]:
                title = movie.select_one(".titleColumn a").text
                year = movie.select_one(".titleColumn span.secondaryInfo").text.strip(
                    "()"
                )
                rating = float(movie.select_one(".imdbRating strong").text)
                votes = int(
                    movie.select_one(".imdbRating strong")
                    .attrs["title"]
                    .split("on")[-1]
                    .split()[0]
                    .replace(",", "")
                )
                href = movie.select_one(".titleColumn a")["href"]
                movie_url = f"https://www.imdb.com/{href}"
                tasks.append(asyncio.create_task(scrape_movie_data(movie_url, headers)))
                movie_data.append(
                    {
                        "title": title,
                        "year": year,
                        "rating": rating,
                        "votes": votes,
                    }
                )
            oscars = await asyncio.gather(*tasks)
            for i in range(len(movie_data)):
                movie_data[i]["num_oscars"] = oscars[i]
    return pd.DataFrame(movie_data)


async def pipeline():
    movies = await scrape_imdb_top20()
    penalized_movies = penalize_movie_score(movies)
    rewarded = rewards_oscars(penalized_movies)
    print(rewarded)


if __name__ == "__main__":
    asyncio.run(pipeline())
