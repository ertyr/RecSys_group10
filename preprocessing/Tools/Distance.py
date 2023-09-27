from math import atan2, cos, sin, sqrt
import pandas as pd
import pgeocode
from pgeocode import Nominatim

ns: dict[str, Nominatim] = {}
class Location:
    def __init__(self, country:str, zip_code:int) -> None:
        if not country in ns.keys():
            ns[country] = pgeocode.Nominatim(country)
        self.loc = ns[country].query_postal_code(zip_code)
    def country_code(self) -> str:
        return self.loc['country_code']
    def postal_code(self) -> int:
        return self.loc['postal_code']
    def place_name(self) -> str:
        return self.loc['place_name']
    def state_name(self) -> str:
        return self.loc['state_name']
    def state_code(self) -> str:
        return self.loc['state_code']
    def county_name(self) -> str:
        return self.loc['county_name']
    def county_code(self) -> str:
        return self.loc['county_code']
    def community_name(self) -> str:
        return self.loc['community_name']
    def community_code(self) -> str:
        return self.loc['community_code']
    def latitude(self) -> float:
        return self.loc['latitude']
    def longitude(self) -> float:
        return self.loc['longitude']
    def accuracy(self) -> float:
        return self.loc['accuracy']
    

def location_user(user: pd.DataFrame) -> Location:
    """Location of a user

    Args:
        user (pd.DataFrame): the row identifying the user, from a pandas.DataFrame from users.tsv

    Returns:
        pd.DataFrame: a pandas.DataFrame containing information about the location of the user
    """ 
    return Location(user.iloc[0]['Country'], user.iloc[0]['ZipCode'])

def location_job(job: pd.DataFrame) -> Location:
    """Location of a job

    Args:
        job (pd.DataFrame): the row identifying the job, from a pandas.DataFrame from jobs.tsv

    Returns:
        pd.DataFrame: a pandas.DataFrame containing information about the location of the job
    """    
    return Location(job.iloc[0]['Country'], job.iloc[0]['Zip5'])
    
R = 6373.0 # radius of the earth
def distance(location_a: Location, location_b: Location) -> float:
    """The distance between two points

    Args:
        location_a (pd.DataFrame): output of location_user or location_job for thing a
        location_b (pd.DataFrame): output of location_user or location_job for thing b

    Returns:
        float: approximate distance in km
    """    
    difference_longitude = location_b.longitude() - location_a.longitude()
    difference_latitude = location_b.latitude() - location_a.latitude()
    a = sin(difference_latitude/2)**2+ cos(location_a.latitude()) * cos(location_b.latitude()) * sin(difference_longitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

    