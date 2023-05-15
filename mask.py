# Import libraries
import cv2 as cv
import numpy as np
import streamlit as st
from PIL import Image
import io

# Load an image
uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg'])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_original = cv.imdecode(file_bytes, 1)

    # Convert the image to HSV
    hsv_image = cv.cvtColor(image_original, cv.COLOR_BGR2HSV)

    # Define color boundaries
    st.header('Define HSV Color Boundaries for Masking')
    hue = st.slider('Hue', min_value=0, max_value=180, value=(40, 116))
    saturation = st.slider('Saturation', min_value=0, max_value=255, value=(28, 255))
    value = st.slider('Value', min_value=0, max_value=255, value=(0, 116))

    lower_bound = np.array([hue[0], saturation[0], value[0]])
    upper_bound = np.array([hue[1], saturation[1], value[1]])

    # Create a mask
    mask = cv.inRange(hsv_image, lower_bound, upper_bound)

    # Apply the mask to the image
    masked_image = cv.bitwise_and(image_original, image_original, mask=mask)

    # Convert BGR images to RGB for displaying
    image_original = cv.cvtColor(image_original, cv.COLOR_BGR2RGB)
    masked_image = cv.cvtColor(masked_image, cv.COLOR_BGR2RGB)

    # Display the original and masked images
    col1, col2 = st.columns(2)
    col1.image(image_original, use_column_width=True)
    col2.image(masked_image, use_column_width=True)
