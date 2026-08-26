import cv2
import numpy as np
import face_recognition as fr
import os

path = r"C:\Users\au773\Documents\VS Code\FaceRecognition\knownfaces"
images =[]  #Images in the folder
img_names = []  #Nmaes of the People
titles = os.listdir(path) #Names of the images along with jpg

for cls in titles:
    curr_img = cv2.imread(f'{path}/{cls}') #Picks the current image in the lsit
    images.append(curr_img) #appends in the img_names list
    img_names.append(os.path.splitext(cls)[0]) #removes.jpg o any extension

def encodings(images):
    encodelist = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)

        if len(encode) > 0:
            encodelist.append(encode[0])
        else:
            print("No face found in image")

    return encodelist
list_encode = encodings(images)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    imgS = cv2.resize(frame,(0,0),None,fx=0.25,fy=0.25)  #just for speeding the process
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    frame_loc = fr.face_locations(imgS)
    frame_encodings = fr.face_encodings(imgS,frame_loc)

    for encoding, loc in zip(frame_encodings,frame_loc):
        matches = fr.compare_faces(list_encode,encoding)
        face_dis = fr.face_distance(list_encode,encoding)
        match_index = np.argmin(face_dis)

        if matches[match_index]: 
            name = img_names[match_index].upper()
            y1,x2,y2,x1 = loc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(frame,(x1,y2+30),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        else:
            name = "Unknown"
            y1,x2,y2,x1 = loc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(frame,(x1,y2+30),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow("Webcam",frame)
    cv2.waitKey(1)    
   
   
