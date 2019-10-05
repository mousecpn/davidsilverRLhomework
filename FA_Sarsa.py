# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:37:51 2019

@author: Dell
"""
import numpy as np
import random as rd
import math
import pickle
from Env import env,State,Card

class Egreedy_Sarsa_agent():
    def __init__(self):
        self.W = np.zeros((36,1))
        self.lambdas = 0.5
    def act(self,state):
        if state == None:
            return 0
        X0 = self.state_transform(state,0)
        X1 = self.state_transform(state,1)
        epsilon = 0.05
        random = rd.random()
        if random < epsilon: # explore
            explore_rand = rd.random()
            if explore_rand > 0.5:
                return 1
            else:
                return 0
        else: # exploit 
            if np.dot(X1.T,self.W) > np.dot(X0.T,self.W):
                return 1
            else:
                return 0
    
    def learn(self,episode,reward):
        # episode is a list of two list, state list and action list
        state_list = episode[0]
        action_list = episode[1]        
        
        for i in range(len(state_list)):
            X = self.state_transform(state_list[i],action_list[i])
            Q = np.dot(X.T,self.W)
            q_t = (1-self.lambdas)*math.pow(self.lambdas,len(state_list) - i)*reward
            alpha = 0.01
            self.W += alpha*(q_t - Q)*X
        return
    
    def state_transform(self,state,action):
        X = np.zeros((3,6,2))
        dealerFirstCard = state.dealerFirstCard().num
        sumOfmine = state.sumOfmine()
        axis1 = []
        axis2 = []

        if dealerFirstCard <= 4:
            axis1.append(0)
        if (dealerFirstCard >= 4) & (dealerFirstCard <= 7):
            axis1.append(1) 
        if (dealerFirstCard >= 7) & (dealerFirstCard <= 10):
            axis1.append(2)
            
        if sumOfmine <= 6:
            axis2.append(0)
        if (sumOfmine >= 4) & (sumOfmine <= 9):
            axis2.append(1) 
        if (sumOfmine >= 7) & (sumOfmine <= 12):
            axis2.append(2)
        if (sumOfmine >= 10) & (sumOfmine <= 15):
            axis2.append(3)
        if (sumOfmine >= 13) & (sumOfmine <= 18):
            axis2.append(4)
        if (sumOfmine >= 16) & (sumOfmine <= 21):
            axis2.append(5)
        
        for i in range(len(axis1)):
            for j in range((len(axis2))):
                X[axis1[i],axis2[j],action] = 1
        X = X.reshape((36,1))
        return X
    
    def Q(self):
        Q = np.zeros((11,22,2))
        for i in range(2): #action
            for j in range(11): # dealer's first card
                for k in range(22): # player's sum
                    card = Card(j,1)
                    state = State(k,card)
                    X = self.state_transform(state,i)
                    Q[j,k,i] = np.dot(X.T,self.W)
        return Q
            


if __name__ == '__main__':
    env = env()
    agent = Egreedy_Sarsa_agent()
    f = open('Q_prime.dat','rb')
    Q_prime = pickle.load(f)
    reward = 0
    iteration = 10000
    
    reward_list = []
    error_list = []

    for i in range(iteration): 
        reward = 0
        state_list = []
        action_list = []
        if i == 0:
            state = env.init_state() 
            print('####### GAME',1,'#######')
        else:
            state = env.Restart()
#            print('########',env.terminal)
            print('####### GAME',i+1,'#######')
        print('dealer\'s first card',state.dealerFirstCard().num)
        
        while state != None:
            print('player\'s sum=' , state.sumOfmine())
            print('reward:',reward)
            
            action = agent.act(state)
            if state != None:
                state_list.append(state)
                action_list.append(action)
            state,reward = env.step(state,action)
        print('reward:',reward)
        print('episode ends')
        print()
        Q_sarsa_term = agent.Q()
        error = np.sum(np.square(Q_sarsa_term-Q_prime))
        error_list.append(error)
        reward_list.append(reward)
        episode = [state_list,action_list]
        agent.learn(episode,reward)
    Q_sarsa = agent.Q()
    V_sarsa = np.sum(Q_sarsa,axis=-1)[1:10,1:22]
        