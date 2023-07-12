import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import processor as prc
import shutil
import time

st.write("## Segment Images")

if 'start_segmenting' not in st.session_state:
    st.session_state['start_segmenting'] = False

if 'num_clusters' not in st.session_state:
    st.session_state['num_clusters'] = 0

if 'clustering_mask' in st.session_state:

    if 'choose_image' not in st.session_state:
        
        st.write("""
        The processing procedure will take some time:
        - set up the parameters
        - enjoy a coffee break.
        """)
  
        with st.form("Set-Up"):
            KERNEL_SIZE = st.select_slider("**Kernel Size**", options=range(1, 112, 2), key="ks", value=33)
            STOP_DIST = st.select_slider("**Blurring Distance**", options=range(0, 100), key="sd", value=60)
            NUM_CLUSTERS = st.select_slider("**Number of clusters**", options=range(2, 5), key="nc", value=4)

            st.session_state['num_clusters'] = NUM_CLUSTERS

            if st.form_submit_button("Segment"):
                st.session_state['start_segmenting'] = True
                if os.path.exists('processed_images'):
                    shutil.rmtree('processed_images')

        if st.session_state['start_segmenting']:

            if st.button("Stop and Reset"):
                if os.path.exists('processed_images'):
                    shutil.rmtree('processed_images')
                st.session_state['start_segmenting'] = False
                st.experimental_rerun()

            st.write("")
            st.write("#### Segmenting ...")

            ATTEMPTS = 20
            DIR = 'processed_images'
            os.makedirs(DIR, exist_ok=True)

            original_images = prc.read_images('cropped_images')
            
            processed_images = original_images.copy()

            prc.extract_channels(processed_images)

            total_iterations = len(processed_images) * (NUM_CLUSTERS-1)
            counter = 0

            progress_bar = st.progress(0)

            empty_space = st.empty()
            text_placeholder = st.empty()
            image_placeholder = st.empty()

            for num_clusters in range(2, NUM_CLUSTERS + 1):
                for idx, img in enumerate(processed_images):
                    counter += 1

                    cm = prc.clustering_mask(processed_images[idx], num_clusters)

                    lcm = prc.largest_component_mask(cm)

                    segmented = prc.apply_mask(original_images[idx], lcm)

                    smoothed = prc.cut_stem(segmented, STOP_DIST, KERNEL_SIZE)

                    smoothed = np.where(smoothed == 0, 255, smoothed)

                    empty_space.markdown("")
                    text_placeholder.write(f"#### Image {counter}")
                    image_placeholder.image(smoothed, width=500)

                    img_name = st.session_state['original_image_paths'][idx]
                    
                    filename = f'{DIR}/{img_name}_{num_clusters}clusters.png'
                   
                    cv2.imwrite(filename, smoothed)

                    progress_bar.progress((counter) / total_iterations, text=f"Iteration {counter}/{total_iterations}")

            time.sleep(1.5)
            st.session_state['choose_image'] = True
            st.experimental_rerun()

    else:
        st.success("You can now post process the images!")

else: 
    st.error("Go back to 'crop' to enable this step.")