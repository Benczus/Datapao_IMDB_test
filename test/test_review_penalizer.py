import unittest

import pandas as pd
from penalizer import penalize_movie_score


class TestPenalizeMovieScore(unittest.TestCase):
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
                "rating": [9.2, 9.3, 9.0],
                "votes": [1500000, 1200000, 1800000],
            }
        )

    def test_penalize_movie_score(self):
        """
        Tests the `penalize_movie_score` when provided with a valid input DataFrame.
        """
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "rating": [9.2, 9.3, 9.0],
                "votes": [1500000, 1200000, 1800000],
                "adjusted_rating": [8.9, 8.7, 9.0],
            }
        )
        output = penalize_movie_score(self.movies)
        pd.testing.assert_frame_equal(output, expected_output)

    def test_penalize_movie_score_small_data(self):
        """
        Tests the `penalize_movie_score` when all movies have the same number of votes and no penalty is applied.
        """
        movies = self.movies[:2].copy()
        expected_output = pd.DataFrame(
            {
                "title": ["The Godfather", "The Shawshank Redemption"],
                "rating": [9.2, 9.3],
                "votes": [1500000, 1200000],
                "adjusted_rating": [9.2, 9.0],
            }
        )
        output = penalize_movie_score(movies)
        pd.testing.assert_frame_equal(output, expected_output)

    def test_penalize_movie_score_no_penalty(self):
        """
        Tests  the `penalize_movie_score`when one or more movies have negative ratings.
        """
        movies = self.movies.copy()
        movies["votes"] = 500000
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "rating": [9.2, 9.3, 9.0],
                "votes": [500000, 500000, 500000],
                "adjusted_rating": [9.2, 9.3, 9.0],
            }
        )
        output = penalize_movie_score(movies)
        pd.testing.assert_frame_equal(output, expected_output)

    def test_penalize_movie_score_negative_rating(self):
        movies = self.movies.copy()
        movies["rating"] = -1
        expected_output = pd.DataFrame(
            {
                "title": [
                    "The Godfather",
                    "The Shawshank Redemption",
                    "The Dark Knight",
                ],
                "rating": [-1, -1, -1],
                "votes": [1500000, 1200000, 1800000],
                "adjusted_rating": [-1.3, -1.6, -1.0],
            }
        )
        output = penalize_movie_score(movies)
        pd.testing.assert_frame_equal(output, expected_output)
