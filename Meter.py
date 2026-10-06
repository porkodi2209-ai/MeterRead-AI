import streamlit as st
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

st.set_page_config(
    page_title="MeterRead AI"
)

st.title("MeterRead AI")
st.write("OCR-Based Utility Meter Reading Assistant")

uploaded_file = st.file_uploader(
    "Upload Meter Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Meter Image",
        width=500
    )

    if st.button("Read Meter"):

        gray = image.convert("L")
        gray = ImageEnhance.Contrast(gray).enhance(2)
        gray = gray.filter(ImageFilter.SHARPEN)

        text = pytesseract.image_to_string(
            gray,
            config="--psm 11"
        )

        reading = None

        for line in text.splitlines():

            if "kwh" in line.lower():

                numbers = re.findall(
                    r"\d{3,8}",
                    line
                )

                if numbers:
                    reading = numbers[-1]
                    break

        if reading is None:

            number_text = pytesseract.image_to_string(
                gray,
                config="--psm 6 -c tessedit_char_whitelist=0123456789"
            )

            numbers = re.findall(
                r"\b\d{4,8}\b",
                number_text
            )

            if numbers:
                reading = numbers[0]

        if reading:

            st.success("Meter reading detected!")

            st.subheader("Meter Reading")

            st.metric(
                "Current Reading",
                f"{reading} kWh"
            )

        else:

            st.error("Meter reading not detected.")