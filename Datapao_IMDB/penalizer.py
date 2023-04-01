import numpy as np
import pandas as pd


def penalize_movie_score(movies: pd.DataFrame) -> pd.DataFrame:
    max_ratings = movies["votes"].nlargest(20).max()
    penalty = (movies["votes"] - max_ratings) // 100000 * 0.1

    # Apply the penalty to the movie scores
    movies["adjusted_rating"] = np.round(movies["rating"] + penalty, 1)

    return movies
