import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates  # New library for image clicks

# Define moisture levels based on color
moisture_levels = [
    {"state": "Very High (Fully Submerged)", "color": (0, 255, 0), "range": [(0, 100, 0), (50, 255, 50)], "desc": "Fully Hydrated - Bright Green / Blue-Green"},
    {"state": "High (Wet Surface, After Rain)", "color": (0, 200, 100), "range": [(50, 100, 50), (100, 255, 150)], "desc": "Hydrated - Green / Blue-Green"},
    {"state": "Moderate (Damp, Humid Conditions)", "color": (100, 100, 50), "range": [(80, 80, 30), (150, 150, 100)], "desc": "Partially Hydrated - Dark Green / Brownish-Green"},
    {"state": "Low (Dry Surface, Drought Conditions)", "color": (150, 100, 50), "range": [(100, 50, 20), (200, 150, 80)], "desc": "Dehydrated - Yellow / Brown / Dark Brown"},
    {"state": "Very Low (Extreme Dryness, Dormant State)", "color": (50, 50, 50), "range": [(0, 0, 0), (100, 100, 100)], "desc": "Highly Dehydrated - Black / Dark Brown"},
]

# Function to find closest moisture level based on RGB value
def get_moisture_level(r, g, b):
    for level in moisture_levels:
        lower, upper = level["range"]
        if lower[0] <= r <= upper[0] and lower[1] <= g <= upper[1] and lower[2] <= b <= upper[2]:
            return level["state"], level["desc"]
    return "Unknown", "No moisture data available."

# Streamlit App UI
st.title("🌱 Nostoc spp. Moisture Level Detector")
st.write("Click on the image to determine moisture level based on color.")

# File uploader
uploaded_file = st.file_uploader("Upload an image of Nostoc spp.", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Convert to OpenCV format
    image = Image.open(uploaded_file)
    img_cv = np.array(image)

    # Display image and get click position
    clicked_pos = streamlit_image_coordinates(image, key="color_picker")

    if clicked_pos:
        x, y = clicked_pos["x"], clicked_pos["y"]

        # Get RGB values from clicked position
        r, g, b = img_cv[y, x][:3]

        # Find moisture level
        moisture_state, description = get_moisture_level(r, g, b)

        # Display results
        st.subheader("Detected Moisture Level:")
        st.write(f"**Moisture State:** {moisture_state}")
        st.write(f"**Description:** {description}")
        st.write(f"**Detected RGB:** R={r}, G={g}, B={b}")

        # Show color box
        color_box = np.zeros((100, 100, 3), dtype=np.uint8)
        color_box[:, :] = [b, g, r]  # OpenCV uses BGR
        st.image(color_box, caption="Detected Color", width=100)
