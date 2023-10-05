import pandas as pd
import numpy as np
import random
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser
from lenskit.algorithms import user_knn
from lenskit.algorithms import Recommender

def createGrps(user_data, size, grpNum, seed):
    # create empty dataframe for groups
    groups = pd.DataFrame([], columns=["Users"])

    # extract high schoolers
    undergrads_data = user_data[user_data["DegreeType"]=="High School"]
    undergrads_data = undergrads_data.reset_index(drop=True).fillna("Not Applicable")

    # extract non high schoolers
    grads_data = user_data.fillna("Not Applicable")
    grads_data = grads_data[(grads_data["DegreeType"]!="High School") & (grads_data["DegreeType"]!="Not Applicable")]
    grads_data = grads_data.reset_index(drop=True)

    # extract no education
    noedu_data = user_data.fillna("Not Applicable")
    noedu_data = noedu_data[noedu_data["DegreeType"]=="Not Applicable"]
    noedu_data = noedu_data.reset_index(drop=True)

    # extract unique column of states
    state_col_0 = noedu_data[["State"]].drop_duplicates().reset_index(drop=True)
    
    state_col_1 = undergrads_data[["State"]].drop_duplicates().reset_index(drop=True)
    
    state_col_2 = grads_data[["State"]].drop_duplicates().reset_index(drop=True)

    # extract unqiue column of majors 
    major_col = grads_data[["Major"]].drop_duplicates().reset_index(drop=True)
    majorLen = len(grads_data)

    # set randomness seed
    random.seed(seed)
    # start generating groups of user ids
    grpCount = 0
    while grpCount < grpNum:
        # choose which of three large groups to access
        grp = random.randint(0,2)
        if grp == 0: # no education group
            working_data = noedu_data
            state_col = state_col_0
        elif grp == 1: # high school group
            working_data = undergrads_data
            state_col = state_col_1
        else: # (grp == 2) # graduate group
            working_data = grads_data
            state_col = state_col_2

        # get length of entries
        stateLen = len(state_col)

        # After selecting one of three large groups split by random state
        rndState = random.randint(0,stateLen-1)
        stt = state_col.loc[rndState]
        working_data = working_data[working_data["State"]==stt]

        # Then if graduate group also split by random major
        if grp == 2:
            rndMaj = random.randint(0,majorLen-1)
            maj = major_col.iloc[rndMaj]
            working_data = working_data[working_data["State"]==maj]
        
        # select <size> (e.g. 20) random users
        users = selectUsersRand(working_data, size)
        groups[grpCount] = users

        # form next group
        grpCount+=1


def selectUsersRand(working_data, size):
    edited_data = working_data
    cntr = 0
    users = np.array([])
    print("Here1")
    while cntr < size:
        id = random.choice(edited_data["UserID"])
        print("Here2")
        users.append(id)
        edited_data = edited_data.drop(edited_data["UserID"]==id)
        cntr+=1
    return users