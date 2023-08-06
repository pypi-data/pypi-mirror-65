import ray
from ray.rllib.agents.a3c.a2c import A2CTrainer
from ray.rllib.agents.pg import PGTrainer
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.models import ModelCatalog
from ray.rllib.models.model import Model
from ray.rllib.utils.annotations import override
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env
from rslib.algo.rl.dqn.dqn import DQNTrainer
from rslib.algo.rl.dqn.fcnet import FullyConnectedNetwork

ray.init()

DQN_config = {
    # === Model ===
    # Number of atoms for representing the distribution of return. When
    # this is greater than 1, distributional Q-learning is used.
    # the discrete supports are bounded by v_min and v_max
    "num_atoms": 1,
    "v_min": -10.0,
    "v_max": 10.0,
    # Whether to use noisy network
    "noisy": False,
    # control the initial value of noisy nets
    "sigma0": 0.5,
    # Whether to use dueling dqn
    "dueling": True,
    # Whether to use double dqn
    "double_q": True,
    # Postprocess model outputs with these hidden layers to compute the
    # state and action values. See also the model config in catalog.py.
    # "hiddens": [128, 128],
    "hiddens": [256, 256],
    # N-step Q learning
    "n_step": 1,

    # === Exploration ===
    # Max num timesteps for annealing schedules. Exploration is annealed from
    # 1.0 to exploration_fraction over this number of timesteps scaled by
    # exploration_fraction
    "schedule_max_timesteps": 10000000,
    "schedule_max_timesteps": 10000000,
    # Minimum env steps to optimize for per train call. This value does
    # not affect learning, only the length of iterations.
    "timesteps_per_iteration": 100,
    # Fraction of entire training period over which the exploration rate is
    # annealed
    "exploration_fraction": 0.1,
    # Final value of random action probability
    "exploration_final_eps": 0.03,
    # Update the target network every `target_network_update_freq` steps.
    "target_network_update_freq": 1000,
    # Use softmax for sampling actions. Required for off policy estimation.
    "soft_q": False,
    # Softmax temperature. Q values are divided by this value prior to softmax.
    # Softmax approaches argmax as the temperature drops to zero.
    "softmax_temp": 1.0,
    # If True parameter space noise will be used for exploration
    # See https://blog.openai.com/better-exploration-with-parameter-noise/
    # "parameter_noise": True,
    # Extra configuration that disables exploration.
    # "evaluation_config": {
    #     "exploration_fraction": 0,
    #     "exploration_final_eps": 0,
    # },

    # === Replay buffer ===
    # Size of the replay buffer. Note that if async_updates is set, then
    # each worker will have a replay buffer of this size.
    "buffer_size": 100000,
    # If True prioritized replay buffer will be used.
    # "prioritized_replay": False,
    "prioritized_replay": True,

    # Alpha parameter for prioritized replay buffer.
    "prioritized_replay_alpha": 0.6,
    # Beta parameter for sampling from prioritized replay buffer.
    "prioritized_replay_beta": 0.4,
    # Fraction of entire training period over which the beta parameter is
    # annealed
    "beta_annealing_fraction": 0.2,
    # Final value of beta
    "final_prioritized_replay_beta": 0.4,
    # Epsilon to add to the TD errors when updating priorities.
    "prioritized_replay_eps": 1e-6,
    # Whether to LZ4 compress observations
    "compress_observations": True,

    # === Optimization ===
    # Learning rate for adam optimizer
    # "lr": 0.001,
    "lr": 5e-4,
    # Learning rate schedule
    "lr_schedule": None,
    # Adam epsilon hyper parameter
    "adam_epsilon": 1e-8,
    # If not None, clip gradients during optimization at this value
    "grad_norm_clipping": None,
    "learning_starts": 100000,
    "learning_starts": 10000,
    "sample_batch_size": 4,
    "train_batch_size": 32,
}

def get_dqn_mask(env):
    ModelCatalog.register_custom_model("pre_model", FullyConnectedNetwork)
    trainer = DQNTrainer(
        env=env,
        config={
            **DQN_config,
            "model": {
                "custom_model": 'pre_model',
            },
        }
    )
    return trainer
