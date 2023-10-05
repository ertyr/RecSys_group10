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