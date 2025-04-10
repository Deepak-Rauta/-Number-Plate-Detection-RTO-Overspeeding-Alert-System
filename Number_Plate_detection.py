import matplotlib.pyplot as plt 
import easyocr
import cv2
import sqlite3
import pywhatkit
from datetime import datetime

img = cv2.imread('samplenumberplate2.jpg', cv2.IMREAD_GRAYSCALE)
num_plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
plates = num_plate_cascade.detectMultiScale(img, 1.1, 10)
print(plates)

for (x, y, w, h) in plates:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

cropped_image = img[y:y + h, x:x + w]
reader = easyocr.Reader(['en'])
image_path = cropped_image
results = reader.readtext(image_path)

if len(results) == 1:
    detected_text = results[0][1]
else:
    detected_text = results[1][1]

def send_message(phone_number, message):
    pywhatkit.sendwhatmsg_instantly(phone_number, message)

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")
current_hour = current_time.hour
current_minute = current_time.minute

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
        send_message(phone_number, message)
    else:
        return None, None

get_owner_details(detected_text)
