import streamlit as st
import numpy as np
import cv2
import easyocr
import sqlite3
import pywhatkit
from datetime import datetime
from PIL import Image

st.title("RTO Overspeeding Alert System")
st.write("Upload an image or video of a vehicle number plate to send an RTO overspeeding alert.")

# File uploader for image or video
uploaded_file = st.file_uploader("Choose an image or video file", type=["jpg", "png", "jpeg", "mp4", "avi"])

if uploaded_file is not None:
    if uploaded_file.type.startswith("image"):
        img = Image.open(uploaded_file)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        num_plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
        plates = num_plate_cascade.detectMultiScale(img, 1.1, 10)
        
        if len(plates) > 0:
            for (x, y, w, h) in plates:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            
            cropped_image = img[y:y + h, x:x + w]
            reader = easyocr.Reader(['en'])
            results = reader.readtext(cropped_image)
            
            if len(results) == 1:
                detected_text = results[0][1]
            else:
                detected_text = results[1][1]
            
            st.image(img, caption="Detected Number Plate", use_column_width=True)
            st.write(f"Detected Vehicle Number: {detected_text}")
            
            current_time = datetime.now()
            current_date = current_time.strftime("%Y-%m-%d")
            current_hour = current_time.hour
            current_minute = current_time.minute
            
            def send_message(phone_number, message):
                pywhatkit.sendwhatmsg_instantly(phone_number, message)
            
            def get_owner_details(vehicle_number):
                conn = sqlite3.connect('vehicle_info.db')
                cursor = conn.cursor()
                cursor.execute('''
                SELECT owner_name, phone_number FROM vehicle_info WHERE vehicle_number = ? 
                ''', (vehicle_number,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    owner_name, phone_number = result
                    message = f'''*RTO Alert: Overspeeding Violation*
                    {owner_name}, Your vehicle was caught overspeeding on 
                    {current_date} at {current_hour}:{current_minute}.
                    Speed Limit: 120km/h 
                    Recorded Speed: 148km/h
                    Fine: ₹2300
                    Please pay the fine within 7 days to avoid further penalties.
                    RTO Maharashtra'''
                    st.write(f"Owner Name: {owner_name}")
                    st.write(f"Phone Number: {phone_number}")
                    
                    # Create button to send WhatsApp message
                    if st.button('📱 Send WhatsApp Message'):
                        send_message(phone_number, message)
                        st.success(f"Message sent to {owner_name} at {phone_number}")
                else:
                    st.error("Vehicle details not found in the database.")
            
            get_owner_details(detected_text)
        else:
            st.error("No number plate detected in the image.")
    
    elif uploaded_file.type.startswith("video"):
        st.write("Video processing is not yet supported.")
else:
    st.write("Please upload an image or video file to get started.")