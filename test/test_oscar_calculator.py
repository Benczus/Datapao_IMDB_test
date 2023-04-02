import unittest

import numpy as np
import pandas as pd
from oscar_rewarder import rewards_oscars


class TestRewardsOscars(unittest.TestCase):
    def setUp(self):
        """
        Initializes a sample DataFrame of movies with title, rating, and votes columns.
        """
        self.movies = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "num_oscars": [3, 7, 1],
                "adjusted_rating": [9.0, 8.7, 8.5],
            }
        )

    def test_rewards_oscars(self):
        """
        Test the rewards_oscars() function with a valid input.
        """
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "num_oscars": [3, 7, 1],
                "adjusted_rating": [9.5, 9.7, 8.8],
            }
        )
        output = rewards_oscars(self.movies)
        pd.testing.assert_frame_equal(output, expected_output)

    def test_rewards_oscars_no_oscar_wins(self):
        """
        Test the rewards_oscars() function with all movies having no oscar wins.
        """
        movies = self.movies.copy()
        movies["num_oscars"] = 0
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "num_oscars": [0, 0, 0],
                "adjusted_rating": [9.0, 8.7, 8.5],
            }
        )
        output = rewards_oscars(movies)
        pd.testing.assert_frame_equal(output, expected_output)

    def test_rewards_oscars_negative_rating(self):
        """
        Test the rewards_oscars() function with a negative adjusted rating.
        """
        movies = self.movies.copy()
        movies["adjusted_rating"] = -1
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "num_oscars": [3, 7, 1],
                "adjusted_rating": [-0.5, -0.0, -0.7],
            }
        )
        output = rewards_oscars(movies)
        pd.testing.assert_frame_equal(output, expected_output)

    def test_rewards_oscars_nan_oscar_wins(self):
        """
        Test the rewards_oscars() function with NaN values for num_oscars.
        """
        movies = self.movies.copy()
        movies["num_oscars"] = np.nan
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "num_oscars": [np.nan, np.nan, np.nan],
                "adjusted_rating": [9.0, 8.7, 8.5],
            }
        )
        output = rewards_oscars(movies)
        pd.testing.assert_frame_equal(output, expected_output)
