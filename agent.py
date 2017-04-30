
class Agent:
    '''
        Class for a simple Reinforcement Learning agent that can interact with the environment
        Rewards Earned - list of rewards earned at each time stamp (interaction with environment)
        Transition Beliefs - probability the agent believes of next state given state and action
        Reward Beliefs - reward the agent believes of state, action pair (Q-Values)
    '''
    def __init__(self):
        self.rewards_earned = []
        self.transition_beliefs = None
        self.reward_beliefs = None

    # Update the transition model
    def update_transitions(self, state, action, next_state):
        pass

    # Update the reward model
    def update_reward_beliefs(self, state, action, next_state, reward):
        pass

    # After taking an action, updating the agent's beliefs about the environment
    def update(self, state, action, next_state, reward):
        self.rewards_earned.append(reward)
        self.update_transitions(state, action, next_state)
        self.update_reward_beliefs(state, action, next_state, reward)

    # Action selection policy of agent using its current state and possible actions to determine what action to take
    # Essentially this will wrap over a policy, which maps states -> actions, to include exploit/explore dynamic
    def determine_action(self, state, possible_actions):
        pass