# check everything works in python functions
import util
import random
import pandas as pd
import numpy as np


size = 20
grpNum = 20
seed = 1234567

user_data = pd.read_csv("dataset/users.tsv", sep='\t')
#print(user_data.head(10))
#print()

groups2 = util.createGrps(user_data, size, grpNum)
print(groups2)
print()