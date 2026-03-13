# from paddleocr import PaddleOCR

# ocr = PaddleOCR(use_angle_cls=True, lang='en')

# result = ocr.ocr('c:/Users/SRIRAM/Pictures/adh.jfif')

# for line in result:
#     for word in line:
#         print(word[1][0])



import os
import cv2
import re
from paddleocr import PaddleOCR

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Folder containing Aadhaar images
folder = "C:/Users/SRIRAM/Desktop/smart-outpass/static/aadhar_cards"


def extract_pincode(image_path):

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found:", image_path)
        return None

    h, w, _ = image.shape

    # Crop lower half (address region)
    address_region = image[int(h * 0.5):h, 0:w]

    # Convert to grayscale
    gray = cv2.cvtColor(address_region, cv2.COLOR_BGR2GRAY)

    # Improve OCR accuracy
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Run OCR
    result = ocr.ocr(gray)

    extracted_text = ""

    for line in result:
        for word in line:

            text = word[1][0]
            confidence = word[1][1]

            if confidence > 0.7:
                extracted_text += text + " "

    print("Detected Text:", extracted_text)

    # Find PIN code
    match = re.search(r"\b\d{6}\b", extracted_text)

    if match:
        return match.group()

    return None


# Store PIN codes
pincodes = []

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    if file.lower().endswith((".jpg", ".jpeg", ".png", ".jfif", ".webp")):

        print("\nProcessing:", file)

        pin = extract_pincode(path)

        if pin:
            print("PINCODE:", pin)
            pincodes.append(pin)
        else:
            print("No PINCODE found")


print("\n==========================")
print("Extracted PINCODES:", pincodes)

# Compare PIN codes
if len(pincodes) == 0:
    print("No valid pincodes detected")

elif len(set(pincodes)) == 1:
    print(" All Aadhaar cards have SAME PINCODE")

else:
    print(" Aadhaar cards have DIFFERENT PINCODES")