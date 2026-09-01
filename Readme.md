# Face Recognition System

This is a simple **Face Recognition project in Python** that uses a webcam to detect and recognize known faces. I made this project to learn how face recognition works using Python, OpenCV, and the `face_recognition` library.

The program takes images from a folder of known faces, creates face encodings for them, and saves those encodings in a `.pkl` file. After that, it opens the webcam and tries to recognize the faces that appear in front of the camera.

## Features

* Detects faces using a webcam.
* Recognizes faces that are already stored in the `knownfaces` folder.
* Shows the person's name when a face is recognized.
* Shows **"Unknown"** when the face doesn't match any known person.
* Saves face encodings in a `trained_faces.pkl` file.
* Doesn't process the same image again if it has already been added.
* Uses a smaller version of the webcam frame to make face recognition faster.
* Press **Q** to close the webcam window.

## Technologies Used

The project is made using:

* **Python**
* **OpenCV (`cv2`)** – for accessing the webcam and displaying the video.
* **face_recognition** – for detecting faces and generating face encodings.
* **NumPy** – for comparing face distances.
* **Pickle** – for saving and loading the trained face encodings.
* **OS** – for reading the images from the known faces folder.

## Project Structure

The project can be organized like this:

```text
FaceRecognition/
│
├── knownfaces/
│   ├── ali.jpg
│   ├── ahmed.jpg
│   └── sara.jpg
│
├── main.py
└── trained_faces.pkl
```

The `knownfaces` folder contains the images of people that I want the program to recognize.

For example:

```text
knownfaces/
├── ali.jpg
├── ahmed.jpg
└── sara.jpg
```

The file name is used as the person's name. So, if the image is called `ali.jpg`, the program will display **ALI** when that person is recognized.

## How It Works

### 1. Load Known Faces

First, the program checks the `knownfaces` folder and gets the names of all the image files.

```python
titles = os.listdir(path)
```

It removes the file extension from each image name:

```python
name = os.path.splitext(cls)[0]
```

So:

```text
ali.jpg → ali
```

### 2. Create Face Encodings

The program reads each image and converts it from BGR to RGB because the `face_recognition` library works with RGB images.

```python
curr_img = cv2.imread(f'{path}/{cls}')
img_rgb = cv2.cvtColor(curr_img, cv2.COLOR_BGR2RGB)
encode = fr.face_encodings(img_rgb)
```

If a face is found, its encoding is stored in a list.

A face encoding is basically a numerical representation of a person's face that can be compared with other faces.

### 3. Save the Encodings

Instead of creating the encodings every time the program starts, I save them in:

```text
trained_faces.pkl
```

The program checks if this file already exists:

```python
if os.path.exists("trained_faces.pkl"):
```

If it exists, the saved encodings and names are loaded.

If a new person is added to the `knownfaces` folder, the program creates an encoding for that image and updates the `.pkl` file.

This makes the program faster because it doesn't need to process all the old images again.

## 4. Start the Webcam

After loading the known faces, the program starts the computer's webcam:

```python
cap = cv2.VideoCapture(0)
```

The webcam continuously captures frames and looks for faces.

## 5. Speed Optimization

To make the face recognition process faster, the webcam frame is resized to 25% of its original size:

```python
imgS = cv2.resize(frame,(0,0),None,fx=0.25,fy=0.25)
```

The face detection is done on this smaller image instead of the full-size frame.

The coordinates are then multiplied by 4 when drawing the rectangle on the original frame.

## 6. Recognizing Faces

The program gets the face encodings from the webcam frame and compares them with the known face encodings:

```python
matches = fr.compare_faces(list_encode,encoding)
face_dis = fr.face_distance(list_encode,encoding)
```

The closest matching face is found using:

```python
match_index = np.argmin(face_dis)
```

If the face matches a known person, their name is displayed in a **green box**.

If there is no match, the program displays **Unknown** in a **red box**.

## Example

If the `knownfaces` folder contains:

```text
knownfaces/
├── ali.jpg
├── ahmed.jpg
```

and Ali stands in front of the webcam, the program will show something like:

```text
┌──────────────────┐
│                  │
│       FACE       │
│                  │
└──────────────────┘
       ALI
```

If someone who isn't in the folder appears:

```text
┌──────────────────┐
│                  │
│       FACE       │
│                  │
└──────────────────┘
     UNKNOWN
```

The known face gets a **green rectangle**, while an unknown face gets a **red rectangle**.

## Installation

First, make sure Python is installed on your computer.

Then install the required libraries:

```bash
pip install opencv-python
pip install numpy
pip install face-recognition
```

You can also install them together:

```bash
pip install opencv-python numpy face-recognition
```

> **Note:** `face-recognition` uses `dlib`, so installation can sometimes be a little difficult depending on your Python version and operating system.

## Setup

### Step 1: Create the `knownfaces` folder

Create a folder called:

```text
knownfaces
```

inside your project.

### Step 2: Add Images

Put clear pictures of the people you want to recognize inside the folder.

For example:

```text
knownfaces/
├── ali.jpg
├── ahmed.jpg
└── hamza.jpg
```

It's better if each image contains **one clear face**.

### Step 3: Update the Folder Path

In the Python code, change the path according to where your folder is located:

```python
path = r"C:\Users\YourName\Documents\FaceRecognition\knownfaces"
```

### Step 4: Run the Program

Run the Python file:

```bash
python main.py
```

The webcam should open automatically.

## Controls

| Key | Action                                |
| --- | ------------------------------------- |
| `Q` | Close the webcam and stop the program |

## Important Notes

* Make sure your webcam is connected and working.
* Use clear images for better recognition.
* Try to keep only one person's face in each known-face image.
* The image file name becomes the person's name.
* If you add a new person to the folder, the program will automatically add their encoding when you run it.
* The generated `trained_faces.pkl` file should normally be kept with the project.
* This project is mainly for learning purposes and is not intended to be used as a high-security identification system.

## Possible Improvements

There are a few things I could improve in the future:

* Add a proper GUI instead of only using the OpenCV window.
* Add support for multiple faces in each known image.
* Improve recognition accuracy in different lighting conditions.
* Add attendance functionality.
* Store recognized people and timestamps in a database.
* Add a login system.
* Improve the way new faces are added.
* Add a confidence/accuracy percentage to the display.
* Make the project work with multiple cameras.

## What I Learned

While making this project, I learned how to:

* Work with OpenCV and webcams.
* Detect faces using Python.
* Generate and compare face encodings.
* Work with image color formats like BGR and RGB.
* Use NumPy for finding the closest face match.
* Save Python data using Pickle.
* Organize data using lists and files.
* Optimize a program by processing smaller images.

## Conclusion

This project helped me understand the basic idea behind **real-time face recognition**. The main concept is to convert known faces into numerical encodings and then compare those encodings with faces detected through the webcam.

It is a fairly simple project, but it was a good way for me to practice Python and understand how different libraries can work together to create something useful.

---

**Made as a learning project using Python, OpenCV, NumPy, and face_recognition.**
