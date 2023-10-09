# 4 Octobre, 2023
## History
1. Trying to find a way for making group recommender system
2. After looking through the slides looks not as difficult
    - main problem is to generate synthetic groups
    - next just choose one of the straightforward group score aggregators and can predict
3. How to generate the groups?
    - synthetically 
    - assume we are doing a government "help employement program" (i.e. government conducts group courses on job application based on peoples choice)
    - then the main criterion will be again distance from each other
    - alternatively instead of "government" can assume that a bunch of friends are given an opportunity to visit "job application" sessions provided by some company:
        - then need to look at the distance as well (states)
        - should also look at cities (easier to become friends if you are closer to...)
        - might also need to look at the degree obtained  
4. Group evaluation might be more problematic though...

# 5 Octobre, 2023
1. Giving up on 2-grams. Just use single keywords to group members. Even if that is too difficult then I will just do an exact match then
2. After talking with the group I am working on generating synthetic groups
    - finnished the code in the second las ipynb cell
    - TODO: transfer from ipynb cell to util.py function

# 6 Octobre, 2023
1. Finnished 2. from 5th Octobre

# 7 Octobre, 2023
1. Thinking about group aggregation
    - now I have the groups
    - next what I need is to train the User-User knn on Tine's data
        - I will need to pick either full dataset or only part of it
            - This depends on what the "coupled" evaluation is using
    - after training it I need to generate recommendations and their scores for each user
        - then I create a list of all the possible jobs and scores from each user
        - then follows the aggregation strategy that picks top x
    - Afterwards must follow a step with evaluation, but I think this is a task for someone else
2. Started implementation
    - Implemented the training on full data as well as import of group gen
    - Ecnounterred stupid python directories non importable problem
    - Tried to solve, but waste of time
        - Next time just import a copy of the file needed (util.py)
        - place timers to solve such problems?

# 8 Octobre, 2023
1. Import stupid files I need and see if ipynb works
    - done
2. Tried to start making a user-item matrix of ratings
    - encounterred indexing error problem and wasting lots of time to solve it

# 9 Octobre, 2023
1. Maybe try to reindex then concatenate?
2. Figured out that the problem was concatenating on columns (leading to creation of incomprehensible columns)
    - instead should have been concatenating on rows
3. Found out about batch recommendations via lenskit
    - had difficulty with running multiple processes in parallel hence used n_jobs=1
4. Started thinking about how to do aggregation:
    - I am assuming that I would need to use all the possible recommendations for each user (i.e. I can't restrict to top 100 or top 10)
5. What to do with users that have no recommendations? (prbably because don't have enough neighbours)
    - for now I will ignore them (i.e. not consider them when aggregating)
