from math import atan2, cos, sin, sqrt
import pandas as pd
import pgeocode

def location_user(user: pd.DataFrame) -> pd.DataFrame:
    """Location of a user

    Args:
        user (pd.DataFrame): the row identifying the user, from a pandas.DataFrame from users.tsv

    Returns:
        pd.DataFrame: a pandas.DataFrame containing information about the location of the user
    """ 
    return pgeocode.Nominatim(user['Country']).query_postal_code(user['ZipCode'])

def location_job(job: pd.DataFrame) -> pd.DataFrame:
    """Location of a job

    Args:
        job (pd.DataFrame): the row identifying the job, from a pandas.DataFrame from jobs.tsv

    Returns:
        pd.DataFrame: a pandas.DataFrame containing information about the location of the job
    """    
    return pgeocode.Nominatim(job['Country']).query_postal_code(job['Zip5'])
    
R = 6373.0 # radius of the earth
def distance(location_a: pd.DataFrame, location_b: pd.DataFrame) -> float:
    """The distance between two points

    Args:
        location_a (pd.DataFrame): output of location_user or location_job for thing a
        location_b (pd.DataFrame): output of location_user or location_job for thing b

    Returns:
        float: approximate distance in km
    """    
    difference_longitude = location_b['longitude'] - location_a['longitude']
    difference_latitude = location_b['latitude'] - location_a['latitude']
    a = sin(difference_latitude/2)**2+ cos(location_a['latitude']) * cos(location_b['latitude']) * sin(difference_longitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
    