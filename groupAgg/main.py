## import packages
import createGrps.util
import pandas as pd
import numpy as np
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser


## First get the groups
# parameters for group generation
size = 20
grpNum = 20
seed = 1234567

# load user data
user_data = pd.read_csv("dataset/users.tsv", sep='\t')

# generate synthetic groups of users and display them
groups2 = createGrps(user_data, size, grpNum)
print(groups2)
print()


## Get the training data and train the user-user collaborative filterring
# read the data (about applications)
data = pd.read_csv('dataset/user_with_negative_ratings_full.csv', delimiter=',')

# construct dataframe in format (user, item, rating) via column addition
df_ui = data.rename(columns={"UserID": "user", "JobID": "item", "Rating":"rating"})
# check data being read properly
print(df_ui.head(10)) 

# Train UserUser collaborative filterring
user_user = UserUser(10, min_nbrs=3)  # Minimum (3) and maximum (10) number of neighbors to consider
recsys = Recommender.adapt(user_user)
recsys.fit(df_ui)


## Create a User-Item matrix of scores so we can apply one of the aggregation strategies
# iterate through groups generated
for i, row in groups2.iterrow():
    print(row)