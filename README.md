# ASL AI Translator

## Synopsis
The ASL AI trasnlator is meant to demonstrate how a neural network can be trained to translate hand gestures for ASL **(American Sign Langugage)** into text and or voice output. Whereas most projects of this type have utilized CNN **(Convolutional Neural networks)** to scan images of hand gestures, this system utilizes an external directory - [Google's MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) - to preproocess the image data. Consequently, this model is composed primarily of a fully-connected ANN **(Artificial Neural Network)** which is used to classify the corrodinates which are genrated from the MediaPipe output as letters of the alphabet and or control characters for interacting with the MediaPipe interface.

## Configuration Notes
The various Jupyter Notebooks provided for this project have been adapted to work within Google Colab. Therefore, directories and file paths for reading and writing data have been also adapted to work within that environment. Should you need to alter them, feel free to adjust the file paths accordingly.

The Python scripts, on the other hand, have been adapted to work within a windows environment and should be addjusted accordingly.

### Libraries needed for python scripts
The python scripts which will be run locally, will require the installation of libraries. These are the commands for installing the dependencies utilizing pip

`pip install mediapipe`
`pip install opencv-python`
`pip install gTTS`


## Contributors
- Mervin McDougall
- Francisco Del Castillo Munoz
- David Plotkin
