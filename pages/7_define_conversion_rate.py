import streamlit as st
from PIL import Image, ImageDraw
import math
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.write(r"""
## Define the pixel/cm Conversion Rate

Steps:
- Read in an image with a ruler.
- Place the blue line over a distance of $d$ $(cm)$.
- Write the real world distance in the text area below.
- Compute the conversion rate.
""")
         
if 'define_conversion_rate' not in st.session_state:
    st.session_state['define_conversion_rate'] = True

if 'finalize' in st.session_state:
    del st.session_state['finalize'] 


if 'define_conversion_rate' in st.session_state:

    if 'finalize' not in st.session_state:

        # Load the image
        image_file = f'images/IMG_4537.JPG'

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

            pixel_distance = 0
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

            
        if st.button('Save Conversion Rate'):
            st.session_state['finalize'] = True
            st.experimental_rerun()


    else:
        st.success("You can now create the final report!")

else: 
    st.error("Go back to 'post process' to enable this step.")