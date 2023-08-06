import numpy as np
import tensorflow as tf

from rslib.algo.rl.exact_k.model import Generator, Discriminator, hp
# from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask2 import L20RecEnv
from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask_atrank2 import L20RecEnv
from rslib.algo.keras_models import lstm_basic
from rslib.core.FeatureUtil import FeatureUtil

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
        g = Generator(l1_mask, l2_mask, l3_mask, t0_mask, t1_mask, t2_mask, t3_mask, t4_mask, l0_ssr_mask, taohua_mask, is_training=True, lr=learning_actor, temperature=temperature, item_id_map=item_id_map)
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
        sess.run(tf.initialize_all_variables())
        print('Generator training start!')

        reward_total = 0.0
        for episode in range(100000):
            # if sv.should_stop():
            #     break
            print('Generator episode: ', episode)

            # 从环境中获取用户特征和候选物品，env reset
            # user：用户特征
            # item_cand：候选物品
            observation = np.array(env.reset())
            item_cand = np.array([list(range(0, 300))] * batch_size)
            while True:
                hill_b_f = []
                for i in range(2):
                    # get action
                    # sample

                    sampled_card_idx, sampled_card, sampled_result_map = sess.run([g.sampled_path, g.sampled_result, g.sampled_result_map],
                                                                  feed_dict={g.user: observation, g.item_cand: item_cand})
                    # sampled_card_idx, sampled_card = sess.run([g.sampled_path, g.sampled_result],
                    #                                           feed_dict={g.user: observation, g.item_cand: item_cand})
                    # 调用模拟环境，计算 reward，env step
                    for step in range(9):
                        observation_, reward, done, info = env.step(sampled_card[:, step])

                    env.reset(reset_user=False)
                    # hill b f
                    hill_b_f.append(list(zip(sampled_card, sampled_card_idx, reward)))

                b_hill_f = np.transpose(hill_b_f, [1, 0, 2])
                samples = []
                for hill_f in b_hill_f:
                    sorted_list = sorted(hill_f, key=lambda x: x[2], reverse=True)
                    samples.append(sorted_list[np.random.choice(1)])

                (sampled_card, sampled_card_idx, reward) = zip(*samples)

                # train
                # card_idx：
                # print(reward)
                reward = np.array(reward)
                reward = reward / 100 if reward_sqr else reward / 10000

                reward_ = sess.run(d.reward, feed_dict={d.user: observation})
                sess.run(d.train_op, feed_dict={d.user: observation, d.reward_target: reward})

                if episode % 50 == 0:
                    print('episode:' + str(episode))
                    print('reward_target' + str(reward_))
                    print('reward' + str(reward))
                    print('actions' + str(sampled_card))
                    print('actions' + str(sampled_result_map))

                # reward 1
                # reward = (reward - reward_)

                # reward 2
                reward = (reward - reward_) / np.abs(reward_)
                reward = np.clip(reward, -2, 2)



                if reward_std:
                    reward = reward / np.std(reward)

                sess.run(g.train_op, feed_dict={g.decode_target_ids: sampled_card_idx,
                                                g.reward: reward,
                                                g.item_cand: item_cand,
                                                g.user: observation,
                                                })
                gs_gen = sess.run(g.global_step)

                # beamsearch
                # beam_card = sess.run(g_infer.infer_result,
                #                      feed_dict={g_infer.item_cand: item_cand,
                #                                 g_infer.user: observation})
                # aa = tf.identity(g_infer.infer_result, name="myOutput")
                # print('beam_card' + str(beam_card[0]))

                if done:
                    break

            # tf.saved_model.simple_save(sess,
            #                            "./model",
            #                            inputs={"user": g_infer.user, 'item_cand': g_infer.item_cand},
            #                            outputs={"myOutput": aa})
            # break
            if episode % 5000 == 0:
                saver = tf.train.Saver()
                # model_file = '/root/rslib/demo/mystic/code/output/exact_k.ckpt'
                model_file = '//root/rslib/rslib/gym_envs/l20_mystic/envs/ckpt/exact_k_atrank2_r2_s2.ckpt'
                saver.save(sess, model_file)
                print('Generator training done!')
    print("Done")
