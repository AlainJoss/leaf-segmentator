import os
import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(
    layout="wide"
)

st.write("## Crop Images")

if 'crop' in st.session_state:
    if 'segment' not in st.session_state:

        st.write("""
        Steps:
        - Adjust the sliders to define the cropping area.
        - y1 must be zero, therefore you cannot change it.
        - Leave out all the the black boarders.
        - Crop all images by pressing the button.
        """)

        # Load a sample image
        id = st.session_state["img_paths"][0]
        image_file = f'images/stem_cutted/{id}'
        image_original = Image.open(image_file)
        image_conversion = image_original.copy()  # Create a copy of the image
        image_width, image_height = image_conversion.size

        # Default crop
        x_default_1_crop = 757
        x_default_2_crop = 2993
        y_default_1_crop = 0
        y_default_2_crop = 3638

        # Create sliders
        x1_crop, x2_crop = st.slider('x1, x2', min_value=0, max_value=image_width, value=[x_default_1_crop, x_default_2_crop], step=1)
        y2_crop = st.slider('y2', min_value=0, max_value=image_height, value=y_default_2_crop, step=1)
        y1_crop = 0

        # Draw rectangle
        image_crop = image_original.copy()
        draw = ImageDraw.Draw(image_crop)
        draw.rectangle(((x1_crop, y1_crop), (x2_crop, y2_crop)), outline="red", width=5)

        col1, col2 = st.columns([1.5,10])
        with col2:
            st.image(image_crop, caption='Image with selected area and tape', width=600)
        with col1:
            if st.button('Crop all images'):
                st.spinner("Cropping ... stay tuned!")
                INPUT_DIR = 'images/stem_cutted'
                OUTPUT_DIR = 'images/cropped'
                
                if not os.path.exists(OUTPUT_DIR):
                    os.makedirs(OUTPUT_DIR)

                image_files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]

                # Crop and save
                for image_file in image_files:
                    img = Image.open(os.path.join(INPUT_DIR, image_file))
                    cropped_img = img.crop((x1_crop, y1_crop, x2_crop, y2_crop))
                    cropped_img.save(os.path.join(OUTPUT_DIR, image_file))

                st.success(f"All images have been cropped and saved to {OUTPUT_DIR}!")
                st.session_state['segment'] = True
                st.experimental_rerun()
    else:
        st.session_state['segment'] = True
        st.success("You can now segment the leafs!")
else: 
    st.error("Go back to 'rotate and cut stems' to enable this step.")
