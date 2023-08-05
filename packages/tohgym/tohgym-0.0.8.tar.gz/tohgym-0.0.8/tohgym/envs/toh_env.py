#!/usr/bin/env python
# coding: utf-8

# # Tower of Hanoi
import sys
from contextlib import closing

import numpy as np
from six import StringIO, b
from matplotlib import pyplot as plt
from gym import utils
from gym.envs.toy_text import discrete
import time
import pandas as pd
import random


class TohEnv(discrete.DiscreteEnv):
    """Tower of hanoi environment."""
    metadata = {'render.modes': ['human', 'ansi']}

    def apply_action(self, s, a):
        """Apply a move and generate the new state, if move is invalid, return None."""
        s = [list(i) for i in s]
        if len(s[a[0]]) == 0:
            # Invalid move
            return None
        to_move = s[a[0]][-1]
        source = a[0]
        dest = a[1]
        new_state = s[:]
        new_state[source].pop()
        new_state[dest].append(to_move)
        output = tuple([tuple(i) for i in new_state])
        return output

    def is_state_valid(self, s):
        """Checks if a state is valid."""
        s = [list(i) for i in s]
        for i in s:
            if i != sorted(i, reverse=True):
                return False
        return True

    def generate_all_states(self, initial_state):
        """Generate all the states for MDP, total number of states = number_of_poles**number_of_disks"""
        states = []
        states.append(initial_state)

        while True:
            old_len = len(states)
            for s in states:
                for action in self.action_list:
                    new_state = self.apply_action(s, action)
                    if new_state and new_state not in states:
                        if self.is_state_valid(new_state):
                            states.append(new_state)
            new_len = len(states)
            if old_len == new_len:
                break
        return states

    def categorical_sample(self, prob_n, np_random):
        """
        Sample from categorical distribution
        Each row specifies class probabilities
        """
        prob_n = np.asarray(prob_n)
        csprob_n = np.cumsum(prob_n)
        return (csprob_n > np_random.rand()).argmax()

    def reset(self):
        if self.default_reset:
            self.s = self.categorical_sample(self.isd, self.np_random)
            self.lastaction = None
            return self.s
        else:
            self.s = 0
            self.lastaction = None
            return self.s

    def __init__(self, initial_state=((2, 1, 0), (), ()), goal_state=((), (), (2, 1, 0)), noise=0, default_reset=True, neg_reward=0.0):

        self.initial_state = initial_state
        assert noise < 1.0, "noise must be between 0 and 1"
        self.goal_state = goal_state

        self.action_list = [(0, 1), (0, 2), (1, 0),
                            (1, 2), (2, 0), (2, 1)]

        self.all_states = self.generate_all_states(initial_state)

        self.nS = len(self.all_states)
        self.nA = len(self.action_list)
        self.neg_reward = neg_reward
        self.default_reset = default_reset
        self.desc = np.array(range(0, self.nS))

        # Maintaining mappings to make use of algorithms from frozen lake.
        # Used to get a state by index of an array instead of a tuple
        self.state_mapping = {}
        self.inverse_mapping = {}
        for i in range(len(self.all_states)):
            self.state_mapping[i] = self.all_states[i]
            self.inverse_mapping[self.all_states[i]] = i

        # Generating probability matrix
        self.P = {s: {a: [] for a in range(len(self.action_list))}
                  for s in range(len(self.all_states))}

        # For stochastic environment
        self.noise = noise
        for s in range(len(self.all_states)):
            for a in range(len(self.action_list)):
                li = self.P[s][a]
                if self.state_mapping[s] == self.goal_state:
                    li.append((1, s, 0, True))
                else:
                    if noise == 0:
                        done = False
                        new_state = self.apply_action(
                            self.state_mapping[s], self.action_list[a])
                        rew = 0
                        if new_state == None:
                            new_state = self.state_mapping[s]
                        if self.is_state_valid(new_state) == False:
                            new_state = self.state_mapping[s]
                            rew = neg_reward
                            done = True
                        if new_state == self.goal_state:
                            rew = 100
                            done = True
                        li.append(
                            (1, self.inverse_mapping[new_state], rew, done))
                    else:
                        for b in [(a, 1-noise), (random.choice(range(6)), noise)]:
                            a, prob = b[0], b[1]
                            done = False
                            new_state = self.apply_action(
                                self.state_mapping[s], self.action_list[a])
                            rew = 0
                            if new_state == None:
                                new_state = self.state_mapping[s]
                            if self.is_state_valid(new_state) == False:
                                new_state = self.state_mapping[s]
                                rew = neg_reward
                                done = True
                            if new_state == self.goal_state:
                                rew = 100
                                done = True
                            li.append(
                                (prob, self.inverse_mapping[new_state], rew, done))

        self.isd = np.array([self.is_state_valid(self.state_mapping[s])
                             for s in range(len(self.all_states))]).astype('float').ravel()
        self.isd /= self.isd.sum()

        super(TohEnv, self).__init__(self.nS, self.nA, self.P, self.isd)
