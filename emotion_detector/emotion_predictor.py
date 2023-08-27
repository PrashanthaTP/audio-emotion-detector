import librosa  
import numpy as np  
import os
import joblib.externals

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#=========================================================================================
saved_model = 'SVM_emotion_clf_24.pkl'
main_dir = r'C:\Users\Prashanth T P\Desktop\DSP project\code\Audio_Speech_Actors_01-24'
DIR = r'E:\Users\VS_Code_Workspace\Python\Resources\Audio_Speech_Actors_01-24'   

audio = os.path.join(main_dir,'Actor_08','03-01-05-01-02-01-08.wav')
audio1 = os.path.join(main_dir,'Actor_05','03-01-06-02-02-02-05.wav')   
audio2 = os.path.join(DIR,'Actor_23','03-01-03-01-01-01-23.wav')

emotions=['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']  

#===========================================================================================
def extract_feature(file_name): 

    print('Extracting the features for the file ' + os.path.basename(file_name))

    X, sample_rate = librosa.load(file_name)

    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
                                              sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz

#=========================================================================================

def predict_emotion(model,x):
    clf = joblib.load(model)
    return(clf.predict(x))

#=========================================================================================

if __name__ == "__main__":

    print("Running "+ str(__file__) + "......")
#!HERE.............
    actual_emo = int(audio2.split('\\')[-1].split('-')[2])-1
    features = np.empty((0,193))

#!HERE.............
    mfccs,chroma,mel,contrast,tonnetz = extract_feature(audio2)

    ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
    features = np.vstack([features,ext_features])

    prediction = predict_emotion(saved_model,features)

    # pred  = np.argmax(prediction)
    # print(prediction)
    # print(pred)
    print('EMOTIONS :' + str(list(enumerate(emotions))))
    print('Predicted emotion \t Actual emotion ')
    print(str(emotions[prediction[0]]) + '\t\t\t ' + str(emotions[actual_emo]))

# else:
#     print('Eno aagide kana....')
#=========================================================================================
