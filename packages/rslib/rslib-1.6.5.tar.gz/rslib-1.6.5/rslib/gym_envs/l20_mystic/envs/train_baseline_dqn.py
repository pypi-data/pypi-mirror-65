
import tensorflow as tf
from rslib.gym_envs.l20_mystic.envs.l20mystic_env_mask2 import L20RecEnv

if __name__ == '__main__':
    from gym.envs.registration import register
    from rslib.algo.rl.dqn2.dqn_mask import get_dqn_mask

    mykwargs = {}


    trainer = get_dqn_mask(L20RecEnv)
    while True:
        # print(pretty_print(trainer.train()))
        trainer.train()
