import csv
import numpy as np
import pandas
import random
import math

def normalize_0_to_1(X=[]):
    min_x = X.min()
    span = X.max() - min_x
    return [((x - min_x)/span) for x in X]

class Dataset():
    def __init__(self, input, labels):
        self.X = input
        self.Y = labels
        self.N = len(np.unique(labels))

class Titanic():
    def __init__(self):
        self.name = "Titanic"
        self.pickle_name = 'tn'
        self.n_class = 2
        self.datafile = 'data/titanic.csv'
        self.train, self.test = self.load_data(self.datafile)
        self.main3_attrs=[0,1,2]
        self.main3_attr_labels=['PClass','Age','Sex']

    def load_data(self, fname):
        with open(fname) as f:
            data = csv.reader(f, delimiter=',')
            data = [row for row in data]

        random.seed=123
        data = data[1:len(data)]
        random.shuffle(data)
        tx = [map(float, x[1:len(x)-1]) for x in data]
        ty = [int(x[-1]) for x in data]

        train_size = int(math.ceil(len(data)*0.7))
        tr_tx = np.asarray(tx[0:train_size])
        tr_tx = np.asarray([normalize_0_to_1(x) for x in tr_tx.T]).T
        tr_ty = np.asarray(ty[0:train_size])
        ts_tx = np.asarray(tx[train_size:])
        ts_tx = np.asarray([normalize_0_to_1(x) for x in ts_tx.T]).T
        ts_ty = np.asarray(ty[train_size:])

        return Dataset(tr_tx, tr_ty), Dataset(ts_tx, ts_ty)

class Abalone():
    def __init__(self):
        self.name = "Abalone"
        self.pickle_name = 'al'
        self.n_class = 29
        self.datafile = 'data/abalone.csv'
        self.train, self.test = self.load_data(self.datafile)
        self.main3_attrs=[1,2,7]
        self.main3_attr_labels=['Length','Diameter','Shell weight']

    def load_data(self, fname):
        with open(fname) as f:
            data = csv.reader(f, delimiter=',')
            data = [row for row in data]

        data = data[1:len(data)]
        random.seed=123
        random.shuffle(data)
        tx = [map(float, x[1:len(x)-1]) for x in data]
        ty = [(int(x[-1])-1) for x in data]

        train_size = int(math.ceil(len(data)*0.7))
        tr_tx = np.asarray(tx[0:train_size])
        tr_tx = np.asarray([normalize_0_to_1(x) for x in tr_tx.T]).T
        tr_ty = np.asarray(ty[0:train_size])
        ts_tx = np.asarray(tx[train_size:])
        ts_tx = np.asarray([normalize_0_to_1(x) for x in ts_tx.T]).T
        ts_ty = np.asarray(ty[train_size:])

        return Dataset(tr_tx, tr_ty), Dataset(ts_tx, ts_ty)
