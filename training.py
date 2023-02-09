import tensorboard
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import reciprocal
import time
import os

root_log = os.path.join(os.curdir, 'tensorboard_logs')

def get_sub():
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_log, run_id)

def get_data():
    #download data from keras
    mnist = keras.datasets.mnist
    (x_train_full, y_train_full), (x_test, y_test) = mnist.load_data()

    #scale down data
    x_train_full = x_train_full / 255.0
    x_test = x_test / 255.0

    return x_train_full, y_train_full, x_test, y_test

#build neural network
def build(hidden=1, neurons=30, learning_rate=3e-3, input_shape=[28, 28]):
    model = keras.models.Sequential()

    model.add(keras.layers.Flatten(input_shape=input_shape)) #input layer
    
    for layer in range(hidden): #build hidden layers
        model.add(keras.layers.Dense(neurons, activation='relu'))
    
    model.add(keras.layers.Dense(10, activation='softmax')) #output layers
    
    #compille with gradient decent and categorical accuracy
    optimizer = keras.optimizers.SGD(learning_rate)
    model.compile(loss=keras.losses.SparseCategoricalCrossentropy(), optimizer=optimizer, metrics=['accuracy'])
    return model

def train(model, X, Y, dir):
    callback = keras.callbacks.TensorBoard(dir)
    history = model.fit(X, Y, batch_size=64 ,epochs=10, validation_split=0.1, callbacks=[callback])
    return history
    
def eval(model, X, Y):
    results = model.evaluate(X, Y, batch_size=128)
    return results

X_Tr, Y_Tr, X_t, Y_t = get_data()
dir = get_sub()

