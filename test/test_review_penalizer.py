import unittest
import pandas as pd

from penalizer import penalize_movie_score


class TestPenalizeMovieScore(unittest.TestCase):
    def setUp(self):
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
