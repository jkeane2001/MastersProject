import streamlit as st
import cv2
from PIL import Image, ImageEnhance, ImageColor
import numpy as np
import os

def main():

    st.title('Image Editor')
    st.text('Edit Images Here')

    st.text("Upload an Image:")
    uploadImage = st.file_uploader('Upload Image', type =['jpg', 'png', 'jpeg'])

    if uploadImage is not None:
        presentImage = Image.open(uploadImage)
        #st.image(presentImage)

        #col1, col2 = st.columns([5, 15])

        with st.sidebar:

            #slider to control Contrast
            rate = st.slider("Contrast", 0.1, 2.0, 1.0)

            enhancer = ImageEnhance.Contrast(presentImage)
            presentImage = enhancer.enhance(rate)

            #slider to control Brightness or Exposure
            rate2 = st.slider("Exposure", 0.1, 2.0, 1.0)

            enhancer2 = ImageEnhance.Brightness(presentImage)
            presentImage = enhancer2.enhance(rate2)


            #slider to control Sharpness
            rate3 = st.slider("Sharpness", 0.1, 2.0, 1.0)

            enhancer3 = ImageEnhance.Sharpness(presentImage)
            presentImage = enhancer3.enhance(rate3)


            #slider to enhance Color Vibrance
            rate4 = st.slider("Color Vibrance", 0.0, 2.0, 1.0)

            enhancer4 = ImageEnhance.Color(presentImage)
            presentImage = enhancer4.enhance(rate4)


            #rate5 = st.slider("Red", 0.0, 2.0, 1.0)
            #presentImage = Image.new('RGB', (5104, 3828))

        #with col2:
        st.image(presentImage)


if __name__ == '__main__':
    main()