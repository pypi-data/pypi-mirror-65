import os
import json
import numpy as np
import tensorflow as tf
from tensorflow_core.python import keras
from tensorflow_core.python.keras import layers, regularizers

from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K

from rslib.algo.layers.interaction import BiInteractionPooling
from .ATRankLayer import ATRankLayer, PositionalEncoding, BuySequence

from ..utils import input_holder
from ..utils.Input_processing import id_input_processing, cross_input_processing, sequence_embedding, sequence_group_embedding, sequence_tar_embedding, id_input_embe_processing
from ..utils.model_compile import compile_model


def get_model(config, return_session=False):
    '''
    get ATRank model
    https://arxiv.org/abs/1711.06632
    :param config:
    :return:
    '''
    activation = 'relu'
    hidden_unit = config['hidden_units']
    output_unit = config['output_unit']
    is_amp = config['is_amp']
    is_serving = config['is_serving']
    output_type = config['output_type']
    hidden_unit = config['hidden_units']
    class_num = config['class_num']
    emb_size = config['emb_size']

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, output_mask_input, cur_time_input], model_input = input_holder.getInput(config)

    user_feature = id_input_processing(user_feature_input, config)
    # user_feature = layers.Dropout(0.5)(user_feature)
    # user_feature = layers.Flatten()(user_feature)

    seq_index_layer = layers.Lambda(lambda x: x[0][:, x[1]])
    seq0 = seq_index_layer([sequence_id_input, 0])
    seq2 = seq_index_layer([sequence_id_input, 2])
    seq3 = seq_index_layer([sequence_id_input, 3])
    time0 = seq_index_layer([sequence_time_input, 0])
    time2 = seq_index_layer([sequence_time_input, 2])
    time3 = seq_index_layer([sequence_time_input, 3])
    seq3, time3, seq4, time4 = BuySequence()(seq3, time3)

    layers_emb_sequence_feature0 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                    embeddings_regularizer=regularizers.l2(0.00005))
    layers_emb_sequence_feature2 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                    embeddings_regularizer=regularizers.l2(0.00005))
    layers_emb_sequence_feature3 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                    embeddings_regularizer=regularizers.l2(0.00005))
    layers_emb_sequence_feature4 = layers.Embedding(input_dim=class_num, output_dim=emb_size,
                                                    embeddings_regularizer=regularizers.l2(0.00005))
    seq0 = layers_emb_sequence_feature0(seq0)
    seq2 = layers_emb_sequence_feature2(seq2)
    seq3 = layers_emb_sequence_feature3(seq3)
    seq4 = layers_emb_sequence_feature4(seq4)
    # time4=time0

    # seq0 = layers.Concatenate(axis=2)([seq0, tf.tile(user_feature[:, tf.newaxis], [1, 32, 1])])
    seq0 = layers.Dense(256, activation='relu',
                        kernel_regularizer=regularizers.l2(0.00005))(seq0)
    mask0 = layers.Lambda(lambda x: tf.tile(tf.cast(tf.sign(time0), dtype=tf.float32)[:, :, tf.newaxis], [1, 1, 256]))(1)
    mask0_sum = layers.Lambda(lambda x: tf.reduce_sum(mask0, axis=1))(1)
    seq0_sum = layers.Lambda(lambda x: tf.reduce_sum(mask0 * seq0, axis=1))(1)
    seq0_mean0 = seq0_sum / mask0_sum

    seq0_max = layers.Lambda(lambda x: tf.reduce_max(seq0, axis=1))(1)
    seq0_min = layers.Lambda(lambda x: tf.reduce_min(seq0, axis=1))(1)
    seq0_mean = layers.Lambda(lambda x: tf.reduce_mean(seq0, axis=1))(1)

    seq0 = layers.Dense(hidden_unit, activation='relu',
                        kernel_regularizer=regularizers.l2(0.00005))(seq0)
    seq2 = layers.Concatenate(axis=2)([seq2,
                                       # tf.tile(seq0_mean[:, tf.newaxis], [1, 32, 1]),
                                       # tf.tile(seq0_max[:, tf.newaxis], [1, 32, 1]),
                                       tf.tile(seq0_mean0[:, tf.newaxis], [1, 32, 1]),
                                       ])
    seq2 = layers.Dense(hidden_unit, activation='relu',
                        kernel_regularizer=regularizers.l2(0.00005))(seq2)
    # seq2 = layers.Dense(hidden_unit, activation='sigmoid')(seq2)
    seq3 = layers.Concatenate(axis=2)([seq3,
                                       # tf.tile(seq0_mean[:, tf.newaxis], [1, 32, 1]),
                                       # tf.tile(seq0_max[:, tf.newaxis], [1, 32, 1]),
                                       tf.tile(seq0_mean0[:, tf.newaxis], [1, 32, 1]),
                                       ])
    seq3 = layers.Dense(hidden_unit, activation='relu',
                        kernel_regularizer=regularizers.l2(0.00005))(seq3)
    # seq3 = layers.Dense(hidden_unit, activation='sigmoid')(seq3)
    seq4 = layers.Concatenate(axis=2)([seq4,
                                       # tf.tile(seq0_mean[:, tf.newaxis], [1, 1, 1]),
                                       # tf.tile(seq0_max[:, tf.newaxis], [1, 1, 1]),
                                       tf.tile(seq0_mean0[:, tf.newaxis], [1, 1, 1]),
                                       ])
    seq4 = layers.Dense(hidden_unit, activation='relu',
                        kernel_regularizer=regularizers.l2(0.00005))(seq4)
    # seq4 = layers.Dense(hidden_unit, activation='sigmoid')(seq4)

    # seq0 = ATRankLayer(config=config, type='encode', name='xx0')(seq0, user_feature, mask=[time0, time0], learning_phase=K.learning_phase())
    # seq2 = ATRankLayer(config=config, type='encode', name='xx2')(seq2, user_feature, mask=[time2, time2], learning_phase=K.learning_phase())
    # seq3 = ATRankLayer(config=config, type='encode', name='xx3')(seq3, user_feature, mask=[time3, time3], learning_phase=K.learning_phase())

    # seq_concat = layers.Concatenate(axis=1)([seq0, seq2, seq3])
    # time_concat = layers.Concatenate(axis=1)([time0, time2, time3])
    seq_concat = layers.Concatenate(axis=1)([seq2, seq3])
    time_concat = layers.Concatenate(axis=1)([time2, time3])

    # seq_concat = seq0
    # time_concat = time0

    att = ATRankLayer(config=config, type='encode', name='xx3')(seq_concat, seq_concat, mask=[time_concat, time_concat], learning_phase=K.learning_phase())

    att_all_seq4 = ATRankLayer(config=config, type='encode', name='yy')(att, seq4, mask=[time_concat, time4], learning_phase=K.learning_phase())

    all_feature = layers.Lambda(lambda x: x[:, 0])(att_all_seq4)

    # pos_target = PositionalEncoding()(dense_group_target)
    # dense_group_target_with_pos = layers.concatenate([dense_group_target, pos_target])

    # all_feature=layers.Concatenate(axis=1)([all_feature,user_feature])

    all_feature = layers.Dense(hidden_unit, activation='relu',
                               kernel_regularizer=regularizers.l2(0.00005))(all_feature)
    # all_feature = layers.Dense(hidden_unit, activation='sigmoid')(all_feature)
    all_feature = layers.Dropout(0.5)(all_feature)
    # all_feature = layers.Dense(hidden_unit, activation='sigmoid')(all_feature)
    # all_feature = layers.Dense(hidden_unit, activation='sigmoid')(all_feature)
    # all_feature = layers.Dropout(0.5)(all_feature)

    output = layers.Dense(output_unit,
                          kernel_regularizer=regularizers.l2(0.00005))(all_feature)

    # if not is_serving:
    # if output_type in ['multi_class', 'multi_label']:
    #     paddings = tf.ones_like(output) * (-2 ** 32 + 1)
    #     output = tf.where(tf.equal(output_mask_input, 0), paddings, output)
    # elif output_type in ['regression', 'multi_regression']:
    #     paddings = tf.zeros_like(output)
    #     output = tf.where(tf.equal(output_mask_input, 0), paddings, output)

    output_layer = {
        'multi_class': tf.nn.softmax,
        'multi_label': tf.sigmoid,
        'regression': lambda x: x,
        'multi_regression': lambda x: x
    }[output_type]
    output = output
    output = output_layer(output)
    model = Model(inputs=model_input, outputs=[output])
    model, sess = compile_model(model, config)

    print(model.summary())
    if return_session:
        return model, sess
    else:
        return model
