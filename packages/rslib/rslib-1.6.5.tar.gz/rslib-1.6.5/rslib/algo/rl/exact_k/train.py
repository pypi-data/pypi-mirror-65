# -*- coding: utf-8 -*-
# /usr/bin/python2
import numpy as np
import tensorflow as tf

from rslib.algo.rl.exact_k.model import Generator
from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask2 import L20RecEnv, get_l20mystic_env_mask2

if __name__ == '__main__':
    # region load env model,env
    # env = get_l20mystic_env_mask2()
    env = L20RecEnv()
    # endregion
    # region Construct graph
    with tf.name_scope('Generator'):
        g = Generator(is_training=True)
    print(len(tf.get_variable_scope().global_variables()))

    tf.get_variable_scope().reuse_variables()
    with tf.name_scope('GeneratorInfer'):
        g_infer = Generator(is_training=False)
    print("Graph loaded")
    # endregion
    # region supervisor
    sv = tf.train.Supervisor(is_chief=True,
                             summary_op=None,
                             save_model_secs=0)
    # endregion
    # region gpu option
    gpu_options = tf.GPUOptions(
        per_process_gpu_memory_fraction=0.95,
        allow_growth=True)  # seems to be not working
    sess_config = tf.ConfigProto(allow_soft_placement=True,
                                 gpu_options=gpu_options)
    # endregion

    with sv.managed_session(config=sess_config) as sess:
        print('Generator training start!')

        reward_total = 0.0
        for episode in range(300):
            if sv.should_stop():
                break
            print('Generator episode: ', episode)

            # 从环境中获取用户特征和候选物品，env reset
            # user：用户特征
            # item_cand：候选物品
            observation = env.reset()
            item_cand = np.array([list(range(1, 300))])
            while True:
                # get action
                # sample
                sampled_card_idx, sampled_card = sess.run([g.sampled_path, g.sampled_result],
                                                          feed_dict={g.enc_user: observation, g.item_cand: item_cand})
                # 调用模拟环境，计算 reward，env step
                observation_, reward, done, info = env.step(sampled_card)  # reward = -1 in all cases
                # reward = sess.run(d_infer.dis_reward, feed_dict={d_infer.card: sampled_card, d_infer.user: user})

                # train
                # card_idx：
                sess.run(g.train_op, feed_dict={g.decode_target_ids: sampled_card_idx,
                                                g.reward: reward,
                                                g.item_cand: item_cand,
                                                g.enc_user: observation,
                                                })
                gs_gen = sess.run(g.global_step)
                reward_total += np.mean(reward)

                # beamsearch
                beam_card = sess.run(g_infer.infer_result,
                                     feed_dict={g_infer.item_cand: item_cand,
                                                g_infer.enc_user: observation})

                if done:
                    break

        print('Generator training done!')
    print("Done")
