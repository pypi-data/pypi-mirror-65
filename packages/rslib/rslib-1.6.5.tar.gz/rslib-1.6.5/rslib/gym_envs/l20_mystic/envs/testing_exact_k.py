import numpy as np
import tensorflow as tf

from rslib.algo.rl.exact_k.model import Generator, Discriminator, hp
# from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask2 import L20RecEnv
from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask_atrank2 import L20RecEnv
from rslib.algo.keras_models import lstm_basic
from rslib.core.FeatureUtil import FeatureUtil

import collections

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('传入参数：***.py')
    parser.add_argument('-b', '--batch', default=64, type=int)
    parser.add_argument('-l1', '--learning_actor', default=0.001, type=float)
    parser.add_argument('-l2', '--learning_critic', default=0.005, type=float)
    parser.add_argument('-r1', '--reward_std', default=True, type=bool)
    parser.add_argument('-r2', '--reward_sqr', default=False, type=bool)
    parser.add_argument('-t', '--temperature', default=10.0, type=float)

    args = parser.parse_args()

    batch = args.batch
    learning_actor = args.learning_actor
    learning_critic = args.learning_critic
    reward_std = args.reward_std
    reward_sqr = args.reward_sqr
    temperature = args.temperature
    temperature = 20
    # temperature = 10

    res = []

    # region load env model,env
    # env = get_l20mystic_env_mask2()
    batch_size = args.batch
    env = L20RecEnv(batch_size=batch_size, one_step=True, reward_sqr=reward_sqr, reward_type='ctr_price')

    l1_mask = env.src.l1_mask
    l2_mask = env.src.l2_mask
    l3_mask = env.src.l3_mask
    t0_mask = env.src.t0_mask
    t1_mask = env.src.t1_mask
    t2_mask = env.src.t2_mask
    t3_mask = env.src.t3_mask
    t4_mask = env.src.t4_mask
    l0_ssr_mask = env.src.l0_ssr_mask
    taohua_mask = env.src.taohua_mask
    item_id_map = env.src.item_id_embedding

    # endregion
    # region Construct graph
    with tf.name_scope('Generator'):
        g = Generator(l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, l0_ssr_mask, taohua_mask, is_training=False, lr=learning_actor, temperature=temperature, item_id_map=item_id_map)
    print(len(tf.get_variable_scope().global_variables()))

    with tf.name_scope('Discriminator'):
        d = Discriminator(lr=learning_critic)

    print("Graph loaded")
    # endregion

    # region gpu option
    gpu_options = tf.GPUOptions(
        per_process_gpu_memory_fraction=0.95,
        allow_growth=True)  # seems to be not working
    sess_config = tf.ConfigProto(allow_soft_placement=True,
                                 gpu_options=gpu_options)
    # endregion

    with tf.Session(config=sess_config) as sess:
        # sess.run(tf.initialize_all_variables())
        # vars = [var for var in g.variables if var.name != 'decoder/id_map_table:0']
        # saver = tf.train.Saver(vars)
        saver = tf.train.Saver()
        model_file = '/root/rslib/rslib/gym_envs/l20_mystic/envs/ckpt/exact_k_atrank2_r2_s2.ckpt'
        saver.restore(sess, model_file)
        print('Generator training start!')

        reward_total = 0.0
        for episode in range(16):
            # if sv.should_stop():
            #     break
            print('Generator episode: ', episode)

            # 从环境中获取用户特征和候选物品，env reset
            # user：用户特征
            # item_cand：候选物品
            observation = np.array(env.reset())
            item_cand = np.array([list(range(0, 300))] * batch_size)

            custom_path, custom_result, custom_result_map = sess.run([g.custom_path, g.custom_result, g.custom_result_map],
                                                                     feed_dict={g.user: observation, g.item_cand: item_cand})

            # print('2' + str(custom_result_map))
            res.extend(list(custom_result_map))

        l1 = collections.defaultdict(int)
        l2 = collections.defaultdict(int)
        l3 = collections.defaultdict(int)
        l1_t = collections.defaultdict(int)
        l2_t = collections.defaultdict(int)
        l3_t = collections.defaultdict(int)

        for items in res:
            for i, item in enumerate(items):
                if i < 3:
                    l1[item] += 1
                    l1_t[str(item)[1]] += 1
                elif i < 6:
                    l2[item] += 1
                    l2_t[str(item)[1]] += 1
                else:
                    l3[item] += 1
                    l3_t[str(item)[1]] += 1

        l1 = sorted(l1.items(), key=lambda a: a[1], reverse=True)
        l2 = sorted(l2.items(), key=lambda a: a[1], reverse=True)
        l3 = sorted(l3.items(), key=lambda a: a[1], reverse=True)
        l1_t = sorted(l1_t.items(), key=lambda a: a[0])
        l2_t = sorted(l2_t.items(), key=lambda a: a[0])
        l3_t = sorted(l3_t.items(), key=lambda a: a[0])
        print(l1)
        print(l2)
        print(l3)
        print(l1_t)
        print(l2_t)
        print(l3_t)

        # tf.saved_model.simple_save(sess,
        #                            "./model",
        #                            inputs={"user": g_infer.user, 'item_cand': g_infer.item_cand},
        #                            outputs={"myOutput": aa})
        # break

        print('Generator training done!')
    print("Done")
