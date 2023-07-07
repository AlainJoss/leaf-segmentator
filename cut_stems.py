import os
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

st.title('Segmented Leafs')
st.write('For each row select the best processed image and mark the stem position:')

def image_paths(dir):
    return os.listdir(dir)

DIR = 'processed_images'
img_paths = image_paths(DIR)
img_paths = sorted(img_paths)

if img_paths[0] == '.DS_Store':
    img_paths.remove('.DS_Store')

for idx, img_path in enumerate(img_paths):
    img_paths[idx] = f'{DIR}/{img_path}'

    with st.form(key='my_form'):
        for idx, group in enumerate(groups):
            cols = st.columns(k+1)  # We add an extra column for the text input
            for i, img_path in enumerate(group):
                with Image.open(img_path) as img:
                    draw = ImageDraw.Draw(img)
                    point = st.session_state.points[idx*k+i]
                    if point is not None:
                        draw.line([(0, point[1]), (img.width, point[1])], fill="red")

                    value = streamlit_image_coordinates(img, key=f"pil_{idx*k+i}")

                    if value is not None:
                        st.session_state.points[idx*k+i] = value["x"], value["y"]
                        st.experimental_rerun()

                cols[i].image(img_path)
            
            key = f'select_{str(groups.index(group))}'
            if key in st.session_state:
                selection = cols[k].selectbox("Select option:", ['further processing', '1', '2', '3'], key=key, value=st.session_state[key])
            else:
                selection = cols[k].selectbox("Select option:", ['further processing', '1', '2', '3'], key=key)
        st.form_submit_button(label='Submit', on_click=save_data)

if "submit_button" in st.session_state and st.session_state.submit_button:
    st.write('Your selections and points have been saved. Refresh the page to make new selections.')
