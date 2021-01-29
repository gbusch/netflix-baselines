import pickle
from random import randint
from math import sqrt


with open("cache/movie_rating.p", "rb") as f:
    MOVIE_RATING = pickle.load(f)

with open("cache/user_rating.p", "rb") as f:
    USER_RATING = pickle.load(f)

with open("cache/movie_user_rating.p", "rb") as f:
    MOVIE_USER_RATING = pickle.load(f)


AVG_RATING = 3.6

def predict(user, movie):
    return AVG_RATING + (USER_RATING.get(user, AVG_RATING) - AVG_RATING) + (MOVIE_RATING.get(movie, AVG_RATING) - AVG_RATING)

BASELINE0 = []
BASELINE1 = []
BASELINE2 = []
BASELINE3 = []

with open("data/probe.txt", "r") as file:
    movie_id = ""
    for line in file:
        if ":" in line:
            movie_id = line.split(":")[0]
            predictions = MOVIE_USER_RATING[movie_id]
            movie_prediction = MOVIE_RATING[movie_id]
        else:
            user_id = line.split()[0]
            expected = predictions[user_id]
            BASELINE0.append((expected - randint(1, 5))**2)
            BASELINE1.append((expected - AVG_RATING)**2)
            BASELINE2.append((expected - movie_prediction)**2)
            BASELINE3.append((expected - predict(user_id, movie_id))**2)

print(f"baseline random rsme: {sqrt(sum(BASELINE0)/len(BASELINE0))}")
print(f"baseline overall average rsme: {sqrt(sum(BASELINE1)/len(BASELINE1))}")
print(f"baseline average of movie: {sqrt(sum(BASELINE2)/len(BASELINE2))}")
print(f"baseline user/movie correction rsme: {sqrt(sum(BASELINE3)/len(BASELINE3))}")
