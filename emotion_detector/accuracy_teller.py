import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib.externals

CUR_DIR = os.getcwd()
model_name = 'SVM_emotion_clf_24.pkl'
features = 'Features_emotions_24.npy'
labels = 'labels_emotions_24.npy'


def load_model():
    return joblib.load(os.path.join(CUR_DIR,model_name))

def fPrediction(clf,train_x,test_x,train_y,test_y):
       prediction = clf.predict(train_x)
       print("Accuracy score of EMOTION DETECTOR is : " +str(accuracy_score(train_y,prediction)))

def print_shape(*args):
    for each in args:
        print("Shape "  + str(each.shape))

if __name__ == '__main__':
    x = np.load(features)
    y = np.load(labels)
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.9, random_state=42)

    train_y = np.argmax(train_y, axis=1)
    test_y = np.argmax(test_y, axis=1)

 
    clf = load_model()
    fPrediction(clf,train_x,test_x,train_y,test_y)
