import os
import numpy as np
import librosa
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Config
DATASET_PATH = "dataset" # Structure: dataset/distress, dataset/normal
MODEL_SAVE_PATH = "distress_model.h5"
TFLITE_MODEL_PATH = "distress_model.tflite"

# Audio Config
SAMPLE_RATE = 16000
DURATION = 1 # seconds
SAMPLES = SAMPLE_RATE * DURATION
NUM_MFCC = 13
HOP_LENGTH = 512
N_FFT = 2048

def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)
        # Pad if short
        if len(audio) < SAMPLES:
            audio = np.pad(audio, (0, SAMPLES - len(audio)))
        else:
            audio = audio[:SAMPLES]
            
        mfcc = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=NUM_MFCC, n_fft=N_FFT, hop_length=HOP_LENGTH)
        # Transpose to shape (Time, MFCC)
        return mfcc.T
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def load_data():
    X = []
    y = []
    
    classes = {"normal": 0, "distress": 1}
    
    for label, class_id in classes.items():
        dir_path = os.path.join(DATASET_PATH, label)
        if not os.path.exists(dir_path):
            print(f"Dataset directory not found: {dir_path}. Please create it and add .wav files.")
            continue
            
        print(f"Loading {label}...")
        for file in os.listdir(dir_path):
            if file.endswith(".wav"):
                feat = extract_features(os.path.join(dir_path, file))
                if feat is not None:
                    X.append(feat)
                    y.append(class_id)
                    
    return np.array(X), np.array(y)

def create_model(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        # CNN for Spectrogram/MFCC
        tf.keras.layers.Reshape((input_shape[0], input_shape[1], 1)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid') # Binary Classification
    ])
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    if not os.path.exists(DATASET_PATH):
        os.makedirs(os.path.join(DATASET_PATH, "distress"))
        os.makedirs(os.path.join(DATASET_PATH, "normal"))
        print(f"Created {DATASET_PATH} folders. Please add .wav files and run again.")
        return

    print("Loading Dataset...")
    X, y = load_data()
    
    if len(X) == 0:
        print("No data found! Please add .wav files to dataset/normal and dataset/distress.")
        return

    print(f"Data Shape: {X.shape}")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    input_shape = (X.shape[1], X.shape[2]) # (Time, MFCC)
    model = create_model(input_shape)
    model.summary()
    
    print("Training...")
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))
    
    print("Saving Model...")
    model.save(MODEL_SAVE_PATH)
    
    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    with open(TFLITE_MODEL_PATH, "wb") as f:
        f.write(tflite_model)
        
    print(f"Done! {TFLITE_MODEL_PATH} created. Copy this to your Android assets folder.")

if __name__ == "__main__":
    main()
