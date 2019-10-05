# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 17:57:39 2019

@author: mouse
"""
import numpy as np
from Env import env
import random as rd


class Egreedy_MC_agent():
    def __init__(self):
        self.N = np.zeros((11,22,2))  # dealer's first card, player's sum, action
        self.Q = np.zeros((11,22,2))
        self.N0 = 100
    def act(self,state):
        if state == None:
            return 0
        dealerFirstCard = state.dealerFirstCard().num*state.dealerFirstCard().sign
        sumOfmine = state.sumOfmine()
        epsilon = self.N0/(self.N0+self.N[dealerFirstCard,sumOfmine,1]+self.N[dealerFirstCard,sumOfmine,0])
        random = rd.random()
        if random < epsilon: # explore
            explore_rand = rd.random()
            if explore_rand > 0.5:
                return 1
            else:
                return 0
        else: # exploit 
            if self.Q[dealerFirstCard,sumOfmine,1] > self.Q[dealerFirstCard,sumOfmine,0]:
                return 1
            else:
                return 0
    def learn(self,episode,reward):
        # episode is a list of two list, state list and action list
        
        state_list = episode[0]
        action_list = episode[1]

        for i in range(len(state_list)):
            dealerFirstCard = state_list[i].dealerFirstCard().num*state_list[i].dealerFirstCard().sign 
            sumOfmine = state_list[i].sumOfmine()
            action = action_list[i]
#            s = self.Q[dealerFirstCard,sumOfmine,action]*self.N[dealerFirstCard,sumOfmine,action] + reward
            
            self.N[dealerFirstCard,sumOfmine,action] += 1
            alpha = 1/self.N[dealerFirstCard,sumOfmine,action]
            self.Q[dealerFirstCard,sumOfmine,action] = self.Q[dealerFirstCard,sumOfmine,action] + alpha*(reward - self.Q[dealerFirstCard,sumOfmine,action])
#            self.Q[dealerFirstCard,sumOfmine,action] = s/self.N[dealerFirstCard,sumOfmine,action]
        return


if __name__ == '__main__':
    env = env()
    agent = Egreedy_MC_agent()
    
    reward = 0
    iteration = 50000
    
    reward_list = []

    for i in range(iteration): 
        reward = 0
        state_list = []
        action_list = []
        if i == 0:
            state = env.init_state() 
        else:
            state = env.Restart()
            print('########',env.terminal)
        print('dealer\'s first card',state.dealerFirstCard().num)

        while state != None:
            print('sum=' , state.sumOfmine())
            print('reward:',reward)
            
            action = agent.act(state)
            if state != None:
                state_list.append(state)
                action_list.append(action)
            state,reward = env.step(state,action)
        print('reward:',reward)
        print('episode ends')
        print()
        reward_list.append(reward)
        episode = [state_list,action_list]
        agent.learn(episode,reward)
    Q = agent.Q
    V = np.sum(Q,axis=-1)[1:10,1:22]
