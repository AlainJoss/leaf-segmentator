import streamlit as st
import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image

st.write("## Download the Final Report")

if 'finalize' in st.session_state:

    col1, col2 = st.columns([1,2])

    with col1:

        def calculate_area(image, conversion_rate):
            """Calculate the area of non-white pixels in the image."""
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            mask = np.where(grayscale == 255, 0, 1)
            pixel_area = np.sum(mask)
            area_cm2 = pixel_area * conversion_rate

            return area_cm2

        # Create a DataFrame to store the results
        results = pd.DataFrame(columns=["Image", "Area_cm2"])

        # Iterate over all images in the selected_images directory
        for filename in os.listdir("selected_images"):
            image = cv2.imread(os.path.join("selected_images", filename))
            area_cm2 = calculate_area(image, st.session_state['conversion_rate'])
            result = pd.DataFrame([{"Image": filename, "Area_cm2": area_cm2}])
            results = pd.concat([results, result], ignore_index=True)

        # Display the results
        st.write(results)

        # Save the results to an Excel file
        results.to_excel("results.xlsx", index=False)

        # Create a button to download the results
        st.download_button(
            "Download Results",
            data=open("results.xlsx", "rb"),
            file_name="results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col2:

        # Get all image paths in the selected_images directory
        img_paths = [os.path.join("selected_images", filename) for filename in os.listdir("selected_images")]

        # Create a grid with 5 images per row
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
    st.error("Go back to 'post process' to enable this step.")
