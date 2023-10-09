import pandas

'''
Get the user id -> query popular_jobs -> extract JobId not exist in applied_jobs -> select top N include in rating dataset
1. Get unique user ID
2. For each user ID get a list of jobID it applied to
3. Loop through popular jobs of each user, find N jobs ID not contain in applied job list
4. Generate dataset with applied job list with value 1, and not applied job list value 0 
'''


def generate_rating_set(user_apps_df=None, popular_jobs_df=None, negative_num=10, negative_ratio=1.0, negative_value=0):
    if user_apps_df is None:
        user_apps_df = pandas.read_table('../dataset/apps.tsv', on_bad_lines='skip')
        print('Default user ratings:', user_apps_df.shape)
    if popular_jobs_df is None:
        popular_jobs_df = pandas.read_csv('../dataset/popular_jobs_full.csv', on_bad_lines='skip')
        print('Default popular jobs:', popular_jobs_df.shape)

    unique_users = user_apps_df.drop_duplicates(['UserID'])['UserID']
    ratings_df = pandas.DataFrame(columns=['UserID', 'JobID', 'Rating'])

    print('Total unique user:', unique_users.shape)
    for idx, user in zip(range(len(unique_users)), unique_users):
        applied_jobs = user_apps_df[user_apps_df['UserID'] == user]['JobID'].tolist()
        temp_df = pandas.DataFrame(data=applied_jobs, columns=['JobID'])
        temp_df['UserID'] = user
        temp_df['Rating'] = 1
        ratings_df = pandas.concat([ratings_df, temp_df])

        negative_sample_size = min(max(round(len(applied_jobs) * negative_ratio), negative_num), 50)

        if not pandas.isna(popular_jobs_df[popular_jobs_df['UserID'] == user]['JobID'].iloc[0]):

            un_applied_jobs = popular_jobs_df[popular_jobs_df['UserID'] == user]['JobID'].iloc[0].split(' ')
            ignored_jobs = [x for x in un_applied_jobs if x not in applied_jobs][:negative_sample_size]
            temp_df = pandas.DataFrame(data=ignored_jobs, columns=['JobID'])
            temp_df['UserID'] = user
            temp_df['Rating'] = negative_value
            ratings_df = pandas.concat([ratings_df, temp_df], ignore_index=True)

        if idx % 5000 == 0:
            print('Progress at index:', idx, 'size:', ratings_df.shape)

    print(ratings_df.shape)
    return ratings_df


if __name__ == '__main__':
    user_apps = pandas.read_table('../dataset/apps.tsv', on_bad_lines='skip')

    user_apps_1 = user_apps[user_apps['WindowID'] == 1]
    generated_df = generate_rating_set(user_apps_df=user_apps_1, negative_num=5)
    # generated_df.to_csv('../dataset/user_with_negative_ratings_full.csv', index=False)
