import gym
from gym import error, spaces, utils
from gym.utils import seeding
from collections import Counter
import tensorflow as tf
# from tensorflow import keras
import numpy as np
from numpy import random
import pandas as pd
import logging

# from RL_brain import PolicyGradient
from rslib.core.FeatureUtil import FeatureUtil
import random
import numpy as np
from rslib.gym_envs.RecEnvSrc import RecEnvSrc
from rslib.gym_envs.RecSim import RecSim
from rslib.gym_envs.l20_mystic.Policy_gradient_softmax.RL_brain import PolicyGradient


class controllerObs(object):
    def __init__(self, config, model, modelfile):
        self.config = config
        self.FeatureUtil = FeatureUtil(config)
        self.model = model
        self.model.load_weights(modelfile)
        item_emb1 = self.model.get_layer('embedding_2').get_weights()[0]
        item_emb2 = self.model.get_layer('embedding_3').get_weights()[0]
        self.item_embs = [item_emb1, item_emb2]

    def get_item_emb(self, itemid):
        if int(itemid) >= 0:
            emb = np.array([x[int(itemid)] for x in self.item_embs])
            return np.max(emb, axis=0)
        else:
            return np.zeros(len(self.item_embs[0][0]))

    def keras_emb(self, rawstate):
        mid_layer_model = tf.keras.Model(inputs=self.model.input,
                                         outputs=self.model.get_layer('concatenate_2').output)
        feat = self.FeatureUtil.feature_extraction([rawstate], predict=True)
        mid_layer_output = mid_layer_model.predict(feat)
        return mid_layer_output[0]

    def rawstate2obs(self, rawstate, info,step):
        if step==0:
            self.hist_emb = self.keras_emb(rawstate)
        item_embs = []
        for itemid in info['actions']:
            item_embs.append(self.get_item_emb(itemid))

        item_emb = np.max(item_embs, axis=0)
        return np.concatenate((self.hist_emb, item_emb))

    def get_obs(self, new_rawstate, info, step):
        obs = self.rawstate2obs(new_rawstate, info,step)
        return obs


class L20RecEnvSrc(RecEnvSrc):
    def __init__(self, config, statefile, actionfile):
        RecEnvSrc.__init__(self, config, statefile, actionfile)

    def get_user_rawstate(self, role_id):
        rawstate = self.state_dict[str(role_id)]
        seq_feat = rawstate.split('@')[2].split(';')
        seq_feat_init = ';'.join([seq_feat[0], seq_feat[1], '0:0', '0:0'])
        rawstate = '@'.join(rawstate.split('@')[:2] + [seq_feat_init] + rawstate.split('@')[3:])
        return rawstate

    def get_new_user_rawstate(self, rawstate, info):
        # 只有最后一步才改变状态，才有奖励
        assert type(rawstate) == type('')
        if 'actions' in info and info['actions'][-1] >= 0:
            seq_feat = rawstate.split('@')[2].split(';')
            expose_feat = ', '.join([str(i) + ':0' for i in info['actions']])
            predict_feat = ', '.join([str(i) + ':0' for i in info['pred_items']])
            seq_feat_actions = ';'.join([seq_feat[0], seq_feat[1], expose_feat, predict_feat])
            new_rawstate = '@'.join(rawstate.split('@')[:2] + [seq_feat_actions] + rawstate.split('@')[3:])
            return new_rawstate
        else:
            return rawstate


class L20RecSim(RecSim):
    def __init__(self, recEnvSrc: RecEnvSrc, model, modelfile, steps=9):
        RecSim.__init__(self, recEnvSrc, model, modelfile, steps)

    def _step(self, rawstate, action, info):
        """ Given an action and return for prior period, calculates costs, navs,
            etc and returns the reward and a  summary of the day's activity. """

        new_rawstate = self.recEnvSrc.get_new_user_rawstate(rawstate, info)

        self.actions[self.step] = action

        info['actions'] = self.actions

        if self.step < self.steps - 1:
            reward = 0
            rewards = []
            done = 0
        else:
            model = self.model
            done = 1

            raw_feats = []
            prices = []
            for item in self.actions[:3]:
                info['pred_items'] = [item]
                price = self.recEnvSrc.get_item_price(item) if item in self.recEnvSrc.available_item else -1000000
                prices.append(price)
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                # feat = self.recEnvSrc.get_new_user_state(rawstate, info)
                raw_feats.append(raw_feat)

            for item in self.actions[3:6]:
                info['pred_items'] = np.concatenate((self.actions[:3], [item]))
                price = self.recEnvSrc.get_item_price(item) if item in self.recEnvSrc.available_item else -1000000
                prices.append(price)
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                # feat = self.recEnvSrc.get_new_user_state(rawstate, info)
                raw_feats.append(raw_feat)

            for item in self.actions[6:]:
                info['pred_items'] = np.concatenate((self.actions[:6], [item]))
                price = self.recEnvSrc.get_item_price(item) if item in self.recEnvSrc.available_item else -1000000
                prices.append(price)
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                # feat = self.recEnvSrc.get_new_user_state(rawstate, info)
                raw_feats.append(raw_feat)

            info['pred_items'] = self.actions[:3]
            raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
            # feat = self.recEnvSrc.get_new_user_state(rawstate, info)
            raw_feats.append(raw_feat)

            info['pred_items'] = self.actions[:6]
            raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
            # feat = self.recEnvSrc.get_new_user_state(rawstate, info)
            raw_feats.append(raw_feat)

            feat = self.recEnvSrc.rawstate_to_state(raw_feats)

            ctr = self.predict_all(model, feat)
            rewards=[]
            rewards += [ctr[i] * prices[i] for i in range(3)]
            rewards += [ctr[9]*ctr[i] * prices[i] for i in range(3,6)]
            rewards += [ctr[10]*ctr[i] * prices[i] for i in range(6,9)]
            reward = np.sum(rewards)


        info = {'reward': reward, 'gmv': self.gmv[self.step], 'actions': self.actions, 'rewards': rewards, 'probs': self.probs}
        self.step += 1
        return new_rawstate, reward, done, info


class L20RecEnv(gym.Env):
    """
    This gym implements a simple recommendation environment for reinforcement learning.
    """

    def __init__(self, statefile, actionfile, modelfile, config, obs_size=906):
        from rslib.algo.keras_models import lstm_basic
        model,_ = lstm_basic.get_model(config)
        src = L20RecEnvSrc(config, statefile, actionfile)
        self.sim = L20RecSim(src, model, modelfile, steps=9)
        self.controllerobs = controllerObs(config, model, modelfile)
        self.action_space = spaces.Discrete(config['class_num'])
        self.observation_space = spaces.Box(-100.0,
                                            100.0,
                                            shape=(obs_size, 1),
                                            # dtype=np.float32
                                            )
        self.info = self.sim.get_init_info()
        self.cur_rawstate = None
        self.cur_obs = None
        self.user = None
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.stepp += 1
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        new_rawstate, reward, done, info = self.sim._step(self.cur_rawstate, action, self.info)
        self.cur_rawstate = new_rawstate
        self.info = info
        # observation用于RL学习，每步都变

        observation = self.controllerobs.get_obs(new_rawstate, info,self.stepp)
        return observation, reward, done, info

    def reset(self):
        self.stepp=0
        self.sim.reset()
        self.info = self.sim.get_init_info()
        self.user = self.sim.recEnvSrc.get_random_user()
        self.cur_rawstate = self.sim.recEnvSrc.get_user_rawstate(self.user)
        self.cur_obs = self.controllerobs.get_obs(self.cur_rawstate, self.info,self.stepp)
        return self.cur_obs


if __name__ == '__main__':
    import sys

    sys.path.append("../test_data")
    import param

    config = param.config
    # src = L20RecEnvSrc(config, statefile='../test_data/users.txt', actionfile='../test_data/items.txt')
    # print(src.get_user_rawstate('1000101190'))
    # rawstate = src.get_random_user_rawstate()
    # print(rawstate)
    # new_rawstate = src.get_new_user_rawstate(rawstate,{})
    # print(new_rawstate)
    # print(src.get_item_price('0'))
    #
    # from rslib.algo.keras_models import lstm_basic
    # model = lstm_basic.get_model(config)
    # sim = L20RecSim(src, model, '../test_data/baseline/baseline.tf', steps=9)
    # info=sim.get_init_info()
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # # rawstate, reward, done, info = sim._step(rawstate, 1, info)
    # print(info)
    #
    # controllerobs = controllerObs(config, model, '../test_data/baseline/baseline.tf')
    # controllerobs.get_obs(rawstate, info)
    # env = L20RecEnv('../test_data/users.txt', '../test_data/items.txt', '../test_data/baseline/baseline.tf',config , 906)
    # env.step(1)

    import gym
    from gym.envs.registration import register

    mykwargs = {'statefile': '../test_data/users.txt',
                'actionfile': '../test_data/items.txt',
                'modelfile': '../test_data/baseline/baseline.tf',
                'config': config,
                'obs_size': 906}

    register(
        id='L20mystic-v0',
        entry_point='l20mystic_env:L20RecEnv',
        # timestep_limit=9,
        reward_threshold=1000.0,
        nondeterministic=False,
        kwargs=mykwargs
    )
    env = gym.make('L20mystic-v0')
    RL = PolicyGradient(
        n_actions=env.action_space.n,
        n_features=env.observation_space.shape[0],
        learning_rate=0.001,
        reward_decay=0.995,
        # output_graph=True,
    )
    for i_episode in range(1000):
        observation = env.reset()
        while True:
            # if RENDER: env.render()
            action = RL.choose_action(observation)
            observation_, reward, done, info = env.step(action)  # reward = -1 in all cases
            RL.store_transition(observation, action, reward)
            if done:
                # calculate running reward
                ep_rs_sum = sum(RL.ep_rs)
                if 'running_reward' not in globals():
                    running_reward = ep_rs_sum
                else:
                    running_reward = running_reward * 0.99 + ep_rs_sum * 0.01
                print("episode:", i_episode, "  reward:", int(running_reward))
                print(info)
                print(ep_rs_sum)
                vt = RL.learn()  # train
                break
            observation = observation_

