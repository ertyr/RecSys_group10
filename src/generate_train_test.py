
import pandas

full_ratings = pandas.read_csv('dataset/user_with_negative_ratings_full.csv')

full_ratings_1 = full_ratings.head(10000)
unique_users = full_ratings_1.drop_duplicates(['UserID'], keep='first').reset_index()
final_df = pandas.DataFrame(columns=full_ratings.columns.tolist())

for idx, user in unique_users.iterrows():
    temp_df = full_ratings[full_ratings['UserID']==user['UserID']][1:]
    final_df = pandas.concat([final_df, temp_df])

    if idx % 5000 == 0:
        print('Progress:', idx)

final_df.to_csv('dataset/user_with_negative_rating_train.csv')
unique_users.to_csv('dataset/user_with_negtive_rating_test.csv')