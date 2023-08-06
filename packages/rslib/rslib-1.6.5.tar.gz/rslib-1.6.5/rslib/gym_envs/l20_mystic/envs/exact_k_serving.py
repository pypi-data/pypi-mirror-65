import os

from tensorflow.python.framework import graph_util
from tensorflow.python.tools import saved_model_utils

from rslib.algo.rl.exact_k.model import Generator
from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask2 import L20RecEnv

os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'

import sys
import json
import collections
import pickle
import param

import os
import time

import tensorflow as tf
from tensorflow.python.keras import layers
from tensorflow.python.keras.models import Model

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants, signature_def_utils_impl

import numpy as np
import pandas as pd

from rslib.utils.datadownload import datadownload
from rslib.utils.date_utils import date_sub
from rslib.utils.exec_hive import exec_hive
from rslib.algo.keras_models import transformer_basic, sparsetransformer_basic, convtransformer_basic, attention_basic

from rslib.algo.keras_models import lstm_basic
from rslib.utils.redis import Redis
from rslib.core.FeatureUtil import FeatureUtil
from rslib.core.MetricsUtil import MetricsUtil
import getopt

if __name__ == '__main__':
    config = param.config
    batch_size = 1
    config['stage'] = 'serving'

    if config['stage'] in ['serving']:
        # env = L20RecEnv(batch_size=batch_size)
        # l1_mask = env.src.l1_mask
        # l2_mask = env.src.l2_mask
        # l3_mask = env.src.l3_mask
        # t0_mask = env.src.t0_mask
        # t1_mask = env.src.t1_mask
        # t2_mask = env.src.t2_mask
        # t3_mask = env.src.t3_mask
        # t4_mask = env.src.t4_mask
        #
        # model = env.controllerobs.model
        #
        # sess = env.controllerobs.sess
        # g1 = sess.graph
        # g1def = g1.as_graph_def()
        # g1def = graph_util.convert_variables_to_constants(
        #     sess,
        #     g1def,
        #     # ,'input_1','input_3','input_4','input_8'
        #     ['input_1', 'input_3', 'input_4', 'input_8', 'input_9','concatenate_2/concat'],
        #     # variable_names_whitelist=None,
        #     # variable_names_blacklist=None
        # )
        #
        # x1 = {('input' + str(i)): model.input[i] for i in range(len(model.input))}
        # xx=model.output
        # tf.saved_model.simple_save(sess,
        #                            "./modellstm",
        #                            inputs=x1,
        #                            outputs={"prediction": xx})

        # import sys
        # sys.exit(0)

        with tf.Graph().as_default() as g2:
            with tf.Session(graph=g2) as sess:
                input_graph_def = saved_model_utils.get_meta_graph_def("./model", tag_constants.SERVING).graph_def
                tf.saved_model.loader.load(sess, [tag_constants.SERVING], "./model")
                g2def = input_graph_def
                g2def = graph_util.convert_variables_to_constants(
                    sess,
                    input_graph_def,
                    ["myOutput"],
                    variable_names_whitelist=None,
                    variable_names_blacklist=None)
                # tf.saved_model.simple_save(sess,
                #                            "./modelbase63",
                #                            inputs=model_input,
                #                            outputs={"prediction": z})

        g1 = tf.Graph()
        with g1.as_default():
            with tf.Session(graph=g1) as sess:
                input_graph_def = saved_model_utils.get_meta_graph_def("./modellstm", tag_constants.SERVING).graph_def
                metagraph = tf.saved_model.loader.load(sess, [tag_constants.SERVING], "./modellstm")
                model_input = dict(metagraph.signature_def['serving_default'].inputs)
                model_output = dict(metagraph.signature_def['serving_default'].outputs)
                # model_input = {k: g1.get_tensor_by_name(v.name) for k, v in model_input.items()}
                model_input = {v.name: g1.get_tensor_by_name(v.name) for k, v in model_input.items()}
                g1def = input_graph_def
                g1def = graph_util.convert_variables_to_constants(
                    sess,
                    input_graph_def,
                    # 'input_1', 'input_3', 'input_4', 'input_8', 'input_9'
                    ["Sigmoid",'input_1', 'input_3', 'input_4', 'input_8', 'input_9'],
                    variable_names_whitelist=None,
                    variable_names_blacklist=None)
                tf.saved_model.simple_save(sess,
                                           "./modelbase62",
                                           inputs=model_input,
                                           outputs={"prediction": g1.get_tensor_by_name('Sigmoid:0')})

                item_cand = np.array([list(range(0, 300))] * batch_size)
                item_cand = tf.convert_to_tensor(item_cand, dtype=tf.int32)
                # concatenate_2+
                hist_emb, = tf.import_graph_def(g1def, input_map=model_input, return_elements=["concatenate_2/concat:0"])
                z, = tf.import_graph_def(g2def, input_map={"GeneratorInfer/item_cand": item_cand, "GeneratorInfer/user": hist_emb}, return_elements=["myOutput:0"])
                tf.identity(z, "prediction")
                graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ["prediction"])
                tf.saved_model.simple_save(sess,
                                           "./modelbase63",
                                           inputs=model_input,
                                           outputs={"prediction": g1.get_tensor_by_name('Sigmoid:0')})
                # g1.get_tensor_by_name('Sigmoid:0')
                tf.saved_model.simple_save(sess,
                                           "./modelbase64",
                                           inputs=model_input,
                                           outputs={"prediction": z})

        # with g1.as_default() as g_combined:
        #     with tf.Session(graph=g_combined) as sess:
        #         item_cand = np.array([list(range(0, 300))] * batch_size)
        #         item_cand = tf.convert_to_tensor(item_cand, dtype=tf.int32)
        #         # concatenate_2+
        #         hist_emb, = tf.import_graph_def(g1def, input_map=model_input, return_elements=["concatenate_2/concat:0"])
        #         z, = tf.import_graph_def(g2def, input_map={"GeneratorInfer/item_cand": item_cand, "GeneratorInfer/user": hist_emb}, return_elements=["myOutput:0"])
        #         tf.identity(z, "prediction")
        #         graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ["prediction"])
        #         tf.saved_model.simple_save(sess,
        #                                    "./modelbase62",
        #                                    inputs=model_input,
        #                                    outputs={"prediction": g1.get_tensor_by_name('Sigmoid:0')})
        #         # g1.get_tensor_by_name('Sigmoid:0')
        #         tf.saved_model.simple_save(sess,
        #                                    "./modelbase64",
        #                                    inputs=model_input,
        #                                    outputs={"prediction": z})

        # region load model
        # with tf.name_scope('Generator'):
        #     g = Generator(l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, is_training=True, user=hist_emb, item_cand=item_cand)
        #     # g = Generator(l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, is_training=True)
        # print(len(tf.get_variable_scope().global_variables()))
        #
        # tf.get_variable_scope().reuse_variables()
        # with tf.name_scope('GeneratorInfer'):
        #     g_infer = Generator(l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, is_training=False, user=hist_emb, item_cand=item_cand)
        #     # g_infer = Generator(l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, is_training=False)
        #
        # saver = tf.train.Saver()
        # sess = env.controllerobs.sess
        # saver.restore(sess, 'model_file')
        # endregion

        # print('outputs: ', [output.op.name for output in model.outputs])
        # x = {('input' + str(i)): model.input[i] for i in range(len(model.input))}
        # y = {"prediction": g_infer.infer_result}

        # prediction_signature = tf.saved_model.signature_def_utils.predict_signature_def(x, y)
        # valid_prediction_signature = tf.saved_model.signature_def_utils.is_valid_signature(prediction_signature)
        # if (valid_prediction_signature == False):
        #     raise ValueError("Error: Prediction signature not valid!")
        #
        # model_serving_file = 'model_saved'
        # os.system('rm -rf %s' % model_serving_file)
        # builder = saved_model_builder.SavedModelBuilder(model_serving_file)
        # # legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
        # builder.add_meta_graph_and_variables(
        #     tf.keras.backend.get_session(), [tag_constants.SERVING],
        #     signature_def_map={
        #         signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature,
        #     })
        # builder.save()
