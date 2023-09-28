import pandas
from collections import defaultdict as ddict

data_path = './dataset/'

print("Recording job locations...")
job_info = {}
jobs_df = pandas.read_table(data_path+'jobs.tsv', on_bad_lines='skip', low_memory=False)
print('jobs.tsv size:', jobs_df.shape)
for (idx, job) in jobs_df.iterrows():
    job_info[str(job['JobID'])] = [int(job['WindowID']), job['State'], job['City'], 0]

print("Counting applications...")
apps_df = pandas.read_table(data_path+'apps.tsv', on_bad_lines='skip')
print('apps.tsv size:', apps_df.shape)
for (idx, app) in apps_df.iterrows():
    if app['JobID'] in job_info.keys():
        job_info[app['JobID']][3] += 1

print("Sorting jobs on based on popularity...")
top_city_jobs = ddict(lambda: ddict(lambda: ddict(list)))
top_state_jobs = ddict(lambda: ddict(list))
for (jobID, (windowID, state, city, count)) in job_info.items():
    top_city_jobs[windowID][state][city].append((jobID, count))
    top_state_jobs[windowID][state].append((jobID, count))

for window in [1, 2, 3, 4, 5, 6, 7]:
    for state in top_city_jobs[window]:
        for city in top_city_jobs[window][state]:
            top_city_jobs[window][state][city].sort(key=lambda x: x[1])
            top_city_jobs[window][state][city].reverse()

    for state in top_state_jobs[window]:
        top_state_jobs[window][state].sort(key=lambda x: x[1])
        top_state_jobs[window][state].reverse()

print("Making predictions...")
popular_data = []
users_df = pandas.read_table(data_path+'users.tsv', on_bad_lines='skip')
print('users.tsv size:', users_df.shape)
for (idx, user) in users_df.iterrows():

    top_jobs = top_city_jobs[int(user['WindowID'])][user['State']][user['City']]
    if len(top_jobs) < 150:
        top_jobs += top_state_jobs[int(user['WindowID'])][user['State']]
    top_jobs = top_jobs[0:150]

    popular_data.append([str(user['UserID']), ' '.join([x[0] for x in top_jobs])])

popular_df = pandas.DataFrame(data=popular_data, columns=['UserID', 'JobID'])
print('popular.csv size:', popular_df.shape)
popular_df.to_csv(data_path+'popular_jobs_full.csv', index=False)
