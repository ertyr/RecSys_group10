## import packages
import pandas as pd
import numpy as np

def aggregate(all_ratings, num_pref = 5, strat = None, limit = None):
    """
    ### Summary:
        Aggregate the top results based on group ratings. 

    ### Parameters:
        - all_ratings: A list of all ratings for the group. Label is the list of members of the group, ratings_grp consists of items, scores, users, and ranks
        - num_pref: The number of aggregated results / DEFAULT = 5
        - strat: Aggregation strategy - 'add' = additive / 'mult' = multiplicative / 'misery' = least misery / 'pleasure' = most pleasure / DEFAULT = additive
        - limit: Limiting the data between 1-0 - 'cap' clipping scores / 'norm' normalize score / 'sig' sigmoid function / DEFAULT = no limit
    ### Returns:
        Dataframe with 2 columns Members (list of members in group) and Recommendation (list of top num_pref aggregations)
    """

    group_preference = pd.DataFrame(columns=["Members", "Recommendation"])
    for label, ratings_grp in all_ratings:
        pref = pd.DataFrame()

        # Perform any other operations or analysis on the DataFrame as needed
        unique_items = ratings_grp["item"].unique().tolist()

        for item in unique_items:
            job_scores = ratings_grp[ratings_grp["item"] == item]
            scores = job_scores["score"].tolist()

            if len(scores) > 1:
                if limit == "cap":
                    scores = np.clip(scores, 0, 1)

                elif limit == "sig":
                    scores = [1 / (1 + np.exp(-x)) for x in scores]

                elif limit == "norm":
                    min_score = min(scores)
                    max_score = max(scores)
                    if min_score == max_score:
                        scores = [0.5] * len(scores)
                    else:
                        scores = [
                            ((score - min_score) / (max_score - min_score))
                            for score in scores
                        ]
                

            if strat == "add" or strat == None:
                temp_item_df = pd.DataFrame(
                    {"Item": [item], "Total_Score": [sum(scores)]}
                )

            elif strat == "mult":
                product = 1
                for s in scores:
                    product *= s

                temp_item_df = pd.DataFrame({"Item": [item], "Total_Score": [product]})
            elif strat == "misery":
                temp_item_df = pd.DataFrame(
                    {"Item": [item], "Total_Score": [min(scores)]}
                )

            elif strat == "pleasure":
                temp_item_df = pd.DataFrame(
                    {"Item": [item], "Total_Score": [max(scores)]}
                )

            pref = pd.concat([pref, temp_item_df], ignore_index=True)

        pref = pref.sort_values(by="Total_Score", ascending=False)
        pref = pref.head(num_pref)

        top_items = pref["Item"].tolist()

        temp_score_list_df = pd.DataFrame(
            {"Members": [label], "Recommendation": [top_items]}
        )
        group_preference = pd.concat(
            [group_preference, temp_score_list_df], ignore_index=True
        )

    return group_preference