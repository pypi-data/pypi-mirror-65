import numpy as np
import sys
from thundergbm import TGBMClassifier
from sklearn import datasets as dts
from sklearn.model_selection import train_test_split

#Overall parameters
train_ratio=0.75
random_state=123457
limit=None
num_classes=10
num_estimators=1
num_parallel_trees=100
objective='multi:softmax'
max_depth=6

#number of GPU's
num_gpus=2


#Loads dataset digits
digits=dts.load_digits()
X=digits.data
y=digits.target

# Create 0.75/0.25 train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, \
        test_size=(1-train_ratio), \
        train_size=train_ratio, \
        random_state=random_state, \
        shuffle=True, \
        stratify=None)


#Classfier
clf = TGBMClassifier(objective=objective, \
        n_trees=num_estimators, \
        n_parallel_trees=num_parallel_trees, \
        n_gpus=num_gpus, \
        depth=max_depth,
        num_class=num_classes,
        tree_method='auto')
#Fitting
clf.fit(X_train, y_train)
#sys.exit(0)

#Predicting
y_pred = clf.predict(X_test)

#Score
print("Score: %10.5f"%(np.count_nonzero(np.equal(y_pred, y_test)) / y_test.shape[0]))
