import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt
from DataPreperation import Prepare





class Model():
    def __init__(self) -> None:
        self.model = keras.models.load_model(
        'hypertuned_best_params.h5',
        custom_objects=None, compile=False)

        optimizer = keras.optimizers.SGD(0.0033331276482504637)
        self.model.compile(loss=keras.losses.SparseCategoricalCrossentropy(), optimizer=optimizer, metrics=['accuracy'])

    def Predict(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        data = Prepare(img)
        img_prepared = data.getGrayScale()
        prediction = self.model.predict(img_prepared)
        print(img_prepared.reshape(28, 28))
        # plt.imshow(img_prepared.reshape(28, 28), cmap=plt.cm.binary)
        # plt.title(np.argmax(prediction[0], axis=0))
        # plt.show()
        return np.argmax(prediction[0], axis=0)



