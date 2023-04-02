import numpy as np
import pandas as pd


def penalize_movie_score(movies: pd.DataFrame) -> pd.DataFrame:
    """
    Penalizes movie scores based on the number of votes received.

    Parameters:
    movies (pd.DataFrame): A pandas DataFrame containing information about movies,
                           including their ratings and number of votes.

    Returns:
    pd.DataFrame: The input DataFrame with an additional column for adjusted movie ratings.

    """
    # Get the maximum number of votes among the top 20 movies
    max_ratings = movies["votes"].nlargest(20).max()

    # Calculate the penalty based on the number of votes
    penalty = (movies["votes"] - max_ratings) // 100000 * 0.1

    # Apply the penalty to the movie scores
    movies["adjusted_rating"] = np.round(movies["rating"] + penalty, 1)

    return movies
