import os
import json
from PIL import Image, ImageOps, ImageEnhance
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import CSVLogger, EarlyStopping
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Paths
TXT_FOLDER = "texts"
DATASET_FOLDER = "datasets/text"
IMAGES_FOLDER = os.path.join(DATASET_FOLDER, "images")
METADATA_FILE = os.path.join(DATASET_FOLDER, "metadata.json")
FONT_PATH = "fonts/LuckiestGuy-Regular.ttf"
NORMALIZED_FOLDER = os.path.join(DATASET_FOLDER, "normalized_images")
MODEL_PATH = os.path.join(DATASET_FOLDER, "text_recognition_model.h5")
LABEL_MAPPING_PATH = os.path.join(DATASET_FOLDER, "label_mapping.json")
TRAINING_LOG_PATH = os.path.join(DATASET_FOLDER, "training_log.csv")
CHECKPOINT_PATH = os.path.join(DATASET_FOLDER, "training_checkpoint.json")
TARGET_SIZE = (256, 64)  # Width, Height for normalization

# Image settings
IMAGE_WIDTH, IMAGE_HEIGHT = TARGET_SIZE


def preprocess_image(image_path):
    """Convert non-black colors to white."""
    image = Image.open(image_path).convert("RGB")
    np_image = np.array(image)
    mask = (np_image[:, :, 0] > 30) | (np_image[:, :, 1] > 30) | (np_image[:, :, 2] > 30)
    np_image[mask] = [255, 255, 255]
    return np_image


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


def load_checkpoint():
    """Load the training checkpoint."""
    if os.path.exists(CHECKPOINT_PATH):
        with open(CHECKPOINT_PATH, "r") as f:
            return json.load(f)
    return None


def save_checkpoint(epoch):
    """Save the current training checkpoint."""
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump({"epoch": epoch}, f)


def train_model(save_every=10):
    """Train the CNN model with customizable save frequency and resume capabilities."""
    # Load metadata and preprocess images
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    images, labels = [], []
    for entry in metadata:
        img_path = os.path.join(NORMALIZED_FOLDER, entry["file_name"])
        if os.path.exists(img_path):
            img = preprocess_image(img_path)
            img = Image.fromarray(img).resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            images.append(np.array(img) / 255.0)
            labels.append(entry["text"])

    images, labels = np.array(images), np.array(labels)
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    labels_categorical = to_categorical(labels_encoded)

    input_shape = (TARGET_SIZE[1], TARGET_SIZE[0], 3)
    num_classes = len(label_encoder.classes_)

    # Load the model if resuming, otherwise create a new one
    checkpoint = load_checkpoint()
    start_epoch = 0
    if checkpoint and os.path.exists(MODEL_PATH):
        print(f"Resuming training from epoch {checkpoint['epoch'] + 1}...")
        model = load_model(MODEL_PATH)
        start_epoch = checkpoint['epoch']
    else:
        print("Starting training from scratch...")
        model = create_model(input_shape, num_classes)

    # Save the label mapping
    with open(LABEL_MAPPING_PATH, "w") as f:
        json.dump(label_encoder.classes_.tolist(), f)

    # Callbacks
    csv_logger = CSVLogger(TRAINING_LOG_PATH, append=True)
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Custom training loop to save model at defined intervals
    for epoch in range(start_epoch, 1000):
        print(f"Epoch {epoch + 1}/1000")
        history = model.fit(
            images, labels_categorical,
            initial_epoch=epoch,
            epochs=epoch + 1,
            batch_size=32,
            validation_split=0.2,
            callbacks=[csv_logger, early_stopping],
            verbose=1
        )
        if (epoch + 1) % save_every == 0:
            model.save(MODEL_PATH)
            save_checkpoint(epoch + 1)
            print(f"Model saved at epoch {epoch + 1}.")
        if early_stopping.stopped_epoch > 0:  # Stop if early stopping is triggered
            print("Early stopping triggered. Training completed.")
            break

    # Final save
    model.save(MODEL_PATH)
    save_checkpoint(1000)
    print("Training completed. Model saved.")


if __name__ == "__main__":
    # Check if training is complete
    checkpoint = load_checkpoint()
    if checkpoint and checkpoint.get("epoch") == 1000:
        response = input("Training is already complete. Do you want to retrain the model? (y/n): ").strip().lower()
        if response != 'y':
            print("Exiting training script.")
            exit()

    train_model(save_every=10)
