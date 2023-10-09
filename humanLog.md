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
    - additionally set the 

# 9 Octobre, 2023
1. Starting the work on the different synthetic group generator algorithm based on the lectures
    - General procedure from the slides:
        - Select member at random 
        - Select most similar users
        - Select randomly users above a certain similarity threshold 
    - Can try knn from sklearn?
        - although seems to be possible might be difficult to justify
        - hence I decided to understnad the method from the lab
2. Spent some time undersntading method from the lab
    - seems to be more or less comprehensible
3. Will try to copy the parts only relevant for similarity
4. Pivoting taking insanely long amount of time
    - t=21m
    - need to save the damn dataframe
    - conversion of dataframe to file also taking quiet long
        - didn't see how long because terminated (will need to rerun everything anyways)
5. Started working on converting alb's group generator code to my version
6. I will need to keep Tine's 1 vs -1 because to dropnas I need to replace them by neutral value (i.e. 0) to be able to compute the similarity