import numpy as np
import pandas as pd
import sys



def groupNDCG(group_members, group_recommendation, recsys):
    ndcg_list = list()
    for user in group_members:
        #TODO: user dataframe here to calculate the ground truth
        user_ground_truth = recsys.recommend(user) # dataframe with [item, rating]
        ndcg_user = evaluateUserNDCG(user_ground_truth, group_recommendation)
        ndcg_list.append(ndcg_user)

    meanNDCG = np.mean(ndcg_list)
    minNCDG = np.amin(ndcg_list)
    maxNDCG = np.amax(ndcg_list)

    return meanNDCG, minNCDG, maxNDCG


def evaluateUserNDCG(user_ground_truth, group_recommendation):
        """
        Looks like ndcg doesn't care about the position and scores in the actual items recommended hence why it outputs large scores close to 1"""
        # note that both dcg and idcg should be element-wise normalized via per_user_propensity_normalization_term
        # therefore, it can be excluded from calculations
        dcg = 0.0

        for k, item in enumerate(group_recommendation):
            if (checkIn(user_ground_truth["item"], item)):
                numerator = (user_ground_truth["score"].loc[user_ground_truth["item"] == item]).iloc[0]
                dcg = dcg + ((numerator) / (np.log2(k + 2)))
            
        idcg = 0.0

        # sort the values to get highest scores first and then compute the most ideal score possible
        user_ground_truth.sort_values("score", inplace=True, ascending=False)

        for k in range(min(len(user_ground_truth), len(group_recommendation))):
            idcg = idcg + (user_ground_truth.iloc[k]["score"] / np.log2(k + 2))
        if idcg > 0.0:
            ndcg = dcg / idcg
        else:
            ndcg = 0.0
        return ndcg

def checkIn(series, checkNum):
    for num in series:
        if num == checkNum:
            return True
    return False

