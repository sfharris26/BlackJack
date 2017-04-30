import numpy as np

# The state class keep track of the agent's hand total, whether or not the agent has a soft ace (one that
# could be reassigned a value of 1 if needed), and the card shown by the dealer

# There is a translate function for converting the state to an integer code that is used
# for array indexing


class State:
    def __init__(self):
        self.dealerShow = 0  # 2 through 11
        self.agentTotal = 0  # 12 through 20
        self.agentSoftAce = 0  # 0 or 1
        self.dealerSoftAce = 0  # 0 or 1
        self.dealerTotal = 0

    def initialize(self):
        self.agentTotal = 0  # 12 through 20
        self.dealerShow = self.get_card()
        self.dealerTotal = self.dealerShow
        while self.agentTotal < 12:
            card = self.get_card()
            self.add_agent_card(card)

    # Add a card to the agent's hand
    def add_agent_card(self, card):
        self.agentTotal += card
        if card == 11 and self.agentSoftAce == 0:
            self.agentSoftAce = 1
        if self.agentTotal > 21 and self.agentSoftAce == 1:
            self.agentSoftAce = 0
            self.agentTotal -= 10

    # Add a card to the dealer's hand
    def add_dealer_card(self):
        self.dealerTotal += self.get_card()

    # Get the array index that corresponds to this state
    def get_state_index(self):
        if self.agentTotal >= 21:
            return -1
        index = (self.dealerShow-2) * 18
        index += (self.agentTotal-12) * 2
        index += self.agentSoftAce
        return index

    # Get a card from 2 to ace. We really just care about the total so the chances of getting a 10 are 4x higher than the other cards
    def get_card(self):
        card = np.random.randint(2, 15, None)
        if card >= 11 and card <= 13:
            card = 10
        if card == 14:
            card = 11
        return card

    def get_agent_total(self):
        return self.agentTotal

    def get_dealer_total(self):
        return self.dealerTotal

    @staticmethod
    def to_string(index, delimiter):
        agentSoftAce = index % 2
        index = (index - (index % 2))/2
        agentTotal = index % 9 + 12
        index = (index - index % 9)/9
        dealerShow = index + 2
        return str(dealerShow)+ delimiter + str(agentTotal) + delimiter + str(agentSoftAce)

    @staticmethod
    def translate_to_state_index(dealer_show, agent_total, agent_softace):
        index = (dealer_show-2) * 18
        index += (agent_total-12) * 2
        index += agent_softace
        return index
