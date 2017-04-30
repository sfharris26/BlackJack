import bj_environment as bje
import bj_bayesian_agent as bjbayes
import bj_state as bjsta
import copy as copy
import datetime as datetime

# Main file for running Agent/Environment interactions

# General Thompson Sampling Algorithm
# initialize
# for t in range(timesteps):
#   agent.determine_action
#   environment.get_reward
#   agent.update
# results

# Constants
total_states = 10*9*2  # 10 possible dealer show, 9*2 possible agent totals needing decision (total of 12-20 with or without ace)
time_steps = 50000
agent_a=1  # Prior beta params for Bayesian agent
agent_b=1

# Writing debug files
save_params_n = [500, 2000, 20000, 50000]
# If we save all the parameters for all possible states, that would be 760 columns. So just select a particular state to
#   investigate over time
tmp_dealer_card = 9;
tmp_agent_total = 15;
tmp_agent_softace = 0;
save_params_state_idx = bjsta.State.translate_to_state_index(tmp_dealer_card, tmp_agent_total, tmp_agent_softace)

datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
bayes_params_file = "C:\\Temp\\blackjack_bayes_params_" + datestr + ".txt"
bayes_reward_file = "C:\\Temp\\blackjack_bayes_reward_" + datestr + ".txt"
file_params = open(bayes_params_file, "w")
file_reward = open(bayes_reward_file, "w")

# Initialize total reward, one sum per agent
tot_reward = 0

# Initialize environment and agents
state = bjsta.State()
env = bje.Environment()
bayes = bjbayes.BjBayesianAgent(total_states=total_states, prior_a=agent_a, prior_b=agent_b)

# Loop through single game for the Bayesian agent
for t in range(time_steps):
    # Initialize variables
    state.initialize()
    actionList = []
    stateList = []
    action = 1   # Hit me!

    while action == 1:
        action = bayes.determine_action(possible_actions=None, state=state)
        actionList += [action]
        stateList += [copy.copy(state)]
        if action == 0:  # Stay
            env.finish_dealer_hand(state)
        else:
            state.add_agent_card(state.get_card())

    reward = env.get_reward(action=action, state=state, next_state=None)
    if reward > -1:  # -1 is a push so we just ignore it completely
        # Update all the agent decisions from this hand with a 0/1 reward.
        # Early on in the learning process, there will be some negative bias in the "hit" decisions because
        #  a good "hit" decision may be followed by a really stupid "hit" decision in the same hand
        bayes.update_reward_beliefs(actionList=actionList, stateList=stateList, reward=reward)
        tot_reward += reward

    if (t + 1) in save_params_n:
        bayes.write_posterior_params(t + 1, save_params_state_idx, file_params)

# Close the debug file
file_params.close()
file_reward.close()

# Print the total rewards for the agent
print ("Total reward:", tot_reward)

# Print the final beta parameters for the agent
print("Bayesian posterior params:", bayes.get_reward_beliefs())

