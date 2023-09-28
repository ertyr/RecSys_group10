import pandas

# TODO: More complex negative sampling technique
NEGATIVE_SAMPLE_NUM = 10  # Number of negative sampling to add to the rating dataset
NEGATIVE_SAMPLE_RATIO = 2.0  # Ratio determine number of negative sampling relative to positive sample in rating dataset

'''
Get the user id -> query popular_jobs -> extract JobId not exist in applied_jobs -> select top N include in rating dataset
1. Get unique user ID
2. For each user ID get a list of jobID it applied to
3. Loop through popular jobs of each user, find N jobs ID not contain in applied job list
4. Generate dataset with applied job list with value 1, and not applied job list value 0 
'''


def generate_rating_set(user_apps_df=None, popular_jobs_df=None, negative_sample_size=10):
    if user_apps_df is None:
        user_apps_df = pandas.read_table('../dataset/apps.tsv', on_bad_lines='skip')
    if popular_jobs_df is None:
        popular_jobs_df = pandas.read_csv('../dataset/popular_jobs.csv', on_bad_lines='skip')

    unique_users = user_apps_df.drop_duplicates(['UserID'])['UserID']
    ratings_df = pandas.DataFrame(columns=['UserID', 'JobID', 'Rating'])

    print('Total unique user:', unique_users.shape)
    for idx, user in zip(range(len(unique_users)),unique_users):
        applied_jobs = user_apps_df[user_apps_df['UserID'] == user]['JobID'].tolist()
        temp_df = pandas.DataFrame(data=applied_jobs, columns=['JobID'])
        temp_df['UserID'] = user
        temp_df['Rating'] = 1
        ratings_df = pandas.concat([ratings_df, temp_df])

        if not pandas.isna(popular_jobs_df[popular_jobs_df['UserID'] == user])['JobID'].values:

            un_applied_jobs = popular_jobs_df[popular_jobs_df['UserID'] == user]['JobID'].iloc[0].split(' ')
            ignored_jobs = [x for x in un_applied_jobs if x not in applied_jobs][:negative_sample_size]
            temp_df = pandas.DataFrame(data=ignored_jobs, columns=['JobID'])
            temp_df['UserID'] = user
            temp_df['Rating'] = 0
            ratings_df = pandas.concat([ratings_df, temp_df])

        if idx % 5000 == 0:
            print('Progress at index:', idx, 'size:', ratings_df.shape)

    print(ratings_df.shape)
    return ratings_df


if __name__ == '__main__':
    user_apps = pandas.read_table('../dataset/apps.tsv', on_bad_lines='skip')
    # user_apps_1 = user_apps[user_apps['WindowID'] == 1]
    generated_df = generate_rating_set(user_apps_df=user_apps, negative_sample_size=5)
    generated_df.to_csv('../dataset/user_with_negative_ratings_full.csv', index=False)
