import streamlit as st
import processor as prc
import os
import cv2
import time
import numpy as np

def save_image(img, img_name, num_clusters):
    DIR = 'selected_images'
    filename = f'{DIR}/{img_name}_{num_clusters}clusters.png'
    cv2.imwrite(filename, img)


def extract_channels(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img_hsv[:, :, 0]

st.write("## Further Processing of Images")



if 'further_processing' in st.session_state:

    if 'define_conversion_rate' not in st.session_state:

        if 'smoothed' not in st.session_state:
            st.session_state['smoothed'] = None

        images = [sorted(os.listdir("cropped_images"))[i] for i in st.session_state['further_processing']]

        if len(images) > 0:

            selected_image_name = st.selectbox('Select an image:', images)
            st.session_state['selected_image_index'] = images.index(selected_image_name)  # Index of the selected image

            if selected_image_name is not None:
                selected_image_path = 'cropped_images/' + selected_image_name
                selected_image = cv2.imread(selected_image_path)
                st.session_state['selected_image_name'] = selected_image_name

                original = selected_image.copy()
                st.image(selected_image, width=100)

                selected_image = extract_channels(selected_image)

            with st.form(key="Setting Up"):
                KERNEL_SIZE = st.select_slider("**Kernel Size**", options=range(1, 112, 2), key="ks", value=33)
                STOP_DIST = st.select_slider("**Blurring Distance**", options=range(0, 100), key="sd", value=60)
                NUM_CLUSTERS = st.select_slider("**Number of clusters**", options=range(2, 5), key="nc", value=4)

                if st.form_submit_button("Segment"):

                    with st.spinner("Segmenting ..."):

                        cm = prc.clustering_mask(selected_image, NUM_CLUSTERS)

                        lcm = prc.largest_component_mask(cm)

                        segmented = prc.apply_mask(original, lcm)

                        smoothed = prc.cut_stem(segmented, STOP_DIST, KERNEL_SIZE)

                        smoothed = np.where(smoothed == 0, 255, smoothed)

                        st.session_state['smoothed'] = smoothed

            col1, col2 = st.columns([1,10])
            if st.session_state['smoothed'] is not None:

                with col2:
                        st.image(st.session_state['smoothed'], width=400)
                    
                with col1:

                    if st.button("Save Image"):
                        save_image(st.session_state['smoothed'], st.session_state['selected_image_name'], NUM_CLUSTERS)
                        st.session_state['further_processing'].remove(st.session_state['further_processing'][st.session_state['selected_image_index']]) # delete value at index from session state
                        del st.session_state['smoothed']
                        del st.session_state['selected_image_name']
                        st.session_state['define_conversion_rate'] = True
                        time.sleep(2)
                        st.write("Qui")
                        st.experimental_rerun()
        else:
            st.session_state['define_conversion_rate'] = True
    else:
        st.success("You can now define the conversion rate of the images!")

else: 
    st.error("Go back to 'segment' to enable this step.")
