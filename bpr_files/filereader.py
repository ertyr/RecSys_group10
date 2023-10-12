#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 12:44:43 2020

@author: shah
"""
from classes import user
from classes import movie
from numpy import random
from util import min_rating, random_vector, num_users
from random import seed
import pandas as pd
import numpy as np
def read_ratings(filename):
    seed(42)
    np.random.seed(42)
    r_cols = ['UserID','JobID','Rating']
    ratings = pd.read_csv(filename,  sep=',', names=r_cols, encoding='latin-1',skiprows=[0])
    print(ratings.head())
    ratings['UserID'] = ratings['UserID'].astype('int')
    ratings['JobID'] = ratings['JobID'].astype('int')
    ratings['Rating'] = ratings['Rating'].astype('float')
    print(ratings.shape())
    numusers = num_users()
    #print(ratings['UserID'])
    msks = ratings['UserID'] < numusers
    ratings = ratings[msks]
    users = dict()
    testcount = 0
    traincount = 0
    trainuserdict = dict()

    for index, row in ratings.iterrows():
        userid = int(row['UserID'])
        movieid = int(row['JobID'])
        rating1 = float(row['Rating'])
        minmovierating = min_rating()
        if rating1 >= minmovierating:
            if random.random() < 0.7:
                traincount = traincount + 1
                if userid in users.keys():
                    user1 = users[userid]
                    user1.movies_train[movieid] = rating1
                else:
                    user1 = user(userid)
                    user1.factor = random_vector()
                    user1.movies_train[movieid] = rating1
                    users[userid] = user1
                    trainuserdict[userid] = 1
            else:
                testcount = testcount + 1
                if userid in users.keys():
                    user1 = users[userid]
                    user1.movies_test[movieid] = rating1
                else:
                    user1 = user(userid)
                    user1.factor = random_vector()
                    user1.movies_test[movieid] = rating1
                    users[userid] = user1

    for index, row in ratings.iterrows():
        userid = int(row['UserID'])
        movieid = int(row['JobID'])
        rating1 = float(row['Rating'])
        if userid in users.keys():
            user1 = users[userid]
            user1.movies_all[movieid] = rating1

    return users

def read_movies(filename):
    r_cols = ['JobID',	'WindowID',	'Title',	'Description',	'Requirements'	'City'	,'State',	'Country',	'Zip5'	,'StartDate'	,'EndDate']
    df = pd.read_table(filename, sep="\t", encoding='latin-1', names= r_cols, on_bad_lines='skip', low_memory=False, skiprows= [0])
    movies = dict()
    for index, row in df.iterrows():
        movieid = row['JobID']
        movie1 = movie(movieid, 0)
        movie1.factor = random_vector()
        movies[movieid] = movie1

    return movies
