import streamlit as st
from PIL import Image, ImageDraw
import math

# Load the image
image_file = st.file_uploader("Upload an image", type=['png', 'jpg'])

if image_file is not None:
    image_original = Image.open(image_file)
    image_conversion = image_original.copy()  # Create a copy of the image

    image_width, image_height = image_conversion.size

    # LINE ##########

    # Calculate the default values as percentiles of the image dimensions
    x_default_1 = int(image_width * 0.25)
    x_default_2 = int(image_width * 0.75)
    y_default_1 = int(image_height * 0.45)
    y_default_2 = int(image_height * 0.55)

    # Get the coordinates for the first point on the measuring tape
    st.write("### Select the first point on the measuring tape")

    # Create the sliders with the default values
    x1_tape, x2_tape = st.slider('x1, x2', min_value=0, max_value=image_width, value=[x_default_1, x_default_2], step=1)
    y1_tape, y2_tape = st.slider('y1, y2', min_value=0, max_value=image_height, value=[y_default_1, y_default_2], step=1)

    draw = ImageDraw.Draw(image_conversion)

    if x1_tape and y1_tape and x2_tape and y2_tape:
        draw.line(((x1_tape, y1_tape), (x2_tape, y2_tape)), fill="blue", width=5)
        st.image(image_conversion, caption='Image with selected area and tape', use_column_width=True)

        # Calculate the pixel distance
        pixel_distance = math.sqrt((x2_tape - x1_tape)**2 + (y2_tape - y1_tape)**2)

    # Get the real-world distance
    real_distance = st.number_input("Enter the real-world distance in cm", min_value=0.0, step=0.1)

    if real_distance == 0:
        st.write(f"**Conversion rate**: {0} cm/pixel")
    else:
        conversion_rate = real_distance / pixel_distance
        st.write(f"**Conversion rate**: {conversion_rate} cm/pixel")

    # CROPPING ##########

    # Get the coordinates from the user for cropping
    st.write("### Adjust the sliders to define the cropping area")

    # Calculate the default values as percentiles of the image dimensions
    x_default_1_crop = int(image_width * 0.10)
    x_default_2_crop = int(image_width * 0.90)
    y_default_1_crop = int(image_height * 0.10)
    y_default_2_crop = int(image_height * 0.90)

    # Create the sliders with the default values
    x1_crop, x2_crop = st.slider('x1, x2', min_value=0, max_value=image_width, value=[x_default_1_crop, x_default_2_crop], step=1)
    y1_crop, y2_crop = st.slider('y1, y2', min_value=0, max_value=image_height, value=[y_default_1_crop, y_default_2_crop], step=1)

    image_crop = image_original.copy()

    draw = ImageDraw.Draw(image_crop)
    draw.rectangle(((x1_crop, y1_crop), (x2_crop, y2_crop)), outline="red", width=5)
    st.image(image_crop, caption='Image with selected area and tape', use_column_width=True)

    if st.button('Crop all images'):
        st.write("Cropping images")

    # FILTERING ##########
