# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 09:17:39 2019

@author: Dell
"""
import numpy as np
import random as rd
import math
import pickle
from Env import env


class Egreedy_Sarsa_agent():
    def __init__(self):
        self.N = np.zeros((11,22,2))  # dealer's first card, player's sum, action
        self.Q = np.zeros((11,22,2))
        self.N0 = 100
        self.lambdas = 0.5
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
            self.N[dealerFirstCard,sumOfmine,action] += 1
            alpha = 1/self.N[dealerFirstCard,sumOfmine,action]
            q_t = (1-self.lambdas)*math.pow(self.lambdas,len(state_list) - i)*reward
            self.Q[dealerFirstCard,sumOfmine,action] = self.Q[dealerFirstCard,sumOfmine,action] + alpha*(q_t - self.Q[dealerFirstCard,sumOfmine,action])
        return


if __name__ == '__main__':
    env = env()
    agent = Egreedy_Sarsa_agent()
    f = open('Q_prime.dat','rb')
    Q_prime = pickle.load(f)
    reward = 0
    iteration = 50000
    
    reward_list = []
    error_list = []

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
        Q_sarsa_term = agent.Q
        error = np.sum(np.square(Q_sarsa_term-Q_prime))
        error_list.append(error)
        reward_list.append(reward)
        episode = [state_list,action_list]
        agent.learn(episode,reward)
    Q_sarsa = agent.Q
    V_sarsa = np.sum(Q_sarsa,axis=-1)[1:10,1:22]
        
        
        
        
        
        
        
        
        
        
#        next_state,reward = env.step()
#        next_action = self.act(next_state)
#        dealerfirst = next_state.dealerFirstCard()
#        sumOfmine = next_state.sumOfmine()
#        alpha = 1/self.N(current_state.dealerFirstCard(),current_state.sumOfmine(),action)
#        for i in range()
#        self.Q(current_state.dealerFirstCard(),current_state.sumOfmine(),action) = self.Q(current_state.dealerFirstCard(),current_state.sumOfmine(),action) + 
#                    alpha*(reward + self.Q(dealerfirst,sumOfmine,next_action))
        

        
        
        