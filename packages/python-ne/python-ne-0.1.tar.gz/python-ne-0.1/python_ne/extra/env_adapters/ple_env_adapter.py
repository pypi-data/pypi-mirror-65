from python_ne.extra.env_adapters.env_adapter import EnvAdapter
import random


class PleEnvAdapter(EnvAdapter):
    """Pygame learning env adapter"""

    def reset(self):
        self.env.reset_game()

    def step(self, action) -> (object, float, bool):
        observation = self.env.getGameState()
        reward = self.env.act(action)
        done = self.env.game_over()
        return observation, reward, done

    def get_n_actions(self) -> int:
        return len(self.env.getActionSet())

    def get_random_action(self):
        return random.choice(self.env.getActionSet())
