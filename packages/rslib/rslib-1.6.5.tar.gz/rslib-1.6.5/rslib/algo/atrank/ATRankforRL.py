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

    # todo，支持定制的输入格式
    input_list = []

    [role_id_input, sequence_id_input, sequence_time_input, sequence_time_gaps_input, cross_feature_input, user_feature_input, output_mask_input, cur_time_input], model_input = input_holder.getInput(config)

    user_feature = id_input_embe_processing(user_feature_input, config)
    user_time = layers.Lambda(lambda x: tf.ones_like(user_feature_input))(1)
    seq0, time0 = sequence_tar_embedding(sequence_id_input, sequence_time_input, config, target_seq=[0])
    seq2, time2 = sequence_tar_embedding(sequence_id_input, sequence_time_input, config, target_seq=[2])
    seq3, time3 = sequence_tar_embedding(sequence_id_input, sequence_time_input, config, target_seq=[3])

    seq3, time3, seq4, time4 = BuySequence()(seq3, time3)

    att_seq0_user = ATRankLayer(config=config, type='encode', name='xx1')(seq0, user_feature, mask=[time0, user_time], learning_phase=K.learning_phase())

    att_seq2_seq2 = ATRankLayer(config=config, type='encode', name='xx2')(seq2, user_feature, mask=[time2, user_time], learning_phase=K.learning_phase())
    att_seq3_seq3 = ATRankLayer(config=config, type='encode', name='xx3')(seq3, user_feature, mask=[time3, user_time], learning_phase=K.learning_phase())

    seq_concat = layers.Concatenate(axis=1)([att_seq0_user, att_seq2_seq2, att_seq3_seq3])
    time_concat = layers.Concatenate(axis=1)([user_time, user_time, user_time])

    att_all_seq4 = ATRankLayer(config=config, type='encode', name='yy')(seq_concat, seq4, mask=[time_concat, time4], learning_phase=K.learning_phase())

    all_feature = layers.Lambda(lambda x: x[:, 0])(att_all_seq4)

    # pos_target = PositionalEncoding()(dense_group_target)
    # dense_group_target_with_pos = layers.concatenate([dense_group_target, pos_target])

    all_feature = layers.Dense(hidden_unit * 4, activation='relu')(all_feature)
    all_feature = layers.Dropout(0.2)(all_feature)
    all_feature = layers.Dense(hidden_unit * 4, activation='relu')(all_feature)
    all_feature = layers.Dropout(0.2)(all_feature)

    output = layers.Dense(output_unit)(all_feature)

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
