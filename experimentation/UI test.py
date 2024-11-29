

import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk
import cv2

# Import the required module for text to speech conversion
from gtts import gTTS
# This module is imported so that we can play the converted audio
import os

# Save text to file
def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_display.get("1.0", tk.END))

# update_text display
def update_text_display(content_list):
    # Clear the text display
    text_display.delete("1.0", tk.END)
    # Convert the list to a string and insert it
    text_display.insert(tk.END, ''.join(content_list))

# Say it 
def speak():
    language = 'en' # Language in which you want to convert
    text = text_display.get("1.0", "end-1c")  
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save(path)   # Saving the converted audio in a mp3 file 

    # Playing the converted file
    os.system(f'start "" "{path}"')

def update_frame():
    ret, frame = cap.read()

    if ret:
        # Convert the frame to RGB (from BGR)
        frame = cv2.flip(frame,1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert the frame to an Image
        img = Image.fromarray(frame_rgb)
        img = img.resize((640, 480))  # Resize to fit the canvas

        # Convert the Image to ImageTk format
        img_tk = ImageTk.PhotoImage(image=img)
        
        # Update the canvas with the new image
        camera_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        
        # Keep a reference to the image object
        camera_canvas.image = img_tk
    
    # Update the frame every 10 ms
    root.after(10, update_frame)


# define the saving directory
current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, 'final_project.mp3')


# Create main window
root = tk.Tk()
root.title("Sign Language to Text")
root.configure(bg='ghost white')

# Video feed frame
camera_canvas = tk.Canvas(root, width=640, height=480)
camera_canvas.grid(row=0, column=0, columnspan=3)

# Display area for recognized text
text_display = tk.Text(root, width=40, height=5, font=("Arial", 12))
text_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5)


# Buttons for clear, say, and quit
clear_button = tk.Button(root, text="Clear All", width=15, bg="lemon chiffon", command=lambda: text_display.delete("1.0", tk.END))
clear_button.grid(row=2, column=0, padx=5, pady=5)

speak_button = tk.Button(root, text="Say it", width=15, bg="green",fg="white", command=lambda: speak())
speak_button.grid(row=2, column=1, padx=5, pady=5)

quit_button = tk.Button(root, text="Quit", width=15, bg="red",fg="white", command=root.quit)
quit_button.grid(row=2, column=2, padx=5, pady=5)


# Button to update the text display with the list
content_list = ['H','e','l','l','o',' ','W','o','r','l','d']
update_button = tk.Button(root, text="Update Text Display", command=lambda: update_text_display(content_list))
update_button.grid(row=1, column=0, padx=10, pady=5)

# delete the last character
delete_button = tk.Button(root, text="Delete", command=lambda: text_display.delete('end-2c','end'))
delete_button.grid(row=1, column=2, padx=10, pady=5)

# insert A to the main text
A_button = tk.Button(root, text="Insert A", command=lambda: text_display.insert(tk.END, "A"))
A_button.grid(row=1, column=1, padx=10, pady=5)

cap = cv2.VideoCapture(0)
# Start updating the frames
update_frame()

# Run the application
root.mainloop()

# Release the camera when the window is closed
cap.release()
cv2.destroyAllWindows()










