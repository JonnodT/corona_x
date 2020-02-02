import tensorflow
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import json


# To silence the tensorflow warning
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



score_table = None

def compute_health_score(data_dict):
    tt = 100

    fever_factor = 0
    if(data_dict['body_temp'] - 37.0 > 0):
        fever_factor = data_dict['body_temp'] - 37.0
    tt -= compute_fever_score(fever_factor)

    sleep_loss = 0
    if(7 - data_dict['sleep_time']  > 0):
        sleep_loss = 7 - data_dict['sleep_time']  > 0
    tt -= compute_sleeploss_score(sleep_loss)

    sym_score_sum = 0
    for sym in data_dict['symptoms']:
        sym_score_sum += score_table[str(sym)]
    tt -= compute_sym_score_sum(sym_score_sum)
    return tt


def compute_sym_score_sum(sum):
    return -0.0091954*sum*sum + 1.645977*sum

def compute_fever_score(fever_factor):
    return -1.25*fever_factor*fever_factor + 10*fever_factor

def compute_sleeploss_score(loss):
    return 0.214*loss*loss - loss/14


def normalize_array(data):
    data[0][0] *= 2.5
    data[0][1] = (data[0][1] - 35) / 7 * 10
    data[0][2] = data[0][2] * 5 / 12
    for i in range(3,len(data[0])):
        data[0][i] *= 10
    return data

def main():
    model = keras.models.load_model('./NN.h5')
    test_arr = np.array([4,37.8,5,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0])[np.newaxis]
    test_arr2 = np.array([2,36.2,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])[np.newaxis]
    test_arr = normalize_array(test_arr)
    test_arr2 = normalize_array(test_arr2)

    print(test_arr)
    print(test_arr2)
    print(tf.data.Dataset.from_tensors(test_arr2))
    print(test_arr2.shape)
    result = model.predict(tf.data.Dataset.from_tensors(test_arr))
    result2 = model.predict(tf.data.Dataset.from_tensors(test_arr2))
    print(result)
    print(result2)
    np.ones(33).shape

main()