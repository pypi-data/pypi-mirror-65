import numpy as np
import tensorflow as tf
from tensorflow.python.keras import layers, regularizers
# from tensorflow.python.keras.backend import _constant_to_tensor, epsilon
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

# from model.rslib.algo.layers.input_layer import Input


def getInput(config):
    maxlen = config['maxlen']
    cross_feature_num = config['cross_feature_num']
    user_feature_num = config['user_feature_num']
    output_unit = config['output_unit']
    seq_num = config['seq_num']
    is_serving = config['is_serving']

    role_id_input = layers.Input(shape=(), dtype='int32', name='role_id_input')
    sequence_id_input = layers.Input(shape=(seq_num, maxlen,), dtype='int32', name='sequence_id_input')
    sequence_time_input = layers.Input(shape=(seq_num, maxlen,), dtype='int32', name='sequence_time_input')
    sequence_time_gaps_input = layers.Input(shape=(seq_num, maxlen,), dtype='int32', name='sequence_time_gaps_input')
    if is_serving:
        cross_feature_indices_input = layers.Input(shape=(None, 2,), dtype='int64', name='cross_feature_indices_input')
        cross_feature_values_input = layers.Input(shape=(None,), dtype='float32', name='cross_feature_values_input')
        cross_feature_indices = layers.Lambda(lambda x: tf.reshape(x, (-1, 2)))(cross_feature_indices_input)
        cross_feature_values = layers.Lambda(lambda x: tf.reshape(x, [-1]))(cross_feature_values_input)
        cross_feature_input = layers.Lambda(lambda x: tf.SparseTensor(indices=x[0], values=x[1], dense_shape=[tf.shape(sequence_id_input)[0], cross_feature_num])) \
            ([cross_feature_indices, cross_feature_values])
    else:
        cross_feature_input = layers.Input(shape=(cross_feature_num,), dtype='float32', sparse=True, name='cross_feature_input')

    user_feature_input = layers.Input(shape=(user_feature_num,), dtype='int32', name='user_feature_input')
    # user_feature_input = Input(tensor=tf.zeros([tf.shape(sequence_id_input)[0], 12], dtype='int32'), name='user_feature_input')

    output_mask_input = layers.Input(shape=(output_unit,), dtype='float32', name='output_mask_input')
    # output_mask_input = layers.Input(shape=(300,), dtype='float32', name='output_mask_input')
    # output_mask_input = layers.Input(tensor=tf.ones([tf.shape(sequence_id_input)[0], 300], dtype='float32'), name='output_mask_input')
    # output_mask_input = Input(tensor=tf.ones([tf.shape(sequence_id_input)[0], 300], dtype='float32'), name='output_mask_input')
    cur_time_input = layers.Input(shape=(), dtype='int32', name='cur_time_input')

    if is_serving:
        return [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, output_mask_input, cur_time_input], \
               [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_indices_input, cross_feature_values_input, user_feature_input, cur_time_input]
    else:
        return [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, output_mask_input, cur_time_input], \
               [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, output_mask_input, cur_time_input]
