# -*- coding: utf-8 -*-
"""IBAC1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14F6Pr2JsSqz0QSDTRAd2_HJsx5eAhN5c

MOUNT GOOGLE **DRIVE**
"""

# Mount Google Drive
from google.colab import drive
drive.mount("/content/Drive", force_remount = True)

"""**IMPORTS**"""

from tensorflow import keras
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras import optimizers, losses
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing import image

import os
import shutil
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

from sklearn.metrics import classification_report

import warnings
warnings.filterwarnings("ignore")

"""DATA PREPARATION



"""

# Unzip data to runtime
!unzip "./Drive/MyDrive/Disaster/damage.zip" -d "./"

# Base Path for all files
data_dir = './damage'

# Using ImageDataGenerator to load the Images for Training and Testing the CNN Model
datagenerator = {
    "train": ImageDataGenerator(
        horizontal_flip=True,
        vertical_flip=True,
        rescale=1. / 255,
        validation_split=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        width_shift_range=0.1,
        height_shift_range=0.1,
        rotation_range=30
    ).flow_from_directory(
        directory=data_dir,
        target_size=(300, 300),
        subset='training'
    ),

    "valid": ImageDataGenerator(
        rescale=1 / 255,
        validation_split=0.1
    ).flow_from_directory(
        directory=data_dir,
        target_size=(300, 300),
        subset='validation'
    )
}

"""BUILDING XCEPTION MODEL

Initializing Base Model
"""

# Initializing Xception (pretrained) model with input image shape as (300, 300, 3)
base_model = Xception(
    weights="imagenet",
    include_top=False,
    input_shape=(300, 300, 3)
)

# Setting the Training of all layers of Xception model to True
base_model.trainable = True

"""Adding More Layers"""

# Adding some more layers at the end of the Model as per our requirement
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.15),
    Dense(1024, activation='relu'),
    Dense(4, activation='softmax') # 2 Output Neurons for 2 Classes
])

"""Adam Optimizer"""

# Using the Adam Optimizer to set the learning rate of our final model
opt = optimizers.Adam(learning_rate = 1e-4)

# Compiling and setting the parameters we want our model to use
model.compile(
    loss="categorical_crossentropy",
    optimizer=opt,
    metrics=['accuracy']
)

# Viewing the summary of the model
model.summary()

"""Separation Train and Test Data"""

# Setting variables for the model
batch_size = 64
epochs = 10

# Seperating Training and Testing Data
train_generator = datagenerator["train"]
valid_generator = datagenerator["valid"]

for i in os.listdir("/content/damage/"):
  print(len(os.listdir("/content/damage/" + i)))

!rm -rf "/content/CNN-Models"

# Calculating variables for the model
steps_per_epoch = train_generator.n // batch_size
validation_steps = valid_generator.n // batch_size

print("steps_per_epoch :", steps_per_epoch)
print("validation_steps :", validation_steps)

"""Training Model"""

# Training the Model
history = model.fit_generator(
    generator=train_generator,
    epochs=epochs,
    steps_per_epoch=steps_per_epoch,
    validation_data=valid_generator,
    validation_steps=validation_steps,
)

print(history.history.keys())

history_df = pd.DataFrame.from_dict(history.history)
history_df

sns.lineplot(x = history_df.index, y = history_df.accuracy)
sns.lineplot(x = history_df.index, y = history_df.loss)
plt.show()