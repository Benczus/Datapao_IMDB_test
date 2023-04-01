import pandas as pd


def rewards_oscars(movies: pd.DataFrame) -> pd.DataFrame:
    rewards = pd.cut(
        movies["num_oscars"],
        bins=[0, 2, 5, 10, float("inf")],
        labels=[0.3, 0.5, 1, 1.5],
    )
    rewards_numeric = rewards.astype(float).fillna(0)
    movies["adjusted_rating"] = (movies["adjusted_rating"] + rewards_numeric).round(1)

    return movies
