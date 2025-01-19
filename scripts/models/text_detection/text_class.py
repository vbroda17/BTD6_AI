import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image


class TextRecognitionModel:
    def __init__(self, model_path, label_mapping_path):
        self.model = tf.keras.models.load_model(model_path)
        with open(label_mapping_path, "r") as f:
            self.label_mapping = json.load(f)

    def preprocess_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        np_image = np.array(image)
        mask = (np_image[:, :, 0] > 30) | (np_image[:, :, 1] > 30) | (np_image[:, :, 2] > 30)
        np_image[mask] = [255, 255, 255]
        image = Image.fromarray(np_image).resize((256, 64), Image.Resampling.LANCZOS)
        return np.array(image) / 255.0

    def predict_text(self, image_path):
        image = self.preprocess_image(image_path)
        image = np.expand_dims(image, axis=0)
        predictions = self.model.predict(image)
        predicted_label = np.argmax(predictions, axis=1)[0]
        return self.label_mapping[predicted_label]


if __name__ == "__main__":
    model_path = "datasets/txt/text_recognition_model.h5"
    label_mapping_path = "datasets/txt/label_mapping.json"

    recognizer = TextRecognitionModel(model_path, label_mapping_path)

    test_image_path = "datasets/txt/images/#Ouch_2.png"  # Update with your test image path
    print("Recognized Text:", recognizer.predict_text(test_image_path))
