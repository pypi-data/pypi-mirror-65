from gym.envs.registration import register
from .envs import(toh_env)

register(
    id='toh-v0',
    entry_point='toh_gym.envs:TohEnv',
    kwargs={},
)
