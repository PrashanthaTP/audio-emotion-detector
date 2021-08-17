import glob  
import os  
import librosa  
import numpy as np  

######from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.model_selection import train_test_split  
from sklearn.metrics import confusion_matrix  
import pandas as pd  
import seaborn as sns  
import matplotlib.pyplot as plt
import joblib.externals

from sklearn.metrics import accuracy_score 

#?-------------------Feature Extraction------------------------------------------

def extract_feature(file_name):
    
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
    sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz
#?-----------------------------------------------------------------------------------

def parse_audio_files(parent_dir,sub_dirs,file_ext="*.wav"):
    
    features, labels = np.empty((0,193)), np.empty(0)
    for label, sub_dir in enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            print(fn)
            try:
              mfccs, chroma, mel, contrast,tonnetz = extract_feature(fn)
            except Exception as e:
              print ("Error encountered while parsing file: ", fn)
              continue
            ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
            features = np.vstack([features,ext_features])
            print(fn.split('\\')[-1].split('-')[2])
            labels = np.append(labels, fn.split('\\')[-1].split('-')[2])
    return np.array(features), np.array(labels, dtype = np.int)

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels+1))
    one_hot_encode[np.arange(n_labels), labels] = 1
    one_hot_encode=np.delete(one_hot_encode, 0, axis=1)
    return one_hot_encode


# main_dir = os.path.join(main_dir,'Audio_Speech_Actors_01-24')
main_dir = "./Resources/dataset/"

sub_dir=os.listdir(main_dir)  

print ("\ncollecting features and labels...")  
print("\nthis will take some time...")  

features, labels = parse_audio_files(main_dir,sub_dir)  

print("Features extracted.....")  


#one hot encoding features
np.save('X',features)  
print('Saved x.npy.....')

#one hot encoding labels  
labels = one_hot_encode(labels)  
np.save('y', labels)
print('Saved y.npy.....')

X=np.load('X.npy')  
y=np.load('y.npy')



train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.33, random_state=42)
y_train = np.argmax(train_y, axis=1)
y_test = np.argmax(test_y, axis=1)
x_train =train_x
clf = svm.SVC(gamma= 'auto')
clf.fit(x_train,y_train)
# n_dim = train_x.shape[1]  
# n_classes = train_y.shape[1]  
# n_hidden_units_1 = n_dim  
# n_hidden_units_2 = 400 # approx n_dim * 2  
# n_hidden_units_3 = 200 # half of layer 2  
# n_hidden_units_4 = 100

# def create_model():
model_name = 'SVM_emotion_clf_24.pkl'
joblib.dump(clf,model_name)
print("Model saved as " + model_name)

predictions = clf.predict(test_x)

# print(accuracy_score(y_test,predictions))
  

# #create the model  
# model = create_model() 
# joblib.dump(model,'model_speech_emotion_detector') 
# print('Model saved,\n Aytala macha')
# #train the model  


# #predicting from the model  
# predict=model.predict(test_x)

# emotions=['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']  
# #predicted emotions from the test set  
# y_pred = np.argmax(predict, 1)  
# predicted_emo=[]   
# for i in range(0,test_y.shape[0]):  
#   emo=emotions[y_pred[i]]  
#   predicted_emo.append(emo)
  
# actual_emo=[]  
# y_true=np.argmax(test_y, 1)  
# for i in range(0,test_y.shape[0]):  
#   emo=emotions[y_true[i]]  
#   actual_emo.append(emo)

#! #generate the confusion matrix  
# cm =confusion_matrix(actual_emo, predicted_emo)  
# index = ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprised']  
# columns = ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprised']  
# cm_df = pd.DataFrame(cm,index,columns)                      
# plt.figure(figsize=(10,6))  

# sns.heatmap(cm_df, annot=True)  
# print(cm_df)
# plt.show()
