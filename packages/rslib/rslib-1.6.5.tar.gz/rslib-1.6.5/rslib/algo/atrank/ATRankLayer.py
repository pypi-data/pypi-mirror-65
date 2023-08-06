#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
Transformer

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

from .contrib import *
# import tensorflow_core as tf
from tensorflow.python.keras import backend as K


class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, num_units=16, **kwargs):
        self.supports_masking = False
        self.num_units = num_units
        super(PositionalEncoding, self).__init__()

    def call(self, inputs):
        position = positional_encoding(inputs, num_units=16)
        return position

    # def compute_output_shape(self, input_shape):
    #     return (input_shape[0][0],input_shape[0][1])

    def compute_mask(self, input, input_mask=None):
        # need not to pass the mask to next layers
        return None


class ATRankLayer(tf.keras.layers.Layer):
    """
    layer used for dealing sequence feature in ATRank model
    """

    def __init__(self, config, name, type='encode', **kwargs):
        self.supports_masking = False
        self.config = config
        self.namee = name
        self.type = type
        super(ATRankLayer, self).__init__()

    def call(self, h_emb, i_emb, mask=None, learning_phase=0):
        # i_emb = i_emb[:, 0]
        # i_b = i_b[:, 0]
        mask = [tf.cast(mask[0], tf.float32), tf.cast(mask[1], tf.float32)]
        learning_phase = tf.cast(learning_phase, tf.bool)

        num_blocks = self.config['atrank_num_blocks']
        num_heads = self.config['atrank_num_heads']
        dropout_rate = self.config['atrank_dropout_rate']
        num_units = h_emb.get_shape().as_list()[-1]

        # 序列模型
        if self.type == 'encode':
            u_emb, stt = attention_net(h_emb, i_emb, num_units, num_heads, num_blocks, learning_phase, dropout_rate, self.namee, False, mask)
        elif self.type == 'decode':
            u_emb, att = attention_net(h_emb, i_emb, num_units, num_heads, num_blocks, learning_phase, dropout_rate, self.namee, False, mask)
        else:
            # u_emb, att = attention_net2(h_emb, i_emb, num_units, num_heads, num_blocks, learning_phase, dropout_rate, 'decode', False, mask)
            h_emb, stt = attention_net(h_emb, h_emb, num_units, num_heads, num_blocks, learning_phase, dropout_rate, self.namee+'encode', False, [mask[0], mask[0]])
            u_emb, att = attention_net(h_emb, i_emb, num_units, num_heads, num_blocks, learning_phase, dropout_rate, self.namee+'decode', False, mask)

        return u_emb

    # def compute_output_shape(self, input_shape):
    #     return (input_shape[0][0],input_shape[0][1])

    def compute_mask(self, input, input_mask=None):
        # need not to pass the mask to next layers
        return None


def attention_net(enc, dec, num_units, num_heads, num_blocks, learning_phase, dropout_rate, name, reuse, mask):
    with tf.variable_scope(name, reuse=reuse):
        for i in range(num_blocks):
            with tf.variable_scope("num_blocks_{}".format(i)):
                ### Multihead Attention
                xx, stt_vec = multihead_attention(
                    keys=enc,
                    queries=dec,
                    num_units=num_units,
                    num_heads=num_heads,
                    is_training=learning_phase,
                    dropout_rate=dropout_rate,
                    mask=mask,
                    scope="attention"
                )

                ### Feed Forward
                xx = feedforward(xx,
                                 num_units=[num_units // 4, num_units],
                                 scope="feed_forward",
                                 reuse=reuse)
    return xx, stt_vec


def attention_net2(enc, dec, num_units, num_heads, num_blocks, learning_phase, dropout_rate, name, reuse, mask):
    with tf.variable_scope('encode', reuse=reuse):
        for i in range(num_blocks):
            with tf.variable_scope("num_blocks_{}".format(i)):
                ### Multihead Attention
                enc, stt_vec = multihead_attention(
                    keys=enc,
                    queries=enc,
                    num_units=num_units,
                    num_heads=num_heads,
                    is_training=learning_phase,
                    dropout_rate=dropout_rate,
                    mask=[mask[0], mask[0]],
                    scope="attention"
                )

                ### Feed Forward
                enc = feedforward(enc,
                                  num_units=[num_units // 4, num_units],
                                  scope="feed_forward",
                                  reuse=reuse)
    with tf.variable_scope('decode', reuse=reuse):
        for i in range(num_blocks):
            with tf.variable_scope("num_blocks_{}".format(i)):
                ### Multihead Attention
                dec, att_vec = multihead_attention(
                    keys=enc,
                    queries=dec,
                    num_units=num_units,
                    num_heads=num_heads,
                    is_training=learning_phase,
                    dropout_rate=dropout_rate,
                    mask=mask,
                    scope="attention"
                )

                ### Feed Forward
                dec = feedforward(dec,
                                  num_units=[num_units // 4, num_units],
                                  scope="feed_forward",
                                  reuse=reuse)
    return dec, stt_vec


class BuySequence(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(BuySequence, self).__init__()

    def call(self, seq3, time3):
        mask = time3
        match_indices = tf.where(  # [[5, 5, 2, 5, 4],
            tf.equal(0, mask),  # [0, 5, 2, 3, 5],
            x=tf.range(tf.shape(mask)[1]) * tf.ones_like(mask),  # [5, 1, 5, 5, 5]]
            y=(tf.shape(mask)[1]) * tf.ones_like(mask))
        seq_len = tf.reduce_min(match_indices, axis=1)

        indices = tf.stack([tf.range(tf.shape(mask)[0]), seq_len-1], axis=1)
        indices = tf.cast(indices, dtype=tf.int64)
        updates = tf.ones([tf.shape(mask)[0]], dtype=tf.int32)
        shape = tf.cast(tf.shape(mask)[0:2], dtype=tf.int64)
        mask_zero = tf.scatter_nd(indices, updates, shape)
        mask_zero = -1 * (mask_zero - 1)
        time3 = mask_zero * mask

        # indices = tf.stack([tf.range(tf.shape(mask)[0]), seq_len], axis=1)
        # updates = tf.zeros([tf.shape(mask)[0]])
        # time3 = tf.scatter_nd_update(time3, indices, updates)

        indices = indices[:, tf.newaxis]
        seq4 = tf.gather_nd(seq3, indices)
        time4 = tf.ones([tf.shape(seq3)[0], 1])

        return seq3, time3, seq4, time4

    # def compute_output_shape(self, input_shape):
    #     return (input_shape[0][0],input_shape[0][1])

    def compute_mask(self, input, input_mask=None):
        # need not to pass the mask to next layers
        return None
