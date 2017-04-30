import agent as a
import bj_state as sta
import numpy as np

class BjBayesianAgent(a.Agent):
    # The agent will keep track of the probabilities of getting reward (beating the dealer)
    # for all the possible states and actions. Each state is a combination of the agent's total, the
    # dealer showing hand, and whether there is a high ace that assume a value of 1 if needed.
    # Actions are either hold or hit. There are no probabilities assigned if the agent's total is
    # less than 12 or is 21.
    # Each scenario is modeled with a Beta prior and a Binomial likelihood, yielding a Beta Posterior distribution
    # The Beta prior is specified by the arguments to the initialization here
    def __init__(self, total_states, prior_a, prior_b):
        a.Agent.__init__(self)
        #w, h = 10, 9;  # 10 possible dealer cards showing (10-King are the same), 9 possible values where decision is needed
        #Matrix = [[0 for x in range(w)] for y in range(h)]
        self.stay_prob = [0.] * total_states
        self.hit_prob = [0.] * total_states
        # Posterior distribution parameters for stay(0) and hit(1) for each possible state
        self.stay_posterior_a = [prior_a] * total_states
        self.stay_posterior_b = [prior_b] * total_states
        self.hit_posterior_a = [prior_a] * total_states
        self.hit_posterior_b = [prior_b] * total_states

    # Reward will be 0 or 1, this updates the posterior
    # Note this need to update rewards of more than one decision
    def update_reward_beliefs(self, stateList, actionList, reward):
        for i in range(len(stateList)):
            state = stateList[i]
            action = actionList[i]
            stateIdx = state.get_state_index()
            if stateIdx > -1:
                if action == 0:
                    self.stay_posterior_a[stateIdx] += reward
                    self.stay_posterior_b[stateIdx] += 1 - reward
                else:
                    self.hit_posterior_a[stateIdx] += reward
                    self.hit_posterior_b[stateIdx] += 1 - reward

    def determine_action(self, state, possible_actions):
        # Sample reward probabilities from reward_beliefs (posterior)
        if state.get_agent_total() == 21:
            return 0
        stateIdx = state.get_state_index()
        if stateIdx == -1 or stateIdx > 190:
            return 0
        self.stay_prob[stateIdx] = np.random.beta(self.stay_posterior_a[stateIdx], self.stay_posterior_b[stateIdx])
        self.hit_prob[stateIdx] = np.random.beta(self.hit_posterior_a[stateIdx], self.hit_posterior_b[stateIdx])
        if self.stay_prob[stateIdx] > self.hit_prob[stateIdx]:
            return 0
        else:
            return 1

    def get_stay_probs(self):
        return self.stay_prob

    def get_hit_probs(self):
        return self.hit_prob

    def get_reward_beliefs(self):
        returnValue = "Dealer show, Agent total, Soft ace, Stay a, Stay b, Hit a, Hit b\n"
        for i in range(len(self.stay_posterior_a)):
            returnValue += sta.State.to_string(i, ",")
            returnValue += ","
            returnValue += str(self.stay_posterior_a[i])
            returnValue += ","
            returnValue += str(self.stay_posterior_b[i])
            returnValue += ","
            returnValue += str(self.hit_posterior_a[i])
            returnValue += ","
            returnValue += str(self.hit_posterior_b[i])
            returnValue += "\n"

        return returnValue

    # Write the posterior params to the specified file in tab-delimited format
    def write_posterior_params(self, time, state_idx, file):
        file.write(str(time) + '\t' + sta.State.to_string(state_idx, "\t") + '\t')
        file.write(str(self.stay_posterior_a[state_idx]) + '\t' + str(self.stay_posterior_b[state_idx]) + '\t')
        file.write(str(self.hit_posterior_a[state_idx]) + '\t' + str(self.hit_posterior_b[state_idx]) + '\t')
        file.write('\n')
