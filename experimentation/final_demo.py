
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Import the required module for text to speech conversion
from gtts import gTTS

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pandas as pd

import copy
import os

def calc_landmark_list(W,H, landmarks): # Get landmarks list
    image_width = W
    image_height = H


    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list): # Pre-process landmark lists
    temp_landmark_list = copy.deepcopy(landmark_list)

    aux_x = []
    aux_y = []

    # Convert to relative coordinates
    for landmark_point in temp_landmark_list:
        current_x, current_y = landmark_point[0], landmark_point[1]
        aux_x.append(current_x)
        aux_y.append(current_y)


    min_x, min_y = min(aux_x), min(aux_y)
    max_x, max_y = max(aux_x), max(aux_y)

    def normalize_(n, min_value, max_value):
        return (n - min_value) / (max_value - min_value)

    x_normalized = list(map(lambda x: normalize_(x, min_x, max_x), aux_x))
    y_normalized = list(map(lambda x: normalize_(x, min_y, max_y), aux_y))

    #print(x_normalized)
    #print(y_normalized)
    final_list = [coordenate for pair in zip(x_normalized, y_normalized) for coordenate in pair]

    return final_list, min_x, max_x, min_y, max_y

def update_history (last_char,prediction,character_count,limit): # Calculate predictions count

    if prediction != last_char:
        character_count = 0
        last_char = prediction
    elif prediction == last_char:
        character_count += 1

    if character_count >= limit:
        print(prediction)

        if prediction == 'Space':
            text_display.insert(tk.END, ' ')
        elif prediction == 'Delete':
            text_display.delete('end-2c','end')
        elif prediction == 'Speak':
            speak()
        elif prediction == 'Exit':
            root.quit()
        elif prediction == 'Clear':
            text_display.delete("1.0", tk.END)
        else:
            text_display.insert(tk.END, prediction)

        character_count =0
    
    return last_char,character_count

def speak(): # Say it
    path = os.path.join(current_dir, 'final_project.mp3')

    language = 'en' # Language in which you want to convert
    # language = 'es'
    text = text_display.get("1.0", "end-1c")  
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save(path)   # Saving the converted audio in a mp3 file 

    # Playing the converted file
    os.system(f'start "" "{path}"')

def update_frame(last_char, character_count): # Update Frame
    ret, frame = cap.read()
    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                frame_rgb,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            
            
            landmark_list = calc_landmark_list(W,H, hand_landmarks)
            #print(landmark_list)

            pre_processed_landmark, min_x, max_x, min_y, max_y = pre_process_landmark(landmark_list) # preprocess landmarks
            input = np.array(pre_processed_landmark)
            input = input.reshape(1, -1)  # Reshape to (1, 42)

            #print((pre_processed_landmark))
            #print(input)            
            #print(hand_landmarks)

        # Get prediction values and confidence
        prediction = model.predict(input, verbose=False)
        index = np.argmax(prediction, axis=None)
        confidence = round(max(max(prediction))*100,1)
        pred_character = labels[index]

        # logic for getting a text
        if confidence > 60:
            last_char, character_count = update_history(last_char, pred_character, character_count, limit)

        # Draw rectangle and annotation

        

        cv2.rectangle(frame_rgb, (min_x - 10, min_y - 10), (max_x + 10, max_y + 10), (255, 0, 0), 2)
        final_text = str(pred_character)+"-"+str(confidence)
        cv2.putText(frame_rgb, final_text, (min_x, min_y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 2, cv2.LINE_AA)


    # Convert the frame to an Image
    img = Image.fromarray(frame_rgb)
    img = img.resize((640, 480))  # Resize to fit the canvas

    # Convert the Image to ImageTk format
    #img_tk = ImageTk.PhotoImage(image=img)
    img_tk = ImageTk.PhotoImage(image=img)

    
    # Update the canvas with the new image
    camera_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    # Keep a reference to the image object
    camera_canvas.image = img_tk
    
    # Update the frame every 10 ms
    root.after(5, lambda: update_frame(last_char, character_count))

# define the saving directory
current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'asl_model.keras')
# Load the model
model = tf.keras.models.load_model(path)

# ------ Layout ------
# Create main window
root = tk.Tk()
root.title("Sign Language to Text")
root.configure(bg='ghost white')

# Video feed frame
camera_canvas = tk.Canvas(root, width=640, height=480)
camera_canvas.grid(row=0, column=0, columnspan=3)

# Display area for recognized text
text_display = tk.Text(root, width=40, height=2, font=("Arial", 20))
text_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Buttons for clear, say, and quit
clear_button = tk.Button(root, text="Clear All", width=20, bg="lemon chiffon", command=lambda: text_display.delete("1.0", tk.END))
clear_button.grid(row=2, column=0, padx=5, pady=5)

speak_button = tk.Button(root, text="Say it", width=20, bg="green",fg="white", command=lambda: speak())
speak_button.grid(row=2, column=1, padx=5, pady=5)

quit_button = tk.Button(root, text="Quit", width=15, bg="red",fg="white", command=root.quit)
quit_button.grid(row=2, column=2, padx=5, pady=5)

# ------ Layout ------


# Camera
cap = cv2.VideoCapture(0)

# Import model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.45)

# initialize variables
last_char = ""
character_count = 0
labels = ['A', 'B', 'C', 'Clear', 'D', 'E', 'Exit', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'Speak', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Delete', 'Space']
limit = 10

# Start updating the frames
update_frame(last_char, character_count)

# Run the application
root.mainloop()

# Release the camera when the window is closed
cap.release()
cv2.destroyAllWindows()