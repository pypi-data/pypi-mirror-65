"""This module contains the FacialMask class. See README.md for more information.
"""
import os
from pathlib import Path
from PIL import Image
import numpy as np
import cv2

class FacialMask:
    """Contains methods for applying a facial mask.

    The process method acts as the main driver and puts an image through
    several steps before outputing the result to an new image file:
        - Preprocessing the image to grayscale.
        - Classification of facial data.
        - Drawing rectangles around the faces classified.
        - Applying the facial mask.

    Attributes:
        filename: A string containing the user provided filename.
        pixel_size: A string containing the user provided pixel size.
        image: A numpy.ndarray containing the loaded image to be processed.
        result: A numpy.ndarray which will act as an output file.
        cascade_path: A string that contains the path to cv2 pretrained facial recognition data.
    """

    def __init__(self, filename, pixel_size):
        self.filename = filename
        self.pixel_size = int(pixel_size)
        self.image = cv2.imread(self.filename)
        self.result = self.image.copy()
        # Specify the trained cascade classifier
        base_path = Path(os.path.join(os.path.dirname(os.path.realpath(__file__)))).parents[0]
        # Assumes this directory structure
        cv2_data_path = '/cv2/data/haarcascade_frontalface_default.xml'
        self.cascade_path = str(base_path)+ cv2_data_path

    def preprocess_image(self):
        """Preprocesses the image data by converting to greyscale.

        Returns:
            numpy.ndarray: The original image greyscaled
        """
        preprocessed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(preprocessed_image)

    def classify_faces(self, preprocessed_image):
        """Uses the cv2 pretrained data model to classify faces in the image.

        Args:
            preprocessed_image (numpy.ndarray): The original image preprocessed as greyscale.

        Returns:
            numpy.ndarray: The classified faces contained in the image.
        """
        # Create a cascade classifier
        face_cascade = cv2.CascadeClassifier()
        # Load the specified classifier - haarcascade_frontalface_default
        face_cascade.load(self.cascade_path)
        return face_cascade.detectMultiScale(
            preprocessed_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

    def apply_facial_mask(self, faces):
        """Iteratees through faces an applies a pixelated facial mask.

        Args:
            faces (numpy.ndarray): The classified faces contained in the image.
        """
        if len(faces) != 0:
            # For each coordinate in faces
            for x, y, w, h in faces:
                # Create rectangle around subface
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (255, 255, 0), 1)
                # Get current index subface
                sub_face = self.image[y:y+h, x:x+w]
                # Convert to PIL format
                sub_face_pil = Image.fromarray(sub_face)
                # Scale down smoothly down to 16x16 pixels
                resample = Image.BILINEAR
                resize = (self.pixel_size, self.pixel_size)
                scaled_down = sub_face_pil.resize(resize, resample)
                # Scale up using NEAREST to original size
                scaled_up = np.array(scaled_down.resize(sub_face_pil.size, Image.NEAREST))
                # Convert back to OpenCV format
                facial_mask = np.array(scaled_up)
                # Apply facial mask
                self.result[y:y+facial_mask.shape[0], x:x+facial_mask.shape[1]] = facial_mask # pylint: disable=E1136  # pylint/issues/3139

    def process_image(self):
        """Main driver.

        Steps:
            - Preprocess the image to grayscale.
            - Classify facial data.
            - Draw rectangles around the faces classified.
            - Apply the facial mask.
        """
        preprocessed_image = self.preprocess_image()
        faces = self.classify_faces(preprocessed_image)
        self.apply_facial_mask(faces)
        cv2.imwrite("./result.png", self.result)
