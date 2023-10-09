## Import packages
import pandas as pd
import numpy as np
import os.path
from util import GroupsGenerator
from util import SimilarGroupsGenerator


## Methods
def elimNeg(x):
    """Eliminate neagtives"""
    if x < 0.0:
        return 0.0
    return x

## Do the parameter set_up for groupGeneration
group_size_to_create = 20
group_number = 20
pathToUserMatrix = "user_matrix_full"

## Get the data and elminate Tine's negative ones
ratings_df = pd.read_csv("dataset/clean/user_ratings_neg_1000_20_20_1.csv") 
 # drop weird column showing up out of nowhere
ratings_df= ratings_df.drop(columns=['Unnamed: 0'])
ratings_df["Rating"] = ratings_df["Rating"].apply(lambda x: elimNeg(x))
# rename the columns in an appropriate way
ratings_df = ratings_df.rename(columns={"UserID": "user", "JobID": "item", "Rating": "rating"})

## Start the pivoting
if(os.path.isfile(pathToUserMatrix)):
    user_matrix = pd.read_csv(pathToUserMatrix) 
else: # taking insanely long
    user_matrix = ratings_df.pivot_table(columns='item', index='user', values="rating")

## Compute the correlation coefficent for every user
user_id_set = set(ratings_df['user'])
user_id_indexes = user_matrix.index.values
user_matrix = user_matrix.fillna(0) # hmm looks like 1, -1 ratings starts to make sense
numpy_array = user_matrix.to_numpy() 
sim_matrix = np.corrcoef(numpy_array) # comoute correlation coefficent matrix

## Generate groups
grpGenerator = SimilarGroupsGenerator()
current_list = grpGenerator.generateGroups(user_id_indexes, user_id_set, sim_matrix, group_sizes_to_create, group_number)
    
print(pd.DataFrame.from_records(current_list))
