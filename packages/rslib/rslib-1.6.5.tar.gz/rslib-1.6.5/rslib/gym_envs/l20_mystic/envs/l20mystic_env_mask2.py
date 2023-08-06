import sys
import traceback
from functools import reduce

import math
import tensorflow as tf
import gym
from gym import error, spaces, utils
from gym.spaces import Discrete, Box, Dict
from gym.utils import seeding

from rslib.algo.atrank import ATRank
from rslib.core.FeatureUtil import FeatureUtil
import random
import numpy as np
from rslib.gym_envs.RecEnvSrc import RecEnvSrc
from rslib.gym_envs.RecSim import RecSim
from rslib.algo.keras_models import lstm_basic

sys.path.append("../test_data")


class controllerObs(object):
    def __init__(self, config, model, modelfile, sess, src, batch_size=None, one_step=False, use_rule=False):
        self.config = config
        self.FeatureUtil = FeatureUtil(config)
        self.model = model
        # self.model.load_weights(modelfile)
        saver = tf.train.Saver()
        sess = tf.keras.backend.get_session()
        saver.restore(sess, modelfile)

        self.item_emb1 = self.model.get_layer('embedding_4').get_weights()[0]
        self.item_emb2 = self.model.get_layer('embedding_5').get_weights()[0]
        self.item_embs = [self.item_emb1, self.item_emb2]

        # self.item_emb0 = self.model.get_layer('embedding').get_weights()[0]
        # self.item_emb11 = self.model.get_layer('embedding_1').get_weights()[0]
        # self.lstm_emb = self.model.get_layer('lstm').get_weights()[0]
        # self.lstm_emb1 = self.model.get_layer('lstm_1').get_weights()[0]
        # self.lstm_emb2 = self.model.get_layer('lstm_2').get_weights()[0]
        # self.lstm_emb3 = self.model.get_layer('lstm_3').get_weights()[0]
        # self.dense = self.model.get_layer('dense').get_weights()[0]

        # tf.keras.backend.set_learning_phase(0)
        self.mid_layer_model = tf.keras.backend.function(self.model.input, [self.model.get_layer('attention1_reduce').output, self.model.get_layer('dropout_1').output])
        # self.emb1 = tf.keras.backend.function(self.model.input, self.model.get_layer('embedding').output)
        # self.lstm1 = tf.keras.backend.function(self.model.input, self.model.get_layer('lstm').output)

        # self.final_layer_model = tf.keras.backend.function(self.model.input, self.model.get_layer('dense').output)
        self.sess = sess
        self.src = src
        self.batch_size = batch_size
        self.one_step = one_step
        self.use_rule = use_rule

    def get_item_emb(self, itemid):
        if int(itemid) >= 0:
            emb = np.array([x[int(itemid)] for x in self.item_embs])
            return np.max(emb, axis=0)
        else:
            return np.zeros(len(self.item_embs[0][0]))

    def keras_emb(self, rawstate):
        feat = self.FeatureUtil.feature_extraction(rawstate, predict=True)
        session = self.sess
        with session.as_default():
            with session.graph.as_default():
                # xx = self.emb1(feat)
                # yy = self.lstm1(feat)
                mid_layer_output = self.mid_layer_model(feat)
                mid_layer_output = np.concatenate(mid_layer_output, axis=-1)
        return mid_layer_output if self.batch_size else mid_layer_output[0]

    def action_mask(self, step, selected_embs):
        if step < 3:
            if step == 0:
                l_mask = self.src.l1_mask
                t_mask = self.src.t3_mask | self.src.t4_mask
            elif step == 1:
                l_mask = self.src.l1_mask
                t_mask = self.src.t3_mask | self.src.t3_mask | self.src.t4_mask
            else:
                l_mask = self.src.l1_mask
                t_mask = self.src.t0_mask
        elif step < 6:
            if step == 3:
                l_mask = self.src.l2_mask
                t_mask = self.src.t1_mask | self.src.t2_mask
            elif step == 4:
                l_mask = self.src.l2_mask
                t_mask = self.src.t3_mask | self.src.t4_mask
            else:
                l_mask = self.src.l2_mask
                t_mask = self.src.t0_mask
        else:
            if step == 6:
                l_mask = self.src.l3_mask
                t_mask = self.src.t1_mask
            elif step == 7:
                l_mask = self.src.l3_mask
                t_mask = self.src.t3_mask | self.src.t4_mask
            else:
                l_mask = self.src.l3_mask
                t_mask = self.src.t0_mask

        if self.use_rule:
            lt_mask = l_mask & t_mask
        else:
            lt_mask = l_mask

        mask = np.array([lt_mask for _ in range(self.batch_size)])
        mask = mask * (-1 * (selected_embs - 1))

        have_ssr = np.max(self.src.l0_ssr_mask * selected_embs, axis=1)
        have_ssr_mask = have_ssr * self.src.l0_ssr_mask
        mask = mask * (-1 * (have_ssr_mask - 1))

        have_taohua = np.max(self.src.taohua_mask * selected_embs, axis=1)
        have_taohua_mask = have_taohua * self.src.taohua_mask
        mask = mask * (-1 * (have_taohua_mask - 1))

        assert np.shape(mask)[-1] == 300
        return mask

    def step_onehot(self, step):
        # assert step >= 0 and step <= 8
        step += 1
        onehot = np.array([[0] * (step - 1) + [1] + [0] * (10 - step)] * self.batch_size)
        # assert np.shape(onehot)[-1] == 9
        return onehot

    def layer_onehot(self, layers):
        onehot = np.array([reduce(lambda x, y: x + ([0] * (y - 1) + [1] * (1 if y >= 1 and y <= 3 else 0) + [0] * (3 - y)), layers[:, batch_i], []) for batch_i in range(self.batch_size)])
        assert np.shape(onehot)[-1] == 27
        return onehot

    def paytype_onehot(self, paytypes):
        onehot = np.array([reduce(lambda x, y: x + ([0] * (y - 1) + [1] * (1 if y >= 1 and y <= 4 else 0) + [0] * (4 - y)), paytypes[:, batch_i], []) for batch_i in range(self.batch_size)])
        assert np.shape(onehot)[-1] == 36
        return onehot

    def select_onehot(self, actions):
        onehot = np.zeros([self.batch_size, 300], dtype=np.int32)
        index = np.arange(0, np.shape(actions)[0])[:, np.newaxis].repeat(np.shape(actions)[1], 1)
        onehot[index, actions] = 1
        return onehot

    def rawstate2obs(self, rawstate, info, step):
        if step == 0:
            self.hist_emb = self.keras_emb(rawstate)
        # a = self.item_emb1[info['actions']]
        if self.one_step:
            return self.hist_emb

        item_embs = np.concatenate([np.concatenate([item_emb[info['actions'][:step]], np.zeros([9 - step, self.batch_size, np.shape(item_emb)[-1]], dtype=int)])
                                    for item_emb in self.item_embs], axis=2)
        item_emb = np.reshape(np.transpose(item_embs, [1, 0, 2]), [self.batch_size, -1])

        step_embs = self.step_onehot(step)
        layers_embs = self.layer_onehot(info['layers'])
        paytypes_embs = self.paytype_onehot(info['paytypes'])

        select_embs = self.select_onehot(np.transpose(info['actions'][:step], [1, 0]))

        action_mask = self.action_mask(step, select_embs)
        # action_mask = np.ones([self.batch_size,300])

        return np.concatenate([action_mask, select_embs, step_embs, self.hist_emb, item_emb, layers_embs, paytypes_embs], 1)

    def get_obs(self, new_rawstate, info, step):
        obs = self.rawstate2obs(new_rawstate, info, step)
        # print(np.shape(obs))
        return obs


class L20RecEnvSrc(RecEnvSrc):
    def __init__(self, config, statefile, actionfile, batch_size=None, reward_type='ctr_price'):
        RecEnvSrc.__init__(self, config, statefile, actionfile, batch_size=batch_size, reward_type=reward_type)

    def get_user_rawstate(self, role_ids):
        rawstates = []
        for role_id in role_ids:
            rawstate = self.state_dict[str(role_id)]
            seq_feat = rawstate.split('@')[2].split(';')
            seq_feat_init = ';'.join([seq_feat[0], seq_feat[1], '0:0', '0:0'])
            rawstate = '@'.join(rawstate.split('@')[:2] + [seq_feat_init] + rawstate.split('@')[3:])

            rawstates.append(rawstate)
        return rawstates

    def get_new_user_rawstate(self, rawstates, info):
        # 只有最后一步才改变状态，才有奖励
        # assert type(rawstates) == type('')

        if 'actions' in info and info['actions'][-1][0] >= 0:
            new_rawstates = []
            for i, rawstate in enumerate(rawstates):
                seq_feat = rawstate.split('@')[2].split(';')
                expose_feat = ', '.join([str(x) + ':1' for x in info['actions'][:, i]])
                predict_feat = ', '.join([str(x) + ':1' for x in info['pred_items'][:, i]])
                seq_feat_actions = ';'.join([seq_feat[0], seq_feat[1], expose_feat, predict_feat])
                new_rawstate = '@'.join(rawstate.split('@')[:2] + [seq_feat_actions] + rawstate.split('@')[3:])
                new_rawstates.append(new_rawstate)
            return new_rawstates
        else:
            return rawstates


class L20RecSim(RecSim):
    def __init__(self, recEnvSrc: RecEnvSrc, model, modelfile, sess, steps=9, batch_size=None, reward_sqr=False, use_rule=False):
        RecSim.__init__(self, recEnvSrc, model, modelfile, steps, batch_size)
        self.sess = sess
        self.reward_sqr = reward_sqr
        self.use_rule = use_rule

        self.layers = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)
        self.paytypes = np.zeros([self.steps, self.batch_size], dtype=int) if self.batch_size else np.zeros(self.steps, dtype=int)

    def _step(self, rawstate, action, info):
        """ Given an action and return for prior period, calculates costs, navs,
            etc and returns the reward and a  summary of the day's activity. """

        new_rawstate = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
        self.actions[self.step] = action

        self.layers[self.step] = np.array([self.recEnvSrc.action_dict[a]['layer'] for a in action])
        self.paytypes[self.step] = np.array([self.recEnvSrc.action_dict[a]['paytype'] for a in action])

        info['actions'] = self.actions
        info['layers'] = self.layers
        info['paytypes'] = self.paytypes

        # region 业务规则介绍
        '''
        业务规则：
            价格 1
            物品在对应层 1
            没有相同物品 1
            第一层必有铜钱或姻缘 1
            第二层必有红尘或红豆，且必有铜钱或姻缘 1
            第三层必有红豆，且必有铜钱或姻缘 1
            桃花不能同时出现1个以上 1
            桃花限制出现
            ssr不能同时出现1个以上 1
            ssr，两种限制方法：1 以一定概率添加惩罚
                               2 price 乘以一个定值
        '''
        # endregion

        # region 计算 业务规则
        self.t1 = self.recEnvSrc.t1_item
        self.t12 = self.recEnvSrc.t1_item | self.recEnvSrc.t2_item
        self.t34 = self.recEnvSrc.t3_item | self.recEnvSrc.t4_item
        self.t234 = self.recEnvSrc.t2_item | self.recEnvSrc.t3_item | self.recEnvSrc.t4_item
        self.ssr = self.recEnvSrc.l1_ssr_item | self.recEnvSrc.l2_ssr_item | self.recEnvSrc.l3_ssr_item

        layer_unique_check = [[1] * 3 for _ in range(self.batch_size)]
        layer_paytype_check = [[1] * 3 for _ in range(self.batch_size)]
        layer_item_in_layer_check = [[1] * 3 for _ in range(self.batch_size)]

        item_unique_check = [[1] * 9 for _ in range(self.batch_size)]
        item_paytype_check = [[1] * 9 for _ in range(self.batch_size)]
        item_item_in_layer_check = [[1] * 9 for _ in range(self.batch_size)]

        unique_check = [1 for _ in range(self.batch_size)]
        paytype_check = [1 for _ in range(self.batch_size)]
        item_in_layer_check = [1 for _ in range(self.batch_size)]
        taohua_check = [1 for _ in range(self.batch_size)]
        ssr_check = [1 for _ in range(self.batch_size)]

        # taohua_si

        step = self.step + 1
        prices = [[0] * 9 for _ in range(self.batch_size)]
        for batch_i in range(self.batch_size):
            #  region item-wise 业务规则, 目前主要是 paytype 的规则
            if step == 1:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][0] = 1 if item in self.t34 else 0
            elif step == 2:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][1] = 1 if item in self.t234 else 0
            elif step == 3:
                item_paytype_check[batch_i][2] = 1
            elif step == 4:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][3] = 1 if item in self.t12 else 0
            elif step == 5:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][4] = 1 if item in self.t34 else 0
            elif step == 6:
                item_paytype_check[batch_i][5] = 1
            elif step == 7:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][6] = 1 if item in self.t1 else 0
            elif step == 8:
                item = self.actions[step - 1, batch_i]
                item_paytype_check[batch_i][7] = 1 if item in self.t34 else 0
            elif step == 9:
                item_paytype_check[batch_i][8] = 1
            else:
                raise Exception("Invalid step!")
            # endregion

            # region layer-wise 业务规则
            item_in_layer123 = set(self.actions[0:step, batch_i])
            if step <= 3:
                item_in_layer1 = set(self.actions[0:step, batch_i])

                layer_unique_check[batch_i][0] = 1 if len(item_in_layer1) == step else 0
                layer_paytype_check[batch_i][0] = 1 if step < 3 or item_in_layer1 & self.t34 else 0
                layer_item_in_layer_check[batch_i][0] = 1 if len(item_in_layer1 & self.recEnvSrc.l1_item) == step else 0

            elif step <= 6:
                item_in_layer1 = set(self.actions[0:3, batch_i])
                item_in_layer2 = set(self.actions[3:step, batch_i])

                layer_unique_check[batch_i][0] = 1 if len(item_in_layer1) == 3 else 0
                layer_paytype_check[batch_i][0] = 1 if item_in_layer1 & self.t34 else 0
                layer_item_in_layer_check[batch_i][0] = 1 if len(item_in_layer1 & self.recEnvSrc.l1_item) == 3 else 0

                layer_unique_check[batch_i][1] = 1 if len(item_in_layer2) == step - 3 else 0
                layer_paytype_check[batch_i][1] = 1 if step == 4 or (step == 5 and (item_in_layer2 & self.t34 or item_in_layer2 & self.t12)) or \
                                                       (step == 6 and (item_in_layer2 & self.t34 and item_in_layer2 & self.t12)) else 0
                layer_item_in_layer_check[batch_i][1] = 1 if len(item_in_layer2 & self.recEnvSrc.l2_item) == step - 3 else 0

            else:
                item_in_layer1 = set(self.actions[0:3, batch_i])
                item_in_layer2 = set(self.actions[3:6, batch_i])
                item_in_layer3 = set(self.actions[6:step, batch_i])

                layer_unique_check[batch_i][0] = 1 if len(item_in_layer1) == 3 else 0
                layer_paytype_check[batch_i][0] = 1 if item_in_layer1 & self.t34 else 0
                layer_item_in_layer_check[batch_i][0] = 1 if len(item_in_layer1 & self.recEnvSrc.l1_item) == 3 else 0

                layer_unique_check[batch_i][1] = 1 if len(item_in_layer2) == 3 else 0
                layer_paytype_check[batch_i][1] = 1 if item_in_layer2 & self.t34 and item_in_layer2 & self.t12 else 0
                layer_item_in_layer_check[batch_i][1] = 1 if len(item_in_layer2 & self.recEnvSrc.l2_item) == 3 else 0

                layer_unique_check[batch_i][2] = 1 if len(item_in_layer3) == step - 6 else 0
                layer_paytype_check[batch_i][2] = 1 if step == 7 or (step == 8 and (item_in_layer3 & self.t34 or item_in_layer3 & self.t1)) or \
                                                       (step == 9 and (item_in_layer3 & self.t34 and item_in_layer3 & self.t1)) else 0
                layer_item_in_layer_check[batch_i][2] = 1 if len(item_in_layer3 & self.recEnvSrc.l3_item) == step - 6 else 0

            # endregion

            # region session-wise 业务规则
            taohua_check[batch_i] = 1 if len(item_in_layer123 & self.recEnvSrc.taohua_item) <= 1 else 0
            ssr_check[batch_i] = 1 if len(item_in_layer123 & self.ssr) <= 1 else 0
            # taohua_check[batch_i] = 1
            # ssr_check[batch_i] = 1
            # endregion

            # region 业务规则整合
            unique_check[batch_i] = reduce(lambda x, y: x & y, layer_unique_check[batch_i], 1)
            # paytype_check[batch_i] = layer_paytype_check[batch_i][0] & layer_paytype_check[batch_i][1] & layer_paytype_check[batch_i][2]
            paytype_check[batch_i] = reduce(lambda x, y: x & y, layer_paytype_check[batch_i], 1) & reduce(lambda x, y: x & y, item_paytype_check[batch_i], 1)
            item_in_layer_check[batch_i] = reduce(lambda x, y: x & y, layer_item_in_layer_check[batch_i], 1)
            # endregion

            # region 在最后一步获取已选物品的价格
            if step == self.steps:
                price = [self.recEnvSrc.get_item_price(i) if i in self.recEnvSrc.available_item else -1 for i in self.actions[0:9, batch_i]]
                if self.reward_sqr:
                    price = np.sqrt(price)
                prices[batch_i] = price
            # endregion
        # endregion
        a = 1

        # region 计算reward
        rewards = [[] for _ in range(self.batch_size)]
        reward = [0 for _ in range(self.batch_size)]
        done = [0 for _ in range(self.batch_size)]

        if step < self.steps:
            for batch_i in range(self.batch_size):
                if self.use_rule:
                    check = unique_check[batch_i] and paytype_check[batch_i] and item_in_layer_check[batch_i] and taohua_check[batch_i] and ssr_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])
                else:
                    check = unique_check[batch_i] and item_in_layer_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])
                if check:
                    reward[batch_i] = 0.1
                    done[batch_i] = 0
                elif not item_in_layer_check[batch_i] or not unique_check[batch_i]:
                    reward[batch_i] = -0.11
                    done[batch_i] = 1
                elif not paytype_check[batch_i] and self.use_rule:
                    reward[batch_i] = -0.12
                    done[batch_i] = 1
                elif (not taohua_check[batch_i] or not ssr_check[batch_i]) and self.use_rule:
                    reward[batch_i] = -0.13
                    done[batch_i] = 1
                else:
                    reward[batch_i] = -0.14
                    done[batch_i] = 1
            1

        else:
            model = self.model
            # print('actions' + str(info['actions']))
            # region 获得监督模型的 feature
            raw_feats = []
            for item in self.actions[0:3]:
                info['pred_items'] = np.concatenate((self.actions[0:0], [item]))
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                raw_feats.extend(raw_feat)

            for item in self.actions[3:6]:
                info['pred_items'] = np.concatenate((self.actions[0:3], [item]))
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                raw_feats.extend(raw_feat)

            for item in self.actions[6:9]:
                info['pred_items'] = np.concatenate((self.actions[0:6], [item]))
                raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
                raw_feats.extend(raw_feat)

            info['pred_items'] = self.actions[0:3]
            raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
            raw_feats.extend(raw_feat)

            info['pred_items'] = self.actions[0:6]
            raw_feat = self.recEnvSrc.get_new_user_rawstate(rawstate, info)
            raw_feats.extend(raw_feat)
            # endregion

            # region 计算 ctr
            feat = self.recEnvSrc.rawstate_to_state(raw_feats)
            ctr = self.predict_all(model, feat, self.sess)
            ctr = np.reshape(ctr, [11, self.batch_size])
            self.probs = ctr
            # endregion

            for batch_i in range(self.batch_size):
                rewards[batch_i] += [ctr[i][batch_i] * prices[batch_i][i] for i in range(0, 3)]
                rewards[batch_i] += [ctr[i][batch_i] * prices[batch_i][i] for i in range(3, 6)]
                rewards[batch_i] += [ctr[i][batch_i] * prices[batch_i][i] for i in range(6, 9)]
                # rewards[batch_i] += [ctr[9][batch_i] * ctr[i][batch_i] * prices[batch_i][i] for i in range(3, 6)]
                # rewards[batch_i] += [ctr[10][batch_i] * ctr[i][batch_i] * prices[batch_i][i] for i in range(6, 9)]

                if self.use_rule:
                    check = unique_check[batch_i] and paytype_check[batch_i] and item_in_layer_check[batch_i] and taohua_check[batch_i] and ssr_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])
                else:
                    check = unique_check[batch_i] and item_in_layer_check[batch_i] \
                            and (self.step == 0 or not self.dones[self.step - 1, batch_i])

                if check:
                    reward[batch_i] = sum(rewards[batch_i])
                    done[batch_i] = 1
                elif not item_in_layer_check[batch_i] or not unique_check[batch_i]:
                    reward[batch_i] = -0.11
                    done[batch_i] = 1
                elif not paytype_check[batch_i] and self.use_rule:
                    reward[batch_i] = -0.12
                    done[batch_i] = 1
                elif (not taohua_check[batch_i] or not ssr_check[batch_i]) and self.use_rule:
                    reward[batch_i] = -0.13
                    done[batch_i] = 1
                else:
                    reward[batch_i] = -0.14
                    done[batch_i] = 1

            # print('actions:' + str(info['actions']))
            # print('rewards:' + str(rewards))
            # print('reward:' + str(reward))

        # endregion

        self.dones[self.step] = done
        # print('actions:' + str(info['actions'][:, 0]))
        # print('actions:' + str(info['actions']))
        # print('rewards:' + str(rewards))
        # print('reward:' + str(reward))

        info['reward'] = reward
        info['rewards'] = rewards
        info['gmv'] = self.gmv[self.step]
        info['probs'] = self.probs
        # info['len'] = np.sum(self.dones[:self.step + 1], axis=0)
        # print(info['len'])

        self.step += 1
        return new_rawstate, reward, done, info


class L20RecEnv(gym.Env):
    """
    This gym implements a simple recommendation environment for reinforcement learning.
    """

    def __init__(self, batch_size=None, one_step=False, reward_sqr=False, use_rslib_model=False, use_rule=True, reward_type='ctr'):
        import param_up
        import param2
        config = param_up.config
        config['is_serving'] = 1
        config2 = param2.config

        statefile, actionfile, modelfile, config = '../test_data/users.txt', '../test_data/items.txt', '../test_data/baseline/baseline.tf', config
        modelfile = '/root/rslib/demo/mystic/code/output/0315atrank256mean.ckpt'
        obs_size = 1361
        if batch_size:
            self.batch_size = batch_size
            self.batch = True
        else:
            self.batch_size = 1
            self.batch = False
        self.one_step = one_step
        self.reward_sqr = reward_sqr
        self.use_rslib_model = use_rslib_model
        self.use_rule = use_rule

        model, sess = ATRank.get_model(config, return_session=True)
        # model, sess = lstm_basic.get_model(config, return_session=True)
        self.src = L20RecEnvSrc(config, statefile, actionfile, batch_size=self.batch_size, reward_type=reward_type)
        self.sim = L20RecSim(self.src, model, modelfile, sess, steps=9, batch_size=self.batch_size, reward_sqr=self.reward_sqr, use_rule=self.use_rule)
        self.controllerobs = controllerObs(config, model, modelfile, sess, self.src, batch_size=self.batch_size, one_step=self.one_step, use_rule=self.use_rule)
        self.action_space = spaces.Discrete(config['class_num'])
        self.observation_space = spaces.Box(-10000.0, 10000.0, shape=(obs_size,))
        self.FeatureUtil = FeatureUtil(config2)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.stepp += 1
        # assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        action = action if self.batch else [action]
        new_rawstate, reward, done, info = self.sim._step(self.cur_rawstate, action, self.info)
        self.cur_rawstate = new_rawstate
        self.info = info
        # observation用于RL学习，每步都变
        if self.use_rslib_model:
            return self.FeatureUtil.feature_extraction(data=self.cur_rawstate, predict=True), reward, done, info

        observation = self.controllerobs.get_obs(new_rawstate, self.info, self.stepp)

        if self.batch:
            return observation, reward, done, info
        else:
            return observation[0], reward[0], done[0], info

    def reset(self, reset_user=True):
        self.stepp = 0
        self.sim.reset()
        self.info = self.sim.get_init_info()
        if reset_user:
            self.user = self.sim.recEnvSrc.get_random_user()
        self.cur_rawstate = self.sim.recEnvSrc.get_user_rawstate(self.user)

        if self.use_rslib_model:
            return self.FeatureUtil.feature_extraction(data=self.cur_rawstate, predict=True)

        observation = self.controllerobs.get_obs(self.cur_rawstate, self.info, self.stepp)
        if self.batch:
            return observation
        else:
            return observation[0]
