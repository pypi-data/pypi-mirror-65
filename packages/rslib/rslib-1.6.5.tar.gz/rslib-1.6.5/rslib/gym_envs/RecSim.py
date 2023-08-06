from . import RecEnvSrc
import numpy as np
import traceback
import tensorflow as tf


class RecSim(object):
    """ Implements core recommendation simulator"""

    def __init__(self, recEnvSrc: RecEnvSrc, model, modelfile, steps=9, batch_size=None):
        # invariant for object life
        self.recEnvSrc = recEnvSrc
        self.steps = steps
        self.step = 0
        self.batch_size = batch_size
        self.states = np.zeros([self.steps, self.batch_size]) if batch_size else np.zeros(self.steps)
        self.actions = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)
        self.layers = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)
        self.paytypes = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)

        self.dones = np.zeros([self.steps, self.batch_size], dtype=int)
        self.probs = [[] for _ in range(self.steps)] if self.batch_size else []
        self.gmv = np.ones([self.steps, self.batch_size]) if self.batch_size else np.ones(self.steps)
        self.model = model
        # self.model.load_weights(modelfile)
        saver = tf.train.Saver()
        sess = tf.keras.backend.get_session()
        saver.restore(sess, modelfile)
        self.final_layer_model = tf.keras.backend.function(self.model.input, self.model.get_layer('tf_op_layer_Softmax').output)
        self.reset()

    def reset(self):
        self.step = 0
        self.actions.fill(-1)
        self.layers.fill(0)
        self.paytypes.fill(0)
        self.dones.fill(0)

        self.probs = [[] for _ in range(self.steps)] if self.batch_size else []
        self.states.fill(None)
        self.gmv.fill(0)

    def predict(self, model, feat):
        prob = model.predict(feat)[0][0]
        self.probs.append(prob)
        return prob

    def predict_all(self, model, feat, session):
        with session.as_default():
            with session.graph.as_default():
                try:
                    # res = model.predict(feat)
                    res = self.final_layer_model(feat)
                except:
                    feat
                    traceback.print_exc()
                    1

        self.probs = [r[1] for r in res]
        return self.probs

    def get_init_info(self):
        reward = [0] * self.batch_size if self.batch_size else 0
        gmv = self.gmv[self.step] if self.batch_size else self.gmv[self.step]
        actions = self.actions
        layers = self.layers
        paytypes = self.paytypes
        return {'reward': reward, 'gmv': gmv, 'actions': actions, 'layers': layers, 'paytypes': paytypes}

    def _step(self, rawstate, action, info):
        """ Given an action and return for prior period, calculates costs, navs,
            etc and returns the reward and a  summary of the day's activity. """

        self.actions[self.step] = action
        info['actions'] = self.actions
        new_rawstate = self.recEnvSrc.get_new_user_rawstate(rawstate, info)

        if self.step < self.steps - 1:
            reward = 0
            done = 0
        else:
            reward = 1
            done = 1

        info = {'reward': reward, 'gmv': self.gmv[self.step], 'actions': self.actions}

        self.step += 1

        return new_rawstate, reward, done, info
