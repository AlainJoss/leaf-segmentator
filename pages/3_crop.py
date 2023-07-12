import os
import streamlit as st
from PIL import Image, ImageDraw

st.write("## Crop Images")

if 'crop_images' in st.session_state:

    if 'clustering_mask' not in st.session_state:

        st.write("""
        - Adjust the sliders to define the cropping area.
        - y1 must be zero, therefore you cannot change it.
        - Leave out all the the black boarders.
        - Crop all images by pressing the button.
        """)

        # Load a sample image
        id = st.session_state["img_paths"][0]
        image_file = f'stem_cutted_leafs/{id}'

        image_original = Image.open(image_file)
        image_conversion = image_original.copy()  # Create a copy of the image

        image_width, image_height = image_conversion.size


        # CROPPING ##########

        # Calculate the default values as percentiles of the image dimensions
        x_default_1_crop = 757
        x_default_2_crop = 2993
        y_default_1_crop = 0
        y_default_2_crop = 3638

        # Create the sliders with the default values
        x1_crop, x2_crop = st.slider('x1, x2', min_value=0, max_value=image_width, value=[x_default_1_crop, x_default_2_crop], step=1)
        y2_crop = st.slider('y2', min_value=0, max_value=image_height, value=y_default_2_crop, step=1)
        y1_crop = 0
        image_crop = image_original.copy()

        draw = ImageDraw.Draw(image_crop)
        draw.rectangle(((x1_crop, y1_crop), (x2_crop, y2_crop)), outline="red", width=5)

        col1, col2 = st.columns([1.25,10])

        with col2:
            st.image(image_crop, caption='Image with selected area and tape', width=600)

        with col1:
            if st.button('Crop all images'):

                st.spinner("Cropping ... stay tuned!")

                # Define the directories
                input_dir = 'stem_cutted_leafs'
                output_dir = 'cropped_images'
                
                # Create output directory if it does not exist
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Get all image files in the input directory
                image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

                # Loop through each image file
                for image_file in image_files:
                    # Open the image file
                    img = Image.open(os.path.join(input_dir, image_file))

                    # Crop the image
                    cropped_img = img.crop((x1_crop, y1_crop, x2_crop, y2_crop))

                    # Save the cropped image to the output directory
                    cropped_img.save(os.path.join(output_dir, image_file))

                st.success(f"All images have been cropped and saved to {output_dir}!")
                st.session_state['clustering_mask'] = True
                st.experimental_rerun()

    else:
        st.success("You can now segment the leafs!")

else: 
    st.error("Go back to 'rotate and cut stems' to enable this step.")
