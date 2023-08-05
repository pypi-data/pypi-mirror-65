import pandas as pd
import numpy as np
from sklearn import preprocessing, utils
from sklearn.preprocessing import LabelEncoder

""" This File is made to hasten the process of loading, prepocessing and modifying the data
    , this will be part of a modular project to make life easier for those who use sklearn
    and its machine learning algorithms"""


class Data:

    def __init__(self, data, sep=','):
        self.data = data
        self.sep = sep
        self.DF = pd.read_csv(self.data, sep=self.sep)
        self.rows = (self.DF.shape[0] - 1)
        self.predict = None

    def put_predict(self, values):

        predict = {}
        for i in range(len(self.DF.columns)):
            predict[self.DF.columns[i]] = values[i]
        predict = pd.DataFrame(predict)
        self.DF = self.DF.append(predict)

    def get_list(self, drop):

        sort = self.DF[drop]
        sort = sort.sort_values()
        sort = sort.to_list()
        sort.pop(-1)
        sort = list(set(sort))

        return sort

    def codify(self):
        obj_data = self.DF.select_dtypes(include=["object"]).copy()
        obj_data_names = []
        for col in obj_data.columns:
            obj_data_names.append(col)

        for col_name in obj_data_names:
            self.DF[col_name] = self.DF[col_name].astype('category')
            self.DF[col_name + "_cat"] = self.DF[col_name].cat.codes
            self.DF[col_name] = self.DF[col_name + "_cat"]
            self.DF.drop(col_name + "_cat", 1, inplace=True)



    def get_predict(self):
        self.predict = pd.DataFrame(columns=self.DF.columns)
        linhas = self.DF.iloc[self.rows, :]
        self.predict = self.predict.append(linhas, ignore_index=True)
        self.DF.drop(self.rows, inplace=True)

    def pre_processing(self, drop, preprocessing_type='normalizer'):

        x = np.array(self.DF.drop([drop], 1))
        predictx = np.array(self.predict.drop([drop], 1))
        y = np.array(self.DF[drop])

        if preprocessing_type == 'normalizer':
            x = preprocessing.normalize(x)
            predictx = preprocessing.normalize(predictx)


        elif preprocessing_type == 'scale':
            x = preprocessing.scale(x)
            predictx = preprocessing.scale(predictx)

        lab_enc = preprocessing.LabelEncoder()
        y = lab_enc.fit_transform(y)

        return x, y, predictx
