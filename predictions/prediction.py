import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, RandomForestClassifier, VotingClassifier
from matplotlib import pyplot
from dataset_creation import read_data
from pandas.api.types import is_string_dtype
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import os.path


# Options for pandas -----
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

accuracy = []
precision = []
recall = []
f1 = []
model_names = []

def read_data_from_questionnaire():
    # reads data/category_columns_dataset.csv
    dataset = pd.read_csv("final_questionnaire.csv",
                          sep=',',
                          header=0,
                          skiprows=0)
    print('Dataset size is: ', len(dataset))
    print(dataset.head(5))

    #Convert "Ναι / Οχι" responses in 0-1
    dataset['follow'] = dataset['follow'].apply(lambda x: 0 if x=='Όχι' else 1)

    # Convert "Άντρας / Γυναίκα" responses in m-f
    dataset['gender'] = dataset['gender'].apply(lambda x: 0 if x == 'Άντρας' else 1)
    print(dataset.head(5))

    print(dataset.columns)
    #Drop name, reasons & category columns
    dataset.drop(['name', 'reasons', 'category'], axis='columns', inplace=True)
    print(dataset.shape)

    #Convert all string values to numeric
    for x in dataset.columns:
        dataset[x] = pd.to_numeric(dataset[x], errors='coerce')

    # Drop rows with age <0 and >100
    dataset.drop(dataset[dataset['age'] < 0].index, inplace=True)
    dataset.drop(dataset[dataset['age'] > 100].index, inplace=True)
    print(dataset.shape)

    # Drop examples (if any) that may contain NaN features
    # ---------------------------------------------------------------
    dataset.dropna(inplace=True)
    print(dataset.shape)

    #dataset.drop(['age'])
    return dataset;


def preprocess_data_from_mongo(df):

    for i in df.columns:
        if is_string_dtype(df[i]):
            df[i] = df[i].map(lambda x: str(x).replace('%',''))
            df[i] = df[i].map(lambda x: str(x).replace('--', '0'))
            df[i] = df[i].map(lambda x: str(x).replace(',', ''))

            # Convert all string values to numeric, except the category column
            if i != 'category':
                df[i] = pd.to_numeric(df[i], errors='coerce')

    # Convert continuous follow_probability to 0-1
    df['follow_probability'] = df['follow_probability'].apply(lambda x: 1 if x >= 0.5 else 0)

    # Drop examples (if any) that may contain NaN features
    # ---------------------------------------------------------------
    df.dropna(inplace=True)
    #print(df.shape)
    #print(df.head(5))
    return df


def print_scores(y_true, y_pred, model_name):
    print("Results with ",model_name)
    print("Accuracy: {:.5f}".format(metrics.accuracy_score(y_true, y_pred)))
    print("Precision: {:.5f}".format(metrics.precision_score(y_true, y_pred)))
    print("Recall: {:.5f}".format(metrics.recall_score(y_true, y_pred)))
    print("F1: {:.5f}".format(metrics.f1_score(y_true, y_pred)))
    accuracy.append(metrics.accuracy_score(y_true, y_pred))
    precision.append(metrics.precision_score(y_true, y_pred))
    recall.append(metrics.recall_score(y_true, y_pred))
    f1.append(metrics.f1_score(y_true, y_pred))
    model_names.append(model_name)

def plot_results(name):

    x = np.arange(len(model_names))
    width = 0.2  # the width of the bars
    X_axis = np.arange(len(model_names))

    plt.bar(X_axis - 0.3, accuracy, width, label='Accuracy', color='red')
    plt.bar(X_axis - 0.1, precision, width, label='Precision', color='purple')
    plt.bar(X_axis + 0.1, recall, width, label='Recall')
    plt.bar(X_axis + 0.3, f1, width, label='F1')

    plt.xticks(X_axis, model_names, rotation=45)
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.25)
    plt.xlabel("Models")
    plt.ylabel("Scores")
    plt.title("Machine Learning Model Scores")
    plt.legend()
    plt.savefig(name + '.png')
    plt.show()


def fit_predict(x_train, x_test, model):
    model.fit(x_train)
    y_predicted = model.predict(x_test)
    return y_predicted


def make_prediction(dataset, prediction_type):

    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=2)


    # Scale all the data with MinMaxScaler
    # ---------------------------------------------------------------
    scaler = MinMaxScaler()
    x_train_s = scaler.fit_transform(x_train)
    x_test_s = scaler.transform(x_test)

    if prediction_type == 'mongo_info':
        pca = PCA(0.95)
        pca.fit(x_train_s)
        x_train_final = pca.transform(x_train_s)
        x_test_final = pca.transform(x_test_s)
    else:
        x_train_final = x_train_s
        x_test_final = x_test_s


    if prediction_type == 'questionnaire_info':
        # Naive Bayes
        # ---------------------------------------------------------------
        mnb = MultinomialNB().fit(x_train, y_train)
        y_predicted = mnb.predict(x_test_final)
        print_scores(y_test, y_predicted, "MultinomialNB")
        print("score on train: ", str(mnb.score(x_train_final, y_train)), "\n")
        # ---------------------------------------------------------------


    # Logistic Regression
    # ---------------------------------------------------------------
    grid = {"C": np.logspace(-3, 3, 7), "tol": [1e-2, 1e-3, 1e-4, 1e-5], "penalty": ["l1", "l2"], "solver": ["saga"], "max_iter": [5000]}
    lr = GridSearchCV(LogisticRegression(), param_grid=grid)
    lr.fit(x_train_final, y_train)
    y_predicted = lr.predict(x_test_final)
    print_scores(y_test, y_predicted, "Logistic Regression")
    print("score on train: ", str(lr.score(x_train_final, y_train)), "\n")
    # ---------------------------------------------------------------


    # K Neighbors Classifier
    # ---------------------------------------------------------------
    knn = KNeighborsClassifier(algorithm='brute', n_jobs=-1)
    knn.fit(x_train_final, y_train)
    y_predicted = knn.predict(x_test_final)
    print_scores(y_test, y_predicted, "K Neighbors Classifier")
    print("score on train: ", str(knn.score(x_train_final, y_train)), "\n")
    # ---------------------------------------------------------------

    # Support Vector Machine
    # ---------------------------------------------------------------
    param_grid = {'C': [0.1, 1, 10, 100, 1000],
                  'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                  'kernel': ['rbf']}
    svm = GridSearchCV(SVC(), param_grid)
    svm.fit(x_train_final, y_train)
    y_predicted = svm.predict(x_test_final)
    print_scores(y_test, y_predicted, "Support Vector Machine")
    print("score on train: " + str(svm.score(x_train_final, y_train)), "\n")
    # ---------------------------------------------------------------

    # Decision Tree Classifier
    # ---------------------------------------------------------------
    clf = DecisionTreeClassifier()
    clf.fit(x_train_final, y_train)
    y_predicted = clf.predict(x_test_final)
    print_scores(y_test, y_predicted, "Decision Tree Classifier")
    print("score on train: " + str(clf.score(x_train_final, y_train)), "\n")
    print(clf.feature_importances_)
    # ---------------------------------------------------------------

    # Bagging Decision Tree
    # ---------------------------------------------------------------
    # max_samples: maximum size 0.5=50% of each sample taken from the full dataset
    # max_features: maximum of features 1=100% taken here all 10K
    # n_estimators: number of decision trees
    bg = BaggingClassifier(DecisionTreeClassifier(), max_samples=0.5, max_features=1.0, n_estimators=10)
    bg.fit(x_train_final, y_train)
    y_predicted = bg.predict(x_test_final)
    print_scores(y_test, y_predicted, "Bagging Decision Tree")
    print("score on train: " + str(bg.score(x_train_final, y_train)), "\n")
    # ---------------------------------------------------------------


    # Boosting Decision Tree
    # ---------------------------------------------------------------
    adb = AdaBoostClassifier(DecisionTreeClassifier(min_samples_split=10, max_depth=4), n_estimators=10,
                             learning_rate=0.6)
    adb.fit(x_train_final, y_train)
    y_predicted = adb.predict(x_test_final)
    print_scores(y_test, y_predicted, "Boosting Decision Tree")
    print("score on train: " + str(adb.score(x_train_final, y_train)), "\n")
    # ---------------------------------------------------------------

    # Random Forest Classifier
    # ---------------------------------------------------------------
    # n_estimators = number of decision trees
    rf = RandomForestClassifier(n_estimators=30, max_depth=9)
    rf.fit(x_train_final, y_train)

    y_predicted = rf.predict(x_test_final)
    print_scores(y_test, y_predicted, "Random Forest Classifier")
    print("score on train: " + str(rf.score(x_train_final, y_train)), "\n")
    # perform Random Forest Build-in importance
    importance = rf.feature_importances_
    # summarize feature importance
    importanceDict = {}
    listImp = []
    print('Random Forest Build-in importance')
    for i, v in enumerate(importance):
        print('Feature: %0d, Score: %.5f' % (i, v))
        listImp.append(v)
        importanceDict[v] = i
    print()
    # plot feature importance
    pyplot.bar([x for x in range(len(importance))], importance)
    pyplot.show()
    # ---------------------------------------------------------------

    if prediction_type == 'questionnaire_info':
        # Voting Classifier
        # ---------------------------------------------------------------
        # 1) naive bias = mnb
        # 2) logistic regression =lr
        # 3) random forest =rf
        # 4) support vector machine = svm
        evc = VotingClassifier(estimators=[('mnb', mnb), ('lr', lr), ('rf', rf), ('svm', svm)], voting='hard')
        evc.fit(x_train_final, y_train)
        y_predicted = evc.predict(x_test_final)
        print_scores(y_test, y_predicted, "Voting Classifier")
        print("score on train: " + str(evc.score(x_train_final, y_train)), "\n")
        # ---------------------------------------------------------------


if __name__ == '__main__':

    #Make prediction on the questionnaire
    print("Machine learning methods: Questionnaire")
    dataset_quest = read_data_from_questionnaire()
    make_prediction(dataset_quest,'questionnaire_info')
    plot_results("questionnaire")

    accuracy = []
    precision = []
    recall = []
    f1 = []
    model_names = []

    # Make prediction on the crowdtangle's info
    print("Machine learning methods: Crowdtangle")
    if os.path.isfile('prediction_info.csv'):
        dataset_mongo_updated = pd.read_csv("prediction_info.csv")
        pass
    elif os.path.isfile('questionnaire.csv'):
        dataset_mongo = read_data.get_influencer_info()
        dataset_mongo_updated = preprocess_data_from_mongo(dataset_mongo)
        dataset_mongo_updated.to_csv('prediction_info.csv', index=False)

    make_prediction(dataset_mongo_updated, 'mongo_info')
    plot_results("crowdtangle")
    

