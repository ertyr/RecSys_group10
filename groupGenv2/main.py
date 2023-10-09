## Import packages
import pandas as pd

## Methods
def elimNeg(x):
    """Eliminate neagtives"""
    if x < 0.0:
        return 0.0
    return x

## Do the parameter set_up for groupGeneration
group_size_to_create = 20
group_number = 20

## Get the data and elminate Tine's negative ones
ratings_df = pd.read_csv("dataset/clean/user_ratings_neg_1000_20_20_1.csv") 
ratings_df["Rating"] = ratings_df["Rating"].apply(lambda x: elimNeg(x))
# rename the columns in an appropriate way
