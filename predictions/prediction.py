import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, RandomForestClassifier, VotingClassifier
from matplotlib import pyplot
from dataset_creation import read_data
from pandas.api.types import is_string_dtype
from sklearn.decomposition import PCA

#from dataset.dataset_methods import split_df_train_test
#from keras import layers, models, optimizers, losses, metrics

# Options for pandas -----
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Models' scores
accuracy = []
precision = []
recall = []
f1 = []

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
    #Drop name and reasons columns
    dataset.drop(['name', 'reasons'], axis='columns', inplace=True)
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
    return df;


def print_scores(y_true, y_pred):
    print("Accuracy: {:.5f}".format(metrics.accuracy_score(y_true, y_pred)))
    print("Precision: {:.5f}".format(metrics.precision_score(y_true, y_pred)))
    print("Recall: {:.5f}".format(metrics.recall_score(y_true, y_pred)))
    print("F1: {:.5f}".format(metrics.f1_score(y_true, y_pred)))
    accuracy.append(metrics.accuracy_score(y_true, y_pred))
    precision.append(metrics.precision_score(y_true, y_pred))
    recall.append(metrics.recall_score(y_true, y_pred))
    f1.append(metrics.f1_score(y_true, y_pred))

def fit_predict(x_train, x_test, model):
    model.fit(x_train)
    y_predicted = model.predict(x_test)
    return y_predicted

def make_prediction(dataset, prediction_type):

    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)


    # Scale all the data with MinMaxScaler
    # ---------------------------------------------------------------
    scaler = MinMaxScaler() #StandarScaler
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    if prediction_type == 'mongo_info':
        pca = PCA(.95)
        pca.fit(x_train)
        x_train = pca.transform(x_train)
        x_test = pca.transform(x_test)


    """
    # Naive Bayes
    # ---------------------------------------------------------------
    mnb = MultinomialNB().fit(x_train, y_train)

    #y_k_means_predicted = fit_predict(x_train, y_train, mnb)
    labels = mnb.predict(x_test)
    print("Results with MultinomialNB")
    print_scores(y_test, labels)
    print()
    """

    # Logistic Regression
    # ---------------------------------------------------------------
    lr = LogisticRegression(max_iter=1000)
    lr.fit(x_train, y_train)
    print("Results with Logistic Regression")
    labels = lr.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(lr.score(x_train, y_train)))
    print()
    # ---------------------------------------------------------------


    # K Neighbors Classifier
    # ---------------------------------------------------------------
    knn = KNeighborsClassifier(algorithm='brute', n_jobs=-1)
    knn.fit(x_train, y_train)
    print("Results with K Neighbors Classifier")
    labels = knn.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(knn.score(x_train, y_train)))
    print()
    # ---------------------------------------------------------------

    # Support Vector Machine
    # ---------------------------------------------------------------
    svm = LinearSVC(C=0.0001)
    svm.fit(x_train, y_train)
    print("Results with Support Vector Machine")
    labels = svm.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(svm.score(x_train, y_train)))
    print()
    # ---------------------------------------------------------------

    # Decision Tree Classifier
    # ---------------------------------------------------------------
    clf = DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    print("Results with Decision Tree Classifier")
    labels = clf.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(clf.score(x_train, y_train)))
    print(clf.feature_importances_)
    print()
    # ---------------------------------------------------------------

    # Bagging Decision Tree
    # ---------------------------------------------------------------
    # max_samples: maximum size 0.5=50% of each sample taken from the full dataset
    # max_features: maximum of features 1=100% taken here all 10K
    # n_estimators: number of decision trees
    bg = BaggingClassifier(DecisionTreeClassifier(), max_samples=0.5, max_features=1.0, n_estimators=10)
    bg.fit(x_train, y_train)
    print("Results with Bagging Decision Tree ")
    labels = bg.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(bg.score(x_train, y_train)))
    print()
    # ---------------------------------------------------------------


    # Boosting Decision Tree
    # ---------------------------------------------------------------
    adb = AdaBoostClassifier(DecisionTreeClassifier(min_samples_split=10, max_depth=4), n_estimators=10,
                             learning_rate=0.6)
    adb.fit(x_train, y_train)
    print("Results with Boosting Decision Tree ")
    labels = adb.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(adb.score(x_train, y_train)))
    print()
    # ---------------------------------------------------------------

    # Random Forest Classifier
    # ---------------------------------------------------------------
    # n_estimators = number of decision trees
    rf = RandomForestClassifier(n_estimators=30, max_depth=9)
    rf.fit(x_train, y_train)
    print("Results with Random Forest Classifier")
    labels = rf.predict(x_test)
    print_scores(y_test, labels)
    print("score on train: " + str(rf.score(x_train, y_train)))
    print()
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

    """
    # Voting Classifier
    # ---------------------------------------------------------------
    # 1) naive bias = mnb
    # 2) logistic regression =lr
    # 3) random forest =rf
    # 4) support vector machine = svm
    evc = VotingClassifier(estimators=[('mnb', mnb), ('lr', lr), ('rf', rf), ('svm', svm)], voting='hard')
    evc.fit(x_train, y_train)
    print("Results with Voting Classifier")
    print("score on test: " + str(evc.score(x_test, y_test)))
    print("score on train: " + str(evc.score(x_train, y_train)))
    print()
    # ---------------------------------------------------------------
    """


    """
    # Neural Network
    # ---------------------------------------------------------------
    # split an additional validation dataset
    x_validation = x_train[:1000]
    x_partial_train = x_train[1000:]
    y_validation = y_train[:1000]
    y_partial_train = y_train[1000:]
    model = models.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x_partial_train, y_partial_train, epochs=4, batch_size=512, validation_data=(x_validation, y_validation))
    print("score on test: " + str(model.evaluate(x_test, y_test)[1]))
    print("score on train: " + str(model.evaluate(x_train, y_train)[1]))
    # ---------------------------------------------------------------
    """

if __name__ == '__main__':

    #Make prediction on the questionnaire
    #dataset_quest = read_data_from_questionnaire()
    #make_prediction(dataset_quest,'questionnaire')

    # Make prediction on the crowtangle's info
    dataset_mongo = read_data.get_influencer_info()
    dataset_mongo_updated = preprocess_data_from_mongo(dataset_mongo)
    dataset_mongo_updated.to_csv('prediction_info.csv', index=False)
    make_prediction(dataset_mongo_updated, 'mongo_info')