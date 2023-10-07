# check everything works in python functions
import groupGen.util
import random
import pandas as pd
import numpy as np

# parameters for group generation
size = 20
grpNum = 20
seed = 1234567

# load user data
user_data = pd.read_csv("dataset/users.tsv", sep='\t')
#print(user_data.head(10))
#print()

#generate synthetic groups of users and display them
groups2 = util.createGrps(user_data, size, grpNum)
print(groups2)
print()