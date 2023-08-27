# Dev

## Issues due to mismatched package versions

```bash
 .../SemesterWise/Sem4/DSP project/emotion_detector ::  master (19b381c)
$ python gui.py
pygame 1.9.5
Hello from the pygame community. https://www.pygame.org/contribute.html
D:/dataset_lip/Audio_Speech_Actors_01-24/Actor_02/03-01-01-01-01-02-02.wav
D:/dataset_lip/Audio_Speech_Actors_01-24/Actor_02/03-01-02-01-01-01-02.wav
D:/dataset_lip/Audio_Speech_Actors_01-24/Actor_01/03-01-01-01-01-01-01.wav
Extracting the features for the file 03-01-03-01-01-01-23.wav.......
E:\Programs\Python\lib\site-packages\scipy\sparse\lil.py:514: FutureWarning: future versions will not create a writeable array from broadcast_array. Set the writable flag explicitly to avoid this warning.
  if not j.flags.writeable or j.dtype not in (np.int32, np.int64):
E:\Programs\Python\lib\site-packages\sklearn\utils\deprecation.py:143: FutureWarning: The sklearn.svm.classes module is  deprecated in version 0.22 and will be removed in version 0.24. The corresponding classes / functions should instead be imported from sklearn.svm. Anything that cannot be imported from sklearn.svm is now part of the private API.
  warnings.warn(message, FutureWarning)
E:\Programs\Python\lib\site-packages\sklearn\base.py:334: UserWarning: Trying to unpickle estimator SVC from version 0.21.3 when using version 0.23.2. This might lead to breaking code or invalid results. Use at your own risk.
  UserWarning)
Cannot extract features.. 'SVC' object has no attribute 'break_ties'
D:/dataset_lip/Audio_Speech_Actors_01-24/Actor_01/03-01-01-01-01-01-01.wav
Extracting the features for the file 03-01-03-01-01-01-23.wav.......
Cannot extract features.. 'SVC' object has no attribute 'break_ties'
```
