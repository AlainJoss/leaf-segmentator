import streamlit as st
import os
import cv2
import numpy as np
import pandas as pd


##### FUNCTIONS #####

def calculate_area(image, conversion_rate):
    """Calculate the area of non-white pixels in the image."""
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = np.where(grayscale == 255, 0, 1)
    pixel_area = np.sum(mask)
    area_cm2 = pixel_area * conversion_rate

    return area_cm2


##### PAGE #####

st.set_page_config(
    layout="wide"
)

st.write("## Download the Final Report")

INPUT_DIR = 'images/selected'

if 'finalize' in st.session_state:

    col1, col2 = st.columns([1,3])

    with col1:

        # DataFrame for storing results
        results = pd.DataFrame(columns=["Image", "Area_cm2"])

        file_names = os.listdir(INPUT_DIR)

        for old_name in file_names:
            # Keep only the first 12 characters of the filename
            new_name = old_name[:12]
            # Only rename the file if the name has changed
            if new_name != old_name:
                os.rename(os.path.join(INPUT_DIR, old_name), os.path.join(INPUT_DIR, new_name))


        # Iterate over all images in the selected_images directory
        for filename in file_names:
            image = cv2.imread(os.path.join(INPUT_DIR, filename))
            area_cm2 = calculate_area(image, st.session_state['conversion_rate'])
            result = pd.DataFrame([{"Image": filename, "Area_cm2": area_cm2}])
            results = pd.concat([results, result], ignore_index=True)

        # Display the results
        st.dataframe(results, height=600, width=300)

        # Report download
        results.to_excel("results.xlsx", index=False)
        st.download_button(
            "Download Results",
            data=open("results.xlsx", "rb"),
            file_name="results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col2:
        img_paths = [os.path.join(INPUT_DIR, filename) for filename in os.listdir(INPUT_DIR)]
        
        # Image grid
        for i in range(0, len(img_paths), 5):
            cols = st.columns(5)
            for j in range(5):
                if i + j < len(img_paths):
                    # Load the image
                    img_path = img_paths[i + j]
                    image = cv2.imread(img_path)
                    # Calculate the area
                    area_cm2 = calculate_area(image, st.session_state['conversion_rate'])
                    # Display the image and its area
                    cols[j].write(f"Area: {round(area_cm2, 5)} cm^2")
                    cols[j].image(image)
else: 
    st.error("Go back to 'define conversion rate' to enable this step.")
