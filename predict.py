import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load model
model = load_model("model.h5")

# Classes (same order)
classes = ["dry", "ewaste", "wet"]

# Give image path
img_path = input("Enter image path: ")

# Read image
img = cv2.imread(img_path)
img = cv2.resize(img, (128,128))
img = img / 255.0
img = np.reshape(img, [1, 128, 128, 3])

# Predict
prediction = model.predict(img)

confidence = np.max(prediction) * 100
result = classes[np.argmax(prediction)]

print(f"Prediction: {result}")
print(f"Confidence: {confidence:.2f}%")