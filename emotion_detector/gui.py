import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import os
from pygame import mixer

import numpy as np
from emotion_predictor import emotions,extract_feature,saved_model,predict_emotion



mixer.init()

DIR  = os.getcwd()
#SONGS_DIR = r'C:\Users\Prashanth T P\Desktop\DSP project\code\Audio_Speech_Actors_01-24\Actor_07'
#song = os.path.join(SONGS_DIR,'03-01-05-02-02-02-07.wav')
song = r'C:/Users/Prashanth T P/Desktop/DSP project/code/Audio_Speech_Actors_01-24\Actor_07/03-01-05-02-02-02-07.wav'
audio_files_path = os.path.join(DIR,'Audio_Speech_Actors_1-24')
INITIAL_DIR  = r'C:/Users/Prashanth T P/Desktop/DSP project/code/Test_set'
DATASET_INFO_DIR = r'C:/Users/Prashanth T P/Desktop/DSP project/data_set_info.txt'

imgPath = r'Resources/icon1.png'
iconPath = r'Resources/icon2.ico'
playButton_path = r'Resources/play_button.png'
stopButton_path = r'Resources/stop_button.png'

file_name = ''
default_vol = 0.7


def create_window():
    global root
    global name

    root = tk.Tk()
    root.title('Emotion Detector')
    root.iconbitmap(iconPath)
    root.geometry('500x350')
    root.minsize(480,350)
    root.maxsize(480,380)
   
    
    name = tk.StringVar()  
    create_menu_bar()

    return root

def create_menu_bar():
    menubar = tk.Menu(root)
    root.config(menu = menubar) # top position

    # sub_menu = tk.Menu(menubar,tearoff = 0)
    menubar.add_cascade(label = 'Select Files',command = select_file)
    menubar.add_cascade(label  = 'About',command = about_us )
    menubar.add_cascade(label = 'Datset Info',command = new_window)
    
    menubar.add_cascade(label = 'Exit',command = root.quit)


def about_us():
    info  = "Created by \n#Prashantha T P\n#Chetan A H\n#Darshan V"
    msg_box = tk.messagebox.showinfo('Emotion Detector',info)
   
    
def new_window():
    # global info_txt,info_root
    # info_txt = open(DATASET_INFO_DIR,'r')
    # info  = info_txt.readlines()
    info1 = "The RAVDESS dataset contains 7356 files\n. Each file was rated 10 times on emotional validity, intensity, and genuineness.\n \
             Ratings were provided by 247 individuals who were characteristic of untrained adult research participants from North America.\n \
             A further set of 72 participants provided test-retest data. High levels of emotional validity, interrater reliability, and \n\
                 test-retest intrarater reliability were reported.\n ."
    info2 = "File naming convention\n  Each of the 7356 RAVDESS files has a unique filename\n. \
            The filename consists of a 7-part numerical identifier \n (e.g., 02-01-06-01-02-01-12.mp4).\
              These identifiers define the stimulus characteristics:\n \
             Filename identifiers \n \
	Modality (01 = full-AV, 02 = video-only, 03 = audio-only).\n \
	Vocal channel (01 = speech, 02 = song).\n \
	Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.\n \
	Statement (01 = 'Kids are talking by the door', 02 = 'Dogs are sitting by the door').\n \
	Repetition (01 = 1st repetition, 02 = 2nd repetition).\n \
	Actor (01 to 24. Odd numbered actors are male, even numbered actors are female)."
    info3 = """\n
    Livingstone SR, Russo FA (2018) The Ryerson Audio-Visual Database of Emotional
    Speech and Song (RAVDESS): A dynamic, multimodal set of facial and vocal
    expressions in North American English. PLoS ONE 13(5): e0196391.
    https://doi.org/10.1371/journal.pone.0196391.
    """
    info4 =  "\nZenodo page - https://zenodo.org/record/1188976"

    info_root = tk.Toplevel(root)
    info_root.geometry('750x400')
    info_text = tk.Label(info_root,text = info1+info2+info3+info4).pack()

    # info_root.protocol('WM_WINDOW_DELETE',on_closing)
# def on_closing():
#     global info_txt,info_root
#     info_txt.close()
#     info_root.destroy()

def select_file():
   
    global file_name
    global pred_variable,actual_variable
  
    file_name = filedialog.askopenfilename(initialdir  = INITIAL_DIR,
                                            title = 'Select a audio file',
                                            filetypes = (("all files","*.*"),("wave files",".wav"),("mp3 files",".mp3")))
    
    print("file name : " ,file_name)

    #name.set("Audio file name : " + file_name.split('/')[-1])
    
    status_bar['text'] = ("Selected audio file name : " + os.path.basename(file_name))
    pred_variable.set('.....')
    actual_variable.set('.....')


def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

def play_music():
    global file_name,status_bar
   
    if file_name=='':
        file_name = song 
    try:
        mixer.music.load(file_name)
        mixer.music.play()
    except:
        error_msg = tk.messagebox.showerror('ERROR!!!','Cannot load the selected file!!!')
    
    #name.set("Audio file name : " + file_name.split('/')[-1])
    status_bar['text'] = ("Selected audio file name : " + file_name.split('/')[-1])
 

def stop_music():
    mixer.music.stop()



def create_widgets():
    global name 
    global pred_variable,actual_variable

    # text_frame = tk.Frame(root).pack()
    # middle_frame = tk.Frame(root)
    # middle_frame.pack(padx =  10, pady = 10)
    # volume_frame = tk.Frame(root).pack()
    # predict_frame = tk.Frame(root).pack()

    main_text = tk.Label(root,text = "Let's detect some emotion!!!\n").pack(pady = 10)

    emotion_list_text = tk.Label(root,text="Emotions :" + str(emotions)).pack()
    # select_file_btn = tk.Button(root,text = 'Select a file',command = lambda:select_file(name))
    # select_file_btn.pack()

    #text = tk.Label(root,textvariable = name).pack()
    
    play_button_img = tk.PhotoImage(file = playButton_path )
    stop_button_img = tk.PhotoImage(file = stopButton_path)

    middle_frame = tk.Frame(root)
    middle_frame.pack(padx =  10, pady = 10)  
    play_btn = tk.Button(middle_frame,image = play_button_img, relief = 'raised',borderwidth = 5,command = play_music).pack(side='left' ,padx = 5)
    stop_btn = tk.Button(middle_frame,image = stop_button_img,relief = 'raised',borderwidth = 5,command = stop_music).pack(side='left' ,padx = 5)
    
    volume_frame = tk.Frame(root).pack()
    vol_text = tk.Label(volume_frame,text="Volume")
    vol_text.pack(pady = 5)
    scale = tk.Scale(volume_frame,from_ = 0, to = 100, orient = 'horizontal',command = set_vol)
    scale.set(default_vol*100)
    mixer.music.set_volume(default_vol)
    scale.pack(fill = 'x')

    predict_btn = tk.Button(root,text = 'Predict',relief = 'solid' ,borderwidth = 2,command = make_prediction)
    predict_btn.pack(pady = 5)

    pred_variable = tk.StringVar()
    prediction_text = tk.Label(root,textvariable  = pred_variable).pack()
    actual_variable = tk.StringVar()
    actual_text = tk.Label(root,textvariable  = actual_variable).pack()
    
    global status_bar
    status_bar = tk.Label(root,text="Welcome to Emotion Detector Application!!!",relief = 'raised',borderwidth = 5)
    status_bar.pack(side = 'bottom', fill = 'x')

    root.mainloop()

def make_prediction(isKnown=1):
    global file_name
    global prediction
    global pred_variable,actual_variable,status_bar
   
  
    features = np.empty((0,193))
    try:
        mfccs,chroma,mel,contrast,tonnetz = extract_feature(file_name)
   
        ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
        features = np.vstack([features,ext_features])

        prediction = predict_emotion(saved_model,features)
        pred_variable.set("Predicted Emotion : " + str(emotions[prediction[0]]))
        
        print('EMOTIONS :' + str((emotions)))
        print('Predicted emotion :' + str(emotions[prediction[0]]))
        
        if isKnown==1:
            actual_emo = int(file_name.split('/')[-1].split('-')[2])-1
        
            print("Actual Emotion :" + str(emotions[actual_emo]))
            actual_variable.set("Actual Emotion   :"+ str(emotions[actual_emo]))

    except Exception as e:
        print('Cannot extract features..',e)
        status_bar['text'] = "Select a valid file..."

if __name__=='__main__':
    print("Welcome !")
    root = create_window()
    create_widgets()



