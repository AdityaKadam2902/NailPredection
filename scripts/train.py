#!/usr/bin/env python3
"""Train VGG-16 nail disease classifier.

Requires Python 3.12 + TensorFlow for real training.
On Python 3.14+, this script provides instructions.
"""

import os
import sys
import argparse
import json


def check_tensorflow():
    try:
        import tensorflow as tf
        return True
    except ImportError:
        return False


def train_real(data_dir, epochs, batch_size):
    """Real training with TensorFlow."""
    import numpy as np
    from tensorflow.keras.applications import VGG16
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    CLASS_LABELS = [
        "Darier's disease", "Muehrcke's lines", "Alopecia areata", "Beau's lines",
        "Bluish nail", "Clubbing", "Eczema", "Half and half nails (Lindsay's nails)",
        "Koilonychia", "Leukonychia", "Onycholysis", "Pale nail", "Red lunula",
        "Splinter hemorrhage", "Terry's nail", "White nail", "Yellow nails",
    ]

    # Build model
    base = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    for layer in base.layers:
        layer.trainable = False
    for layer in base.layers[-4:]:
        layer.trainable = True

    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.3)(x)
    out = Dense(17, activation="softmax")(x)

    model = Model(inputs=base.input, outputs=out)
    model.compile(optimizer=Adam(1e-4), loss="categorical_crossentropy", metrics=["accuracy"])

    # Data generators
    train_gen = ImageDataGenerator(
        rescale=1./255, rotation_range=20, width_shift_range=0.1,
        height_shift_range=0.1, zoom_range=0.1, horizontal_flip=True
    ).flow_from_directory(os.path.join(data_dir, "train"), target_size=(224, 224), batch_size=batch_size, class_mode="categorical", classes=CLASS_LABELS)

    val_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
        os.path.join(data_dir, "test"), target_size=(224, 224), batch_size=batch_size, class_mode="categorical", classes=CLASS_LABELS, shuffle=False
    )

    callbacks = [
        ModelCheckpoint("models/best_model.h5", monitor="val_accuracy", save_best_only=True),
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-7),
    ]

    print(f"Training on {train_gen.samples} images...")
    model.fit(train_gen, epochs=epochs, validation_data=val_gen, callbacks=callbacks)

    model.save("models/vgg-16-nail-disease.h5")
    with open("models/class_labels.json", "w", encoding="utf-8") as f:
        json.dump(CLASS_LABELS, f, indent=2)
    print("\nModel saved to models/vgg-16-nail-disease.h5")
    print("Class labels saved to models/class_labels.json")
    print("Copy to app/static/models/ for production use")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data", help="Data directory")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    if not check_tensorflow():
        print("="*60)
        print("TensorFlow not installed!")
        print("="*60)
        print("\nTo train a real model, you need Python 3.12 + TensorFlow:")
        print("  1. Install Python 3.12 from python.org")
        print("  2. python3.12 -m venv venv")
        print("  3. pip install tensorflow>=2.16.0")
        print("  4. python scripts/train.py")
        print("\nThe app currently runs in MOCK mode for demo purposes.")
        print("="*60)
        return

    os.makedirs("models", exist_ok=True)
    train_real(args.data, args.epochs, args.batch_size)


if __name__ == "__main__":
    main()
