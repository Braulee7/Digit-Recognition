import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import reciprocal
import time
import os

keras = tf.keras
root_log = os.path.join(os.curdir, 'tensorboard_logs')

def get_sub():
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_log, run_id)

def get_data():
    #download data from keras
    mnist = keras.datasets.mnist
    (x_train_full, y_train_full), (x_test, y_test) = mnist.load_data()

    #scale down data
    x_valid, x_train  = x_train_full[:5000] / 255.0, x_train_full[5000:] / 255.0
    y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
    x_test = x_test 

    return x_train_full, y_train_full, x_valid, y_valid, x_test, y_test

#build neural network
def build(hidden=1, neurons=30, learning_rate=3e-3, input_shape=[28, 28]):
    model = keras.models.Sequential()

    model.add(keras.layers.Flatten(input_shape=input_shape)) #input layer
    
    for layer in range(hidden): #build hidden layers
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dense(neurons, activation='relu', kernel_initializer="he_normal"))
    
    model.add(keras.layers.Dense(10, activation='softmax')) #output layers
    
    #compille with gradient decent and categorical accuracy
    optimizer = keras.optimizers.SGD(learning_rate)
    model.compile(loss=keras.losses.SparseCategoricalCrossentropy(), optimizer=optimizer, metrics=['accuracy'])
    return model

def train(model, X, Y, dir):
    callback = keras.callbacks.TensorBoard(dir)
    history = model.fit(X, Y, batch_size=32 ,epochs=15, validation_split=0.1, callbacks=[callback, keras.callbacks.EarlyStopping(patience=10)])
    return history
    
def eval(model, X, Y):
    results = model.evaluate(X, Y, batch_size=128)
    return results

def tune(X, Y, X_v, Y_v, dir):
    reg = keras.wrappers.scikit_learn.KerasRegressor(build)

    params = {
        'hidden': [0, 1, 2, 3],
        'neurons': np.arange(1, 100),
        'learning_rate': reciprocal(3e-4, 3e-2),
    }
    callback = keras.callbacks.TensorBoard(dir)


    rnd_search = RandomizedSearchCV(reg, params, n_iter=10, cv=3)
    rnd_search.fit(X, Y, epochs=100, validation_data=(X_v, Y_v), callbacks = [callback, keras.callbacks.EarlyStopping(patience=10)])

    print(rnd_search.best_params_)

    return rnd_search.best_estimator_.model

X_Tr, Y_Tr, X_v, Y_v, X_t, Y_t = get_data()
dir = get_sub()

#{'hidden': 3, 'learning_rate': 0.0033331276482504637, 'neurons': 25}
#model = build(hidden=1, learning_rate=0.0033331276482504637, neurons=25)

#hist = train(model, X_Tr, Y_Tr, dir)

model = keras.models.load_model('hypertuned.h5')

results = eval(model, X_t, Y_t)

print('loss, acc', results)
print(X_t[3].shape)
img = np.reshape(X_t[9], (-1, 28, 28))

prediction = model.predict(img)
# plt.imshow(img.reshape(28, 28), cmap=plt.cm.binary)
# plt.title(np.argmax(prediction[0], axis=0))
# plt.show()
print(img)



model.save('hypertuned_best_params.h5')





