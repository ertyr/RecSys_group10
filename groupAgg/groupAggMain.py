## import packages
from util import createGrps
import pandas as pd
import numpy as np
from lenskit.algorithms import Recommender
from lenskit.algorithms import Predictor
from lenskit.algorithms.user_knn import UserUser
from lenskit import batch
import sys

## Methods
def cap(x):
    if x > 1.0:
        return 1.0
    elif x < 0.0:
        return 0.0
    return x 


## Get the training data and train the user-user collaborative filterring
# read the data (about applications)
# TODO: replace by Tine's filter  data
data = pd.read_csv('dataset/user_ratings_neg_1000_20_20_1.csv', delimiter=',')

# load user data
user_data = pd.read_csv('dataset/users.tsv', sep='\t')

## First get the groups
# parameters for group generation
size = 10
grpNum = 20
seed = 12345

# generate synthetic groups of users and display them
groups2 = createGrps(user_data, 10, 10, 12345)

# construct dataframe in format (user, item, rating) via column addition
df_ui = data.rename(columns={"UserID": "user", "JobID": "item", "Rating":"rating"})
# check data being read properly

# train UserUser collaborative filterring
user_user = UserUser(10, min_nbrs=3)  # Minimum (3) and maximum (10) number of neighbors to consider
recsys = Recommender.adapt(user_user)
recsys.fit(df_ui)

## Create a User-Item matrix of scores so we can apply one of the aggregation strategies
# iterate through groups generated
# pd.set_option('display.max_rows', None)
all_ratings = []

## Create a User-Item matrix of scores so we can apply one of the aggregation strategies
# iterate through groups generated
for i, row in groups2.iterrows():
    # get the array of users from the row
    synGrp = row.iloc[0]

    # get recommendations for all group members
    ratings_grp = batch.recommend(recsys, synGrp, n=None,  n_jobs=1)
    
    # cap the values (x > 1 then 1; x < 0 then 0)
    # TODO: if you are confident that you can explain the clamping -> go ahead and use it
    # ratings_grp["score"] = ratings_grp["score"].map(cap)
    # print(ratings_grp)
    # TODO: sys.exit only for demonstration to not run through all 20 groups of users
    all_ratings.append((synGrp, ratings_grp))

num_pref = 5
group_preference = []
index = 0

for label, ratings_grp in all_ratings:
    pref = []
    # Print the label to differentiate the DataFrames
    print("Label:", label)
    
    # Access and work with the ratings_grp DataFrame
    print(ratings_grp)  # Example: Display the first few rows of the DataFrame
    
    # Perform any other operations or analysis on the DataFrame as needed
    unique_items = ratings_grp['item'].unique().tolist()

    for item in unique_items:
        job_scores = ratings_grp[ratings_grp['item'] == item]
        print(job_scores)
        
        # if len(job_scores) > 1:
        #     print("Number of job_scores:", len(job_scores))
        
    index += 1
    sys.exit()
