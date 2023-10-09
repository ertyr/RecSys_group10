import math
import pandas
from sklearn.model_selection import train_test_split

NEGATIVE_NUM = 5

MIN_APPLIED = 5
MIN_TEST_SIZE = 2

TEST_SIZE = 0.3


def generate_train_test_set_legacy(ratings_full):
    unique_user = ratings_full.drop_duplicates(['UserID']).reset_index(drop=True)

    ratings_train = pandas.DataFrame(columns=ratings_full.columns.tolist())
    ratings_test = pandas.DataFrame(columns=ratings_full.columns.tolist())

    print('Total unique users:', unique_user.shape[0])
    print('Total user ratings:', ratings_full.shape[0])
    for idx, user in unique_user.iterrows():
        rating_users = ratings_full[ratings_full['UserID'] == user['UserID']]

        if rating_users.shape[0] - NEGATIVE_NUM >= MIN_APPLIED:
            test_num = max(MIN_TEST_SIZE, math.floor((rating_users.shape[0] - NEGATIVE_NUM) * TEST_SIZE))

            temp_ratings_test = rating_users.iloc[:test_num]
            temp_ratings_train = rating_users.iloc[test_num + 1:]

            ratings_test = pandas.concat([ratings_test, temp_ratings_test])
            ratings_train = pandas.concat([ratings_train, temp_ratings_train])

        if idx % 5000 == 0:
            print('Progress at index: {:} or {:.4f} percent of total'.format(idx, idx / unique_user.shape[0]))

    print('User with minimum of {:} application:'.format(MIN_APPLIED),
          ratings_test.drop_duplicates(['UserID']).shape[0])
    print('Test size of {:} total ratings count:'.format(TEST_SIZE), ratings_test.shape[0])
    print('Train size total ratings count:', ratings_train.shape[0])

    return ratings_train, ratings_test


def generate_train_test_set(user_ratings_full, split_ratio=0.9, split_seed=1234, min_split_size=5):
    unique_user = user_ratings_full.drop_duplicates(['UserID']).reset_index(drop=True)

    ratings_train = pandas.DataFrame(columns=user_ratings_full.columns.tolist())
    ratings_test = pandas.DataFrame(columns=user_ratings_full.columns.tolist())

    print('Total unique users:', unique_user.shape[0])
    print('Total user ratings:', user_ratings_full.shape[0])
    for idx, user in unique_user.iterrows():

        rating_users = user_ratings_full[user_ratings_full['UserID'] == user['UserID']]

        if rating_users.shape[0] >= min_split_size:
            train_split, test_split = train_test_split(rating_users, train_size=split_ratio, random_state=split_seed)

            ratings_train = pandas.concat([ratings_train, train_split], axis=0, ignore_index=True)
            ratings_test = pandas.concat([ratings_test, test_split], axis=0, ignore_index=True)
        else:
            ratings_train = pandas.concat([ratings_train, rating_users], axis=0, ignore_index=True)

        if idx % 5000 == 0:
            print('Progress at index: {:} or {:.4f} percent of total'.format(idx, idx / unique_user.shape[0]))

    print('User count:', ratings_test.drop_duplicates(['UserID']).shape[0])
    print('Train size of {:} total ratings count:'.format(split_ratio), ratings_train.shape[0])
    print('Test size total ratings count:', ratings_test.shape[0])

    return ratings_train, ratings_test


if __name__ == '__main__':
    ratings_full = pandas.read_csv('./dataset/user_with_negative_ratings_full.csv')
    # ratings_full = ratings_full.iloc[:100000]

    ratings_train_df, ratings_test_df = generate_train_test_set_legacy(ratings_full)

    ratings_test_df.to_csv('./dataset/user_negative_ratings_test_full.csv', index=False)
    ratings_train_df.to_csv('./dataset/user_negative_ratings_train_full.csv', index=False)
