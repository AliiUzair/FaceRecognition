import cv2
import numpy as np
import face_recognition as fr
import os
import pickle

path = r"C:\Users\au773\Documents\VS Code\FaceRecognition\knownfaces"
titles = os.listdir(path) #Names of the images along with jpg

# Load existing file if it exists, otherwise start with empty lists
if os.path.exists("trained_faces.pkl"):
    with open("trained_faces.pkl", "rb") as f:
        list_encode, img_names = pickle.load(f)
else:
    list_encode = []
    img_names = []

# Change 3: Look through your folder but only process brand new images
updated = False
for cls in titles:
    name = os.path.splitext(cls)[0]  # Kept exactly [0] indexing for clean names
    if name not in img_names:       # Skip if name is already inside the saved list
        curr_img = cv2.imread(f'{path}/{cls}') 
        img_rgb = cv2.cvtColor(curr_img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img_rgb)
        if len(encode) > 0:
            list_encode.append(encode[0])
            img_names.append(name)
            updated = True

#Save the list to your hard drive if a new image was added
if updated:
    with open("trained_faces.pkl", "wb") as f:
        pickle.dump([list_encode, img_names], f)

cap = cv2.VideoCapture(0)
process_this_frame = True
while True:
    if process_this_frame:
        success, frame = cap.read()
        imgS = cv2.resize(frame,(0,0),None,fx=0.25,fy=0.25)  #just for speeding the process
        imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        frame_loc = fr.face_locations(imgS)
        frame_encodings = fr.face_encodings(imgS,frame_loc)
    process_this_frame = not process_this_frame

    for encoding, loc in zip(frame_encodings,frame_loc):
        matches = fr.compare_faces(list_encode,encoding)
        face_dis = fr.face_distance(list_encode,encoding)
        match_index = np.argmin(face_dis)

        y1,x2,y2,x1 = loc
        y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

        if matches[match_index]: 
            name = img_names[match_index].upper()
            
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(frame,(x1,y2+30),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        else:
            name = "Unknown"
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(frame,(x1,y2+30),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow("Webcam",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  
   
   
