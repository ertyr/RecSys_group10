import pandas as pd
import numpy as np
import random
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser
from lenskit.algorithms import user_knn
from lenskit.algorithms import Recommender

def createGrps(user_data, size, grpNum, seed = None):
    """
    Summary:
        Break into users by education level. Then break each of these groups by state. 
        For graduate education level additionally break by major. Then randomly select 
        education level, state (and major if education level is "graduates"). Using 
        these values generate a group of <size> users. Generate <grpNum> groups in the 
        same way and return them.
    Some assumptions:
        1. One user can be in multiple groups
        2. Same state can be selected multiple times
        3. Same major can be selected multiple times
        4. Same education level can be selected multiple times
    Parameters:
        - user_data - dataframe containing information about all the users
        - size - number of users per one group
        - grpNum - number of groups to generate
        - seed - if you want to generate the same groups (i.e. used to make random generate output same things)
    Returns:
        dataframe containing <grpNum> rows. Note that the value in "Users" column is a string (even though it looks like an array)
    """
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
    majorLen = len(major_col)

    # set randomness seed
    if (seed!=None): random.seed(seed)
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
        stt = state_col["State"].loc[rndState]
        working_data = working_data[working_data["State"]==stt]

        # Then if graduate group also split by random major
        if grp == 2:
            rndMaj = random.randint(0,majorLen-1)
            maj = major_col["Major"].loc[rndMaj]
            working_data = working_data[working_data["State"]==maj]
        
        # select <size> (e.g. 20) random users
        if (len(working_data)>size-1): # if working dataset has less than <size> (e.g. 20) number of users then ignore because can't reach desired number of users
            users = selectUsersRand(working_data, size)
            #groups.loc[grpCount] = [users]     # if you want to get dataframe of series instead
            groups.loc[grpCount] = np.array2string(users)
            
            # form next group
            grpCount+=1
    return groups

def selectUsersRand(working_data, size):
    """
    Select <size> users randomly from <working_data> (i.e. dataframe for users with same education 
    level, state and major)
    """
    edited_data = working_data
    cntr = 0
    users = np.array([])
    #display(edited_data)
    while cntr < size:
        id = random.choice(np.array(edited_data["UserID"]))
        users = np.append(users, id)
        edited_data = edited_data[edited_data["UserID"]!=id]
        cntr+=1
        if(len(edited_data)==0): break
    return users