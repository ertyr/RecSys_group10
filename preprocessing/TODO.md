# Things left to do
1. Express all user data values (except for postal code) numerically
2. Implement similarity
## Fun stuff to add
User vector expansion


Job description -> encoder -> neat -> vector length user vector + 1 = v_j.  
User data -> expended user data numerical vector -> + distance to job = v_u.  
Application probability = v_j dot product v_u.  
Train neat with a fitness function that ranks high: uniformly distributed application probabilities over all jobs, high application probabilities for all jobs applied to.