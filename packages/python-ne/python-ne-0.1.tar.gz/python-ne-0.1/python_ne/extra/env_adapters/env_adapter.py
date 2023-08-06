class EnvAdapter:

    def __init__(self, env, render=False):
        self.env = env
        self.render = render

    def reset(self):
        raise NotImplementedError('reset method must be implemented')

    def step(self, action) -> (object, float, bool):
        """must return observation, reward (float) and if done or not (bool)"""
        raise NotImplementedError('step method must be implemented')

    def get_n_actions(self) -> int:
        """must return number of actions of the current env"""
        raise NotImplementedError('get_n_actions method must be implemented')

    def get_random_action(self):
        """must return a random action"""
        raise NotImplementedError('get_random_action method must be implemented')
