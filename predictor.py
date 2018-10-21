# For inline plotting
import pandas
from pandas.tools.plotting import scatter_matrix

import matplotlib.pyplot as plt

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import numpy as np

url = "./fireData.csv"
names = ['month', 'temperature', 'wind', 'rain', 'city']

dataset = pandas.read_csv(url, names=names)


# Split out validation dataset

array = dataset.values

X = array[:,0:4]

Y = array[:,4]

validation_size = 0.20


seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, 
                                                                                Y, 
                                                                                test_size=validation_size, 
                                                                                random_state=seed)

seed = 7
scoring = 'accuracy'


models = []
models.append(('SVM', SVC()))

results = []
names = []

for name, model in models:
    #
    kfold = model_selection.KFold(n_splits=10, 
                                  random_state=seed)
    #
    cv_results = model_selection.cross_val_score(model, 
                                                 X_train, Y_train, 
                                                 cv=kfold, scoring=scoring)
    #
    results.append(cv_results)
    names.append(name)
    msg = "{0}: {1:f} ({2:f})".format(name, cv_results.mean(), cv_results.std())
    # print(msg)

svm = SVC()
svm.fit(X_train, Y_train)
predictions = svm.predict(X_validation)

print(X_validation)

print("Accuracy score:")
print(accuracy_score(Y_validation, predictions))
print()

print("confusion_matrix:")
print(confusion_matrix(Y_validation, predictions))
print()

print("classification_report:")
print(classification_report(Y_validation, predictions))
print()

print("________________________________")
# predictions2=svm.predict(np.array([[6, 23, 5.7, 0.0]]))
predictions2=svm.predict(X_train)
print(predictions2)