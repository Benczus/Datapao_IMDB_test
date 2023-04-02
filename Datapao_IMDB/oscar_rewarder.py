import pandas as pd


def rewards_oscars(movies: pd.DataFrame) -> pd.DataFrame:
    """
    Adjusts the ratings of movies based on the number of Oscars they have won.

    Parameters:
    - movies (pd.DataFrame): a Pandas DataFrame containing movie data including
        the number of Oscars won and an initial adjusted rating.

    Returns:
    - pd.DataFrame: a Pandas DataFrame containing the adjusted ratings of movies
        with additional rewards based on the number of Oscars won.
    """
    # Define the reward tiers based on the number of Oscars won
    rewards = pd.cut(
        movies["num_oscars"],
        bins=[0, 2, 5, 10, float("inf")],
        labels=[0.3, 0.5, 1, 1.5],
    )
    # Convert the rewards to a numeric format and fill any missing values with 0
    rewards_numeric = rewards.astype(float).fillna(0)
    # Add the rewards to the initial adjusted rating and round to 1 decimal place
    movies["adjusted_rating"] = (movies["adjusted_rating"] + rewards_numeric).round(1)

    return movies
