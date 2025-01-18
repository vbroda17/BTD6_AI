import os
import random
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow as tf

# Paths
TXT_FOLDER = "txts"
DATASET_FOLDER = "datasets/txt"
IMAGES_FOLDER = os.path.join(DATASET_FOLDER, "images")
METADATA_FILE = os.path.join(DATASET_FOLDER, "metadata.json")
FONT_PATH = "fonts/LuckiestGuy-Regular.ttf"
NORMALIZED_FOLDER = os.path.join(DATASET_FOLDER, "normalized_images")
TARGET_SIZE = (256, 64)  # Width, Height for normalization

# Image settings
IMAGE_WIDTH, IMAGE_HEIGHT = TARGET_SIZE


def random_color():
    """Generate a random color (RGB)."""
    return tuple(random.randint(0, 255) for _ in range(3))


def generate_text_image(text, font_path, output_path):
    """
    Generate an image with the given text and ensure it fits fully.

    Args:
        text (str): The text to render.
        font_path (str): Path to the .ttf font file.
        output_path (str): Path to save the generated image.
    """
    # Load the font
    font_size = random.randint(50, 80)  # Randomize font size
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text dimensions
    temp_image = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Create a canvas large enough for the text
    padding = 20  # Add padding around the text
    canvas_width = text_width + padding * 2
    canvas_height = text_height + padding * 2
    image = Image.new("RGB", (canvas_width, canvas_height), random_color())

    # Draw text on the canvas
    draw = ImageDraw.Draw(image)
    fill_color = random_color()
    x, y = padding, padding
    draw.text((x, y), text, font=font, fill=fill_color)

    # Apply random augmentations
    image = apply_augmentations(image)

    # Save the image
    image.save(output_path)



def apply_augmentations(image):
    """Apply random augmentations to an image."""
    if random.random() < 0.4:
        image = image.rotate(random.uniform(-15, 15), expand=False)
    if random.random() < 0.4:
        image = image.filter(ImageFilter.GaussianBlur(random.uniform(0, 2)))
    if random.random() < 0.4:
        image = ImageOps.solarize(image, threshold=random.randint(50, 200))
    if random.random() < 0.4:
        image = ImageOps.invert(image)
    if random.random() < 0.4:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(random.uniform(0.5, 1.5))
    return image


def build_dataset():
    """Build a dataset of text images and metadata."""
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    metadata = []
    for txt_file in os.listdir(TXT_FOLDER):
        if txt_file.endswith(".txt"):
            txt_path = os.path.join(TXT_FOLDER, txt_file)
            with open(txt_path, "r") as f:
                for line in f:
                    text = line.strip()
                    if text:
                        for i in range(50):
                            filename = f"{text.replace(' ', '_')}_{i}.png"
                            output_path = os.path.join(IMAGES_FOLDER, filename)
                            generate_text_image(text, FONT_PATH, output_path)
                            metadata.append({"file_name": filename, "text": text})
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Dataset created with {len(metadata)} entries.")


def normalize_images():
    """Normalize all generated images to a fixed size."""
    os.makedirs(NORMALIZED_FOLDER, exist_ok=True)
    for img_file in os.listdir(IMAGES_FOLDER):
        if img_file.endswith(".png"):
            img_path = os.path.join(IMAGES_FOLDER, img_file)
            img = Image.open(img_path)
            img_resized = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            img_resized.save(os.path.join(NORMALIZED_FOLDER, img_file))
    print(f"All images normalized to {TARGET_SIZE}.")


def load_data(metadata_file, normalized_folder):
    """Load image data and labels for training."""
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    images, labels = [], []
    for entry in metadata:
        img_path = os.path.join(normalized_folder, entry["file_name"])
        if os.path.exists(img_path):
            img = Image.open(img_path).convert("RGB")
            images.append(np.array(img))
            labels.append(entry["text"])
    return np.array(images), np.array(labels)


def create_model(input_shape, num_classes):
    """Create a CNN model for text recognition."""
    model = Sequential([
        Conv2D(64, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def train_model():
    """Train the CNN model."""
    images, labels = load_data(METADATA_FILE, NORMALIZED_FOLDER)
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    labels_categorical = to_categorical(labels_encoded)
    images = images / 255.0
    input_shape = (TARGET_SIZE[1], TARGET_SIZE[0], 3)
    num_classes = len(label_encoder.classes_)
    model = create_model(input_shape, num_classes)
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(
            os.path.join(DATASET_FOLDER, "text_recognition_model.h5"),
            save_best_only=True, monitor='val_loss'
        )
    ]
    device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'
    print(f"Training on: {device}")
    with tf.device(device):
        model.fit(images, labels_categorical, epochs=1000, batch_size=32, validation_split=0.2, callbacks=callbacks)
    with open(os.path.join(DATASET_FOLDER, "label_mapping.json"), "w") as f:
        json.dump(label_encoder.classes_.tolist(), f)
    print("Model trained and saved.")


if __name__ == "__main__":
    build_dataset()
    normalize_images()
    train_model()

3