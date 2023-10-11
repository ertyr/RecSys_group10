from collections import defaultdict
import collections
import numbers
import re
from typing import Any
from tqdm import tqdm
from uszipcode import SearchEngine
import pandas as pd

df: pd.DataFrame = pd.read_table('dataset/users.tsv', index_col='UserID')
search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)

# Goes over a dictionary with str keys and returns a dictionary with only real values, purpose build to deal with uszipcode outputs
# 'lat','lng'
pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
ignore_keys: tuple[str,...] = ('zipcode', 'zipcode_type','major_city','post_office_city','common_city_list','county','state','timezone','area_code_list',
                               'bounds_west','bounds_east','bounds_north','bounds_south','polygon')
def dict2Real(dictionary: dict[str, Any]) -> dict[str, numbers.Real]:
    ans: dict[str, numbers.Real] = {}
    for key, value in dictionary.items():
        if not key in ignore_keys:
            match value:
                case numbers.Real():
                    ans[key] = value
                case [{'key': 'Data', 'values': list()}]:
                    a_list_of_dicts_l2 = value[0]['values']
                    for i in a_list_of_dicts_l2:
                        if isinstance(i, dict):
                            ans[key+'_'+str(i['x'])] = i['y']
                        else:
                            print('error')
                case [{'key': 'Male', 'values': list()}, {'key': 'Female', 'values': list()}, {'key': 'Total', 'values': list()}]:
                    for i in value:
                        key2 = i['key']
                        a_list_of_dicts_l2 = i['values']
                        for i in a_list_of_dicts_l2:
                            if isinstance(i, dict):
                                ans[key+'_'+key2+'_'+str(i['x'])] = i['y']
                            else:
                                print('error')
                case [{'key': 'Owner', 'values': list()}, {'key': 'Renter', 'values': list()}, {'key': 'Total', 'values': list()}]:
                    for i in value:
                        key2 = i['key']
                        a_list_of_dicts_l2 = i['values']
                        for i in a_list_of_dicts_l2:
                            if isinstance(i, dict):
                                ans[key+'_'+key2+'_'+str(i['x'])] = i['y']
                            else:
                                print('error')
                case dict():
                    sub_dict = dict2Real(value)
                    if not sub_dict is None:
                        for key2, value2 in sub_dict.items():
                            ans[key+"_"+key2] = value2
                case list():
                    for i in range(len(value)):
                        temp_dict: dict[str, Any] = {str(i): value[i]}
                        sub_dict = dict2Real(temp_dict)
                        if not sub_dict is None:
                            for key2, value2 in sub_dict.items():
                                ans[key+"_"+key2] = value2
                case tuple():
                    for i in range(len(value)):
                        temp_dict = {str(i): value[i]}
                        sub_dict = dict2Real(temp_dict)
                        if not sub_dict is None:
                            for key2, value2 in sub_dict.items():
                                ans[key+"_"+key2] = value2
                case str() if pattern.fullmatch(value):
                    ans[key] = float(value)
                case None:
                    pass
                case _:
                    print("non expected @ dict2Real",key,value)
    return ans
                
                
append: str = "_value"
def zip_facts(country_code: str, zipcode) -> dict[str, numbers.Real]:
    ans: dict[str, numbers.Real] = {}
    if country_code == "US":
        z = search.by_zipcode(zipcode)
        if not z is None:
            z = z.to_dict()
            ans = dict2Real(z)
    return ans
        

degree_type: dict[str,int] = defaultdict(int)
degree_type.update({"Master's":5, 'High School':1, "Bachelor's":4, 'Vocational':2, "Associate's":3, 'PhD':6})
currently_employed: dict[str, int] = defaultdict(int)
currently_employed.update({'Yes': 2, 'No': 1})
managed_others: dict[str, int] = defaultdict(int)
managed_others.update({'No':1, 'Yes':2})

def users_to_vector(users: pd.DataFrame) -> pd.DataFrame:
    ans: pd.DataFrame = users['WindowID'].to_frame()
    ans['Split'] = users['Split']
    print("zip codes")
    for index in tqdm(users.index, total=len(users.index)):
        d = zip_facts(users.at[index, "Country"], users.at[index,"ZipCode"])
        d["UserID"] = index
        ans.loc[index, d.keys()] = d.values()
    ans['DegreeType_value'] = users['DegreeType'].map(degree_type)
    # TODO 'Major'
    # TODO 'GraduationDate'
    ans['WorkHistoryCount_value'] = users['WorkHistoryCount']
    ans['TotalYearsExperience_value'] = users['TotalYearsExperience']
    ans['CurrentlyEmployed_value'] = users['CurrentlyEmployed'].map(currently_employed)
    ans['ManagedOthers_value'] = users['ManagedOthers'].map(managed_others)
    ans['ManagedHowMany_value'] = users['ManagedHowMany']
    return ans
        

print(users_to_vector(df))