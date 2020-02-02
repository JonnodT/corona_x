import tensorflow
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np

# To silence the tensorflow warning
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



def load_rawdata():
    data = pd.read_csv("./dataset.csv")
    data = np.asarray(data)
    return data


def normalize_data(data):
    rcnt, ccnt = data.shape
    for i in range(0,rcnt):
        data[i][0] *= 2.5
        data[i][1] = (data[i][1] -35)/7*10
        data[i][2] = data[i][2]*5/12
        for j in range(3, ccnt-1):
            data[i][j] *= 10
    return data


def normalize_array(data):
    data[0][0] *= 2.5
    data[0][1] = (data[0][1] - 35) / 7 * 10
    data[0][2] = data[0][2] * 5 / 12
    for i in range(3,len(data[0])):
        data[0][i] *= 10
    return data


def preprocess(x,y):
    x = tf.cast(x, tf.float32) / 255.0
    y = tf.cast(y, tf.int64)
    return x, y


def create_dataset(mat,y):
    y = tf.cast(y, tf.int64)
    y = tf.one_hot(y, 2)
    return tf.data.Dataset.from_tensor_slices((mat,y)).map(preprocess).shuffle(len(y)).batch(1)


def main():
    data = load_rawdata()
    data = normalize_data(data)
    rcnt, ccnt = data.shape
    train_mat = data[:,0:ccnt-1]
    val_mat = data[:,ccnt-1]
    train_dataset = create_dataset(train_mat, val_mat)
    val_dataset = create_dataset(train_mat,val_mat)
    print(len(data[:, ccnt - 1]))
    model = keras.Sequential([
        keras.layers.Reshape(target_shape=(33,), input_shape=(33,)),
        keras.layers.Dense(units=33, activation='relu'),
        keras.layers.Dense(units=22, activation='relu'),
        keras.layers.Dense(units=15, activation='relu'),
        keras.layers.Dense(units=11, activation='relu'),
        keras.layers.Dense(units=2, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(
        train_dataset.repeat(),
        epochs=10,
        steps_per_epoch=500,
        validation_data=val_dataset.repeat(),
        validation_steps=2,
    )

    model.save('NN.h5')
    print("Saved model to disk")
main()
