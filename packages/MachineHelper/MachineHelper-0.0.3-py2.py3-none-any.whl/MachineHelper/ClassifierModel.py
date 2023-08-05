from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

""" This file is made to hasten the process of creating and adjusting your machine learning model, 
    this will be part of a modular project to make life easier for those who use sklearn
    and its machine learning algorithms"""


class Model:

    def __init__(self, x, y, predict, test_size, lista):
        self.x = x
        self.y = y
        self.lista = lista
        self.predict = predict
        self.test_size = test_size

        self.x_train, self.x_test, self.y_train, self.y_test = \
            train_test_split(self.x, self.y, test_size=self.test_size)

    def linear_regression(self, visual=0):

        linear = linear_model.LinearRegression()
        linear.fit(self.x_train, self.y_train)

        acc = linear.score(self.x_test, self.y_test)
        predict = linear.predict(self.predict)
        predict = int(round(predict[0]))
        predict = self.lista[predict]
        if visual == 1:
            predictions = linear.predict(self.x_test)
            for i in range(len(predictions)):
                print(f"Esperado: {self.y_test[i]} Obtido: {round(predictions[i])}")

        return acc, predict

    def knn(self, k=3, weight='uniform', visual=0):

        knn = KNeighborsClassifier(n_neighbors=k, weights=weight)
        knn.fit(self.x_train, self.y_train)

        acc = knn.score(self.x_test, self.y_test)
        predict = knn.predict(self.predict)
        predict = int(predict[0])
        predict = self.lista[predict]

        if visual == 1:
            predictions = knn.predict(self.x_test)
            for i in range(len(predictions)):
                print(f"Esperado: {self.y_test[i]} Obtido: {predictions[i]}")
        return acc, predict

    def svm(self, kernel='rbf', degree=3, gamma='scale', visual=0):

        svm = SVC(kernel=kernel, degree=degree, gamma=gamma)
        svm.fit(self.x_train, self.y_train)

        acc = svm.score(self.x_test, self.y_test)
        predict = svm.predict(self.predict)
        predict = int(predict[0])
        predict = self.lista[predict]

        if visual == 1:
            predictions = svm.predict(self.x_test)
            for i in range(len(predictions)):
                print(f"Esperado: {self.y_test[i]} Obtido: {predictions[i]}")

        return acc, predict

    def decision_tree(self, criterion='gini', splitter='best', visual=0):

        dtc = DecisionTreeClassifier(criterion=criterion, splitter=splitter)
        dtc.fit(self.x_train, self.y_train)

        acc = dtc.score(self.x_test, self.y_test)
        predict = dtc.predict(self.predict)
        predict = int(predict[0])
        predict = self.lista[predict]

        if visual == 1:
            predictions = dtc.predict(self.x_test)
            for i in range(len(predictions)):
                print(f"Esperado: {self.y_test[i]} Obtido: {predictions[i]}")

        return acc, predict
