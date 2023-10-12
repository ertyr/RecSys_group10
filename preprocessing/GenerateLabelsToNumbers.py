from collections import defaultdict
import collections
import numbers
from pathlib import Path
import re
from typing import Any, Type
from tqdm import tqdm
from uszipcode import SearchEngine
import pandas as pd

df: pd.DataFrame = pd.read_table('dataset/users.tsv', index_col='UserID')
#search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)

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
                
def zip_facts(country_code: str, zipcode) -> dict[str, numbers.Real]:
    ans: dict[str, numbers.Real] = {}
    if country_code == "US":
        search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
        z = search.by_zipcode(zipcode)
        if not z is None:
            z = z.to_dict()
            ans = dict2Real(z)
    return ans

def apply_zip_facts(row):
    d = zip_facts(row['Country'], row['ZipCode'])
    ans = pd.Series(d).to_frame().T
    ans.index = [row.name]
    return ans
  
degree_type: dict[str,int] = defaultdict(int)
degree_type.update({"Master's":5, 'High School':1, "Bachelor's":4, 'Vocational':2, "Associate's":3, 'PhD':6})
currently_employed: dict[str, int] = defaultdict(int)
currently_employed.update({'Yes': 2, 'No': 1})
managed_others: dict[str, int] = defaultdict(int)
managed_others.update({'No':1, 'Yes':2})
def users_to_vector(users: pd.DataFrame) -> pd.DataFrame:
    tqdm.pandas()
    ans: pd.DataFrame = users['WindowID'].to_frame()
    ans['Split'] = users['Split']
    print('ZipCode')
    temp = None
    for i in tqdm(users.index):
        row = users.loc[i]
        if temp is None:
            temp = apply_zip_facts(row)
        else:
            temp = pd.concat([temp, apply_zip_facts(row)])
    ans = ans.join(temp, how='inner')
    # TODO improve 'DegreeType'
    ans['DegreeType'] = users['DegreeType'].map(degree_type)
    # TODO 'Major'
    ans['TODO Major'] = users['Major']
    ans['GraduationDate'] = pd.to_datetime(users['GraduationDate']).astype('int64') // 10**9
    ans['WorkHistoryCount'] = users['WorkHistoryCount']
    ans['TotalYearsExperience'] = users['TotalYearsExperience']
    ans['CurrentlyEmployed'] = users['CurrentlyEmployed'].map(currently_employed)
    ans['ManagedOthers'] = users['ManagedOthers'].map(managed_others)
    ans['ManagedHowMany'] = users['ManagedHowMany']
    return ans

#df = df.iloc[0:10]
df = users_to_vector(df)
print(df)
filepath = Path('users_as_vectors.csv')
df.to_csv(filepath)