import streamlit as st
import processor as prc
import os
import cv2
import time
import numpy as np

st.write("## Further Processing of Images")

def save_image(img, img_name, num_clusters):
    DIR = 'selected_images'
    filename = f'{DIR}/{img_name}_{num_clusters}clusters.png'
    cv2.imwrite(filename, img)


# Get all the images
images = [sorted(os.listdir("cropped_images"))[i] for i in st.session_state['further_processing']]

# Extract the image names
image_names = [os.path.basename(img_path) for img_path in images]

# Create a select box with the image names
selected_image = st.selectbox('Select an image:', image_names)

selected_image = 'cropped_images/' + selected_image

if selected_image is not None:
    # st.image(selected_image)
    pass

def extract_channels(images):
    for idx, img in enumerate(images):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        images[idx] = img_hsv[:, :, 0]



with st.form(key="Setting Up"):
    KERNEL_SIZE = st.select_slider("**Kernel Size**", options=range(1, 112, 2), key="ks", value=33)
    STOP_DIST = st.select_slider("**Blurring Distance**", options=range(0, 100), key="sd", value=60)
    NUM_CLUSTERS = st.select_slider("**Number of clusters**", options=range(2, 5), key="nc", value=4)

    if st.form_submit_button("Segment"):
        extract_channels([selected_image])
        st.write("ok")

        for num_clusters in range(2, NUM_CLUSTERS + 1):

            selected_image = cv2.imread(f'{selected_image}')

            st.write(f"Image shape: {selected_image.shape}")
            st.write(f"Image dtype: {selected_image.dtype}")
            st.write(f"Min and max image values: {selected_image.min()}, {selected_image.max()}")



            cm = prc.clustering_mask(selected_image, num_clusters)

            lcm = prc.largest_component_mask(cm)

            st.write("ok")

            segmented = prc.apply_mask(selected_image, lcm)

            smoothed = prc.cut_stem(segmented, STOP_DIST, KERNEL_SIZE)

            smoothed = np.where(smoothed == 0, 255, smoothed)

            # Display the processed image and provide a save button
            st.image(smoothed)

            if st.button("Save Image and Proceed to Next"):
                save_image(smoothed, img_name, NUM_CLUSTERS)
                st.experimental_rerun()
