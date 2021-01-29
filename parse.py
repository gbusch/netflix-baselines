from collections import defaultdict
from glob import glob
import pickle

import logging
logging.basicConfig(level=logging.INFO)

USER_MOVIE_RATING = defaultdict(dict)
MOVIE_USER_RATING = defaultdict(dict)
ALL_RATINGS_SUM = 0
ALL_RATINGS_LEN = 0


for filename in glob("data/combined_data_*.txt"):
    logging.info(f"processing input file {filename}")
    with open(filename, "r") as file:
        movie_id = ""
        for line in file:
            if ":" in line:
                movie_id = line.split(":")[0]
                logging.info(f"processing movie: {movie_id}")
            else:
                user_id, rating, _ = line.split(",")
                USER_MOVIE_RATING[user_id][movie_id] = int(rating)
                MOVIE_USER_RATING[movie_id][user_id] = int(rating)
                ALL_RATINGS_SUM += int(rating)
                ALL_RATINGS_LEN += 1


USER_RATING = {user: sum(ratings.values())/(10 + len(ratings)) for user, ratings in USER_MOVIE_RATING.items()}
MOVIE_RATING = {movie: sum(ratings.values())/(5 + len(ratings)) for movie, ratings in MOVIE_USER_RATING.items()}

with open("cache/user_rating.p", "wb") as f:
    pickle.dump(USER_RATING, f)

with open("cache/movie_rating.p", "wb") as f:
    pickle.dump(MOVIE_RATING, f)

with open("cache/user_movie_rating.p", "wb") as f:
    pickle.dump(USER_MOVIE_RATING, f)

with open("cache/movie_user_rating.p", "wb") as f:
    pickle.dump(MOVIE_USER_RATING, f)

OVERALL_RATING = ALL_RATINGS_SUM / ALL_RATINGS_LEN
print(OVERALL_RATING)
