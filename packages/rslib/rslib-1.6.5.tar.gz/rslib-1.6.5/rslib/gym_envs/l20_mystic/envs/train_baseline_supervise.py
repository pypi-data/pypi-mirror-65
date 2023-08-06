import numpy as np
import tensorflow as tf

from rslib.algo.rl.exact_k.model import Generator, Discriminator, hp
from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask2 import L20RecEnv
from rslib.algo.keras_models import lstm_basic
from rslib.core.FeatureUtil import FeatureUtil

import param2

if __name__ == '__main__':

    use_rule = 1
    rank_method = 'ctr'

    # region 加载监督模型
    # ds = '2020-03-02'
    # model_type = 'lstm'
    # model_unit = ['sequence', 'cross', 'user']
    # model_file = "/project/diting/l20_mystic/model/%s/model_%s_%s.ckpt" % (ds, model_type, '_'.join(model_unit))
    model_file = '../test_data/supervise/model_lstm_sequence_cross_user.ckpt'
    config = param2.config
    config['is_serving'] = True

    g1 = tf.Graph()
    sess1 = tf.Session(graph=g1)

    g2 = tf.Graph()
    sess2 = tf.Session(graph=g2)

    with sess1.as_default():
        with g1.as_default():
            # region 加载监督模型模型，用于生成 推荐物品
            model = lstm_basic.get_model(config)
            saver = tf.train.Saver()
            saver.restore(sess1, model_file)
            # endregion        
    with sess2.as_default():
        with g2.as_default():
            # region 加载环境模型，用于生成 reward
            env = L20RecEnv(use_rslib_model=True, use_rule=use_rule)
            l1_item = env.src.l1_item
            l2_item = env.src.l2_item
            l3_item = env.src.l3_item
            t0_item = env.src.available_item
            t1_item = env.src.t1_item
            t2_item = env.src.t2_item
            t3_item = env.src.t3_item
            t4_item = env.src.t4_item
            ssr_item = env.src.l0_ssr_item
            taohua_item = env.src.taohua_item
            item_dict = env.src.action_dict
            # endregion        

    # region 

    with sess1.as_default():
        with g1.as_default():
            for episode in range(3000000):
                observation = env.reset()
                while True:
                    # region 监督模型预测结果
                    scores = model.predict(observation)[0]

                    # endregion
                    # region 排序
                    if rank_method == 'ctr':
                        item_score = [[i, scores[i]] for i in range(1, 251)]
                    elif rank_method == 'ctr_price':
                        item_score = [[i, scores[i] * item_dict[i]['price']] for i in range(1, 251)]
                    else:
                        item_score = [[i, scores[i]] for i in range(1, 251)]
                    item_score.sort(key=lambda x: x[1], reverse=True)
                    items = [x[0] for x in item_score]
                    # endregion
                    action = [0] * 9
                    # region 业务规则
                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l1_item & (t3_item | t4_item) - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l1_item - set(action)
                    for item in items:
                        if item in cand:
                            action[0] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l1_item & (t2_item | t3_item | t4_item) - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l1_item - set(action)
                    for item in items:
                        if item in cand:
                            action[1] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l1_item - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l1_item - set(action)
                    for item in items:
                        if item in cand:
                            action[2] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l2_item & (t1_item | t2_item) - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l2_item - set(action)
                    for item in items:
                        if item in cand:
                            action[3] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l2_item & (t3_item | t4_item) - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l2_item - set(action)
                    for item in items:
                        if item in cand:
                            action[4] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l2_item - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l2_item - set(action)
                    for item in items:
                        if item in cand:
                            action[5] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l3_item & t1_item - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l3_item - set(action)
                    for item in items:
                        if item in cand:
                            action[6] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l3_item & (t3_item | t4_item) - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l3_item - set(action)
                    for item in items:
                        if item in cand:
                            action[7] = item
                            break

                    set_action = set(action)
                    have_ssr = 1 if set_action & ssr_item else 0
                    have_taohua = 1 if set_action & taohua_item else 0
                    if use_rule:
                        cand = l3_item - set(action)
                        if have_ssr:
                            cand = cand - ssr_item
                        if have_taohua:
                            cand = cand - taohua_item
                    else:
                        cand = l3_item - set(action)
                    for item in items:
                        if item in cand:
                            action[8] = item
                            break
                    # endregion
                    print('jiandu:' + str(action))
                    action_scores=[scores[item] for item in action]
                    print('jiandu s:' + str(action_scores))
                    # region 与环境交互，获取 reward
                    for step in range(9):
                        observation_, reward, done, info = env.step(action[step])
                    # endregion

                    print(reward)
                    if done:
                        break

            print("Done")
