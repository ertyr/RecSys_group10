#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 12:44:49 2020

@author: shah
"""
from util import random_vector
class user:
    def __init__(self, userid):
        self.userid = userid
        self.movies_train = dict()
        self.movies_test = dict()
        self.movies_all = dict()
        self.factor = random_vector()
    
    def __str__(self) -> str:
        return "ID: " + str(self.userid) + ", Train: " + str(self.movies_train) + ", Factor: " + str(self.factor)
    
    def __repr__(self) -> str:
        return "ID: " + str(self.userid) + ", Train: " + str(self.movies_train) + ", Factor: " + str(self.factor)
    
class movie:
    def __init__(self, movieid, rating=0, title=None, genres=None):
        self.movieid = movieid
        self.rating = rating
        self.title = title
        self.genres = genres
        self.factor = random_vector()

class ret:
    def __init__(self):
        self.userid = None
        self.movieid = None
        self.isuser = True
        self.retvalue = []
    
class usermovie:
    def __init__(self):
        self.userid = None
        self.movieid = None
        self.rating = 0