🚘 Number Plate Detection & RTO Overspeeding Alert System

This project detects vehicle number plates from images using OpenCV and EasyOCR, matches the plate with vehicle owner data from a SQLite database, and sends an overspeeding alert via WhatsApp using pywhatkit.

🔧 Technologies Used

Python

Streamlit – for building the web UI

OpenCV – for number plate detection using Haar cascades

EasyOCR – for extracting text from number plate

SQLite – for storing vehicle owner data

PyWhatKit – for sending WhatsApp alerts

PIL & NumPy – for image processing

🛠️ How the System Works – Step-by-Step

🔹 1. User Uploads Image

A user uploads a vehicle image using Streamlit UI.

Image is read and converted from RGB to BGR (for OpenCV processing).

🔹 2. Detect Number Plate using Haar Cascade

Haar Cascade XML file (haarcascade_russian_plate_number.xml) is used to detect number plates.

OpenCV's detectMultiScale() is used to find number plate regions in the image.

A rectangle is drawn on the detected number plate for visualization.

🔹 3. Crop Number Plate

Detected region is cropped using the coordinates from detectMultiScale.

 4. Text Extraction with EasyOCR

The cropped number plate image is passed to EasyOCR to read the text (vehicle number).

If multiple text elements are found, the second one is selected assuming better accuracy.

🔹 5. Vehicle Lookup from Database

A SQLite database (vehicle_info.db) contains vehicle_number, owner_name, and phone_number.

The extracted number plate text is queried against this database.
