import random
import numpy as np
from xgboost import XGBClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits


def get_splits(n, k, seed):
    # splits = [i for i in range(n)]
    # random.seed(seed)
    # random.shuffle(splits)
    return [list(x) for x in np.array_split(np.arange(n), k)]


def my_cross_val(method, X, y, splits):
    errors = []

    if method == "LinearSVC":
        model = LinearSVC(max_iter=2000, random_state=412)
    elif method == "SVC":
        model = SVC(gamma='scale', C=10, random_state=412)
    elif method == "LogisticRegression":
        model = LogisticRegression(
            penalty='l2', solver='lbfgs', random_state=412, multi_class='multinomial')
    elif method == "RandomForestClassifier":
        model = RandomForestClassifier(
            max_depth=20, n_estimators=500, random_state=412)
    elif method == "XGBClassifier":
        model = XGBClassifier(max_depth=5, random_state=412)

    splits = [sorted(sublist) for sublist in splits]
    # print(splits)
    for i in range(len(splits)):
        train_indices = [ind for sublist in splits[:i] +
                         splits[i + 1:] for ind in sublist]
        test_indices = splits[i]

        train_indices.sort()

        train_X, train_Y = np.take(X, train_indices, axis=0), np.take(
            y, train_indices, axis=0)
        test_X, test_Y = np.take(X, test_indices, axis=0), np.take(
            y, test_indices, axis=0)
        # fit model
        model.fit(train_X, train_Y)
        # predict
        prediction = model.predict(test_X)

        assert len(prediction) == len(test_Y)
        # calculate error rate

        errors.append((np.array(prediction) != np.array(
            test_Y)).sum() / len(prediction))
    # Implement your code to calculate the errors here
    return np.array(errors)


if __name__ == "__main__":
    digits = load_digits()
    # print(digits.data.shape, digits.target.shape)
# [0.03888889 0.03333333 0.06145251 0.03888889 0.02777778 0.03888889
#  0.01117318 0.05027933 0.01666667 0.06111111]
#   # print(get_splits(10, 3, 1))
    n = len(digits.target)
    print(my_cross_val("LinearSVC", digits.data,
          digits.target, get_splits(n, 10, 1)))
