from keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D
from keras.models import Sequential
import numpy as np
import pickle

# Height and width of the images (32 x 32)
WIDTH = 32
HEIGHT = 32
# 3 channels: Red, Green, Blue (RGB)
CHANNELS = 3
# Number of classes
NUM_CLASSES = 100


# Function that builds a shadow model.
def build_shadow_model():

    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(WIDTH, HEIGHT, CHANNELS)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())

    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(NUM_CLASSES, activation='softmax'))

    model.summary()

    return model


# Function that builds an attacker model.
# You'll need one attacker model per class.
def build_attack_model():
    model = Sequential()

    # Input - Layer
    model.add(Dense(128, activation="relu", input_shape=(NUM_CLASSES,)))

    # Hidden - Layers
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(64, activation="relu"))

    # Output- Layer
    model.add(Dense(1, activation="sigmoid"))

    model.summary()

    return model

# Input: file with cifar100 images
# Output: two arrays with images and their labels
def load_cifar100_data(filename):

    data = unpickle(filename)

    # get raw images
    images_array = data[b'data']

    # convert image
    images = convert_images(images_array)
    # convert class number to numpy array
    fine_labels = np.array(data[b'fine_labels'])

    return images, fine_labels

# ----- This is a helper fct, no need to use it directly -----
# returns a dictionary with images and labels
def unpickle(file):

    with open(file, 'rb') as fo:
        print("Decoding file: %s" % (file))
        dict = pickle.load(fo, encoding='bytes')

    return dict


# ----- This is a helper fct, no need to use it directly -----
# convert images to numpy arrays
def convert_images(raw_images):

    # convert raw images to numpy array and normalize it
    raw = np.array(raw_images, dtype=float) / 255.0

    # reshape to 4-dimensions - [image_number, channel, height, width]
    images = raw.reshape([-1, CHANNELS, HEIGHT, WIDTH])
    images = images.transpose([0, 2, 3, 1])

    # 4D array - [image_number, height, width, channel]
    return images


# Input: images_<email>.npy file path
# Output: array with 100 images
def load_batch_images(filename):
    images = np.load(filename)
    return images


# Input: labels_<email>.npy file path
# Output: array with 100 labels, corresponding index-wise to the images file
def load_batch_labels(filename):
    labels = np.load(filename)
    return labels




