## Import packages
from util import createGrps
import pandas as pd
import numpy as np
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser
import sys


## First get the groups
# parameters for group generation
size = 20
grpNum = 20
seed = 12345

# load user data
user_data = pd.read_csv("dataset/users.tsv", sep='\t')

# generate synthetic groups of users and display them
groups2 = createGrps(user_data, size, grpNum, seed)
print(groups2)
print()


## Get the training data and train the user-user collaborative filterring
# read the data (about applications)
data = pd.read_csv('user_with_negative_ratings_full.csv', delimiter=',')

# construct dataframe in format (user, item, rating) via column addition
df_ui = data.rename(columns={"UserID": "user", "JobID": "item", "Rating":"rating"})
# check data being read properly
print(df_ui.head(10)) 

# train UserUser collaborative filterring
user_user = UserUser(10, min_nbrs=3)  # Minimum (3) and maximum (10) number of neighbors to consider
recsys = Recommender.adapt(user_user)
recsys.fit(df_ui)


## Create a User-Item matrix of scores so we can apply one of the aggregation strategies
# iterate through groups generated
for i, row in groups2.iterrows():
    # get the array of users from the row
    synGrp = row[0]
    # create empty dataframe for ratings of Users to Items
    ratings_grp = pd.DataFrame(columns=["UserID", "item", "score"])
    # create an empty dataframe to store unique jobs of this syn group
    items_grp = pd.DataFrame(columns=["item"])
    # iterate through each user and generate top 10 recommendations
    db_ind = 0
    for userId in synGrp:
        # generate top 10: (item, score)
        top10 = recsys.recommend(userId, 10)
        # concatenate and drop duplicates to store the jobs
        items_grp = (pd.concat([items_grp, top10[["item"]]], axis=0, ignore_index=True)).drop_duplicates()
        # add top 10 with associated user ID
        top10.insert(0, "UserID", np.full((len(top10), 1), userId), True)
        if (db_ind==2): sys.exit()
        db_ind+=1


