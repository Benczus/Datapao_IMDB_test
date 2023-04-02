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
    """
    Scrape the number of Oscars won by a movie from its IMDb page.

    Parameters:
    movie_url (str): The URL of the movie's IMDb page.
    headers (dict): A dictionary containing the headers for the HTTP request.

    Returns:
    int: The number of Oscars won by the movie.
    """

    # Create a new HTTP client session
    async with aiohttp.ClientSession() as session:
        # Send an HTTP GET request to the specified URL with the provided headers
        async with session.get(movie_url, headers=headers) as response:
            # Get the response content
            content = await response.text()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")

            try:
                # Try to extract the number of Oscars won by the movie
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
                # If the number of Oscars won cannot be found, set it to 0
                num_oscars = 0

            except Exception as e:
                # Print any exception that may occur during the scraping process
                print(e)

    # Return the number of Oscars won by the movie
    return num_oscars


async def scrape_imdb_top20() -> pd.DataFrame:
    """
    Scrape the top 20 movies on IMDb and return their details in a pandas DataFrame.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the details of the top 20 movies on IMDb.

    """
    # Set the URL to the top 20 movies on IMDb and choose a random user agent
    url = "https://www.imdb.com/chart/top/"
    headers = {"User-Agent": random.choice(user_agents_list)}

    # Create a session and get the response from the URL
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            content = await response.text()

    # Use BeautifulSoup to extract movie details from the HTML content
    soup = BeautifulSoup(content, "html.parser")
    movies = soup.select("tbody.lister-list tr")
    movie_data = []
    tasks = []

    # Loop through the top 20 movies and extract their details
    for movie in movies[:20]:
        title = movie.select_one(".titleColumn a").text
        year = movie.select_one(".titleColumn span.secondaryInfo").text.strip("()")
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

        # Create an asynchronous task to scrape the number of Oscars won by the movie
        tasks.append(asyncio.create_task(scrape_movie_data(movie_url, headers)))

        # Store the movie details in a dictionary
        movie_data.append(
            {
                "title": title,
                "year": year,
                "rating": rating,
                "votes": votes,
            }
        )

    # Run the asynchronous tasks to scrape the number of Oscars won by each movie
    oscars = await asyncio.gather(*tasks)

    # Add the number of Oscars won by each movie to the movie data dictionary
    for i in range(len(movie_data)):
        movie_data[i]["num_oscars"] = oscars[i]

    # Return the movie data as a pandas DataFrame
    return pd.DataFrame(movie_data)


async def pipeline():
    movies = await scrape_imdb_top20()
    penalized_movies = penalize_movie_score(movies)
    rewarded = rewards_oscars(penalized_movies)
    print(rewarded)


if __name__ == "__main__":
    asyncio.run(pipeline())
