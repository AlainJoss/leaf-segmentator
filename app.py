import os
import streamlit as st
from st_clickable_images import clickable_images


st.title('Processed Images')

st.write('For each row select the best processed image.')

def image_paths(dir):
    return os.listdir(dir)

DIR = 'processed_images'
img_paths = image_paths(DIR)
img_paths = sorted(img_paths)

if img_paths[0] == '.DS_Store':
    img_paths.remove('.DS_Store')

for idx, img_path in enumerate(img_paths):
    img_paths[idx] = f'{DIR}/{img_path}'

groups = []
k = 4
for i in range(0, len(img_paths), k):
    groups.append(img_paths[i:i+k])
    st.write(img_paths[i:i+k])

cols = st.columns(k)

for group in groups:
    for i, img_path in enumerate(group):
        cols[i].image(img_path)


