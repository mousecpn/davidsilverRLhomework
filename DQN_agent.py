# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:11:00 2019

@author: Dell
"""

from keras.models import Sequential
from keras.layers import Dense,Activation
#import keras.backend as K
import numpy as np
import random as rd
from Env import env

class DQN_agent():
    def __init__(self):
        self.Q = self.policyNet()
        self.Q_target = self.policyNet()
        self.Q.summary()
        self.Q_target.summary()
        
    def policyNet(self):
        model = Sequential()
        model.add(Dense(32,input_shape=(3,))) # input state{dealer's card,sum} and action
        model.add(Activation('relu'))
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dense(32))
        model.add(Activation('relu'))
        model.add(Dense(1))  # output a reward
        
        model.compile(optimizer='rmsprop',loss='mse',metrics=['mse'])
        return model
    

    
    def renew(self):
        for layer,layer_target in zip(self.Q.layers,self.Q_target.layers):
            self.Q_target.get_layer(layer_target.name).set_weights(self.Q.get_layer(layer.name).get_weights())  
        return
    
    def act(self,state):
        if state == None:
            return 0
        dealerFirstCard = state.dealerFirstCard().num*state.dealerFirstCard().sign
        sumOfmine = state.sumOfmine()
        epsilon = 0.05
        random = rd.random()
        x0 = np.array([dealerFirstCard,sumOfmine,0]).reshape(1,-1)
        x1 = np.array([dealerFirstCard,sumOfmine,1]).reshape(1,-1)
        
        if random < epsilon: # explore
            explore_rand = rd.random()
            if explore_rand > 0.5:
                return 1
            else:
                return 0
        else: # exploit 
            if self.Q.predict(x1) > self.Q.predict(x0):
                return 1
            else:
                return 0
    def Qmat(self):
        Q = np.zeros((11,22,2))
        for i in range(2): #action
            for j in range(11): # dealer's first card
                for k in range(22): # player's sum
                    X = np.array([j,k,i]).reshape(1,-1)
                    Q[j,k,i] = self.Q.predict(X)
        return Q
            
    


if __name__ == '__main__':
    env = env()
    agent = DQN_agent()
    
    reward = 0
    iteration = 500000
    batch_size = 25
    gamma = 1
    renew_step = 5
    step = 0
    maximum_memory = 1000
    
    reward_list = []
    transition_list = []
    
    for i in range(iteration):
        reward = 0
        if i == 0:
            state = env.init_state() 
            print('####### GAME',1,'#######')
        else:
            state = env.Restart()
#            print('########',env.terminal)
            print('####### GAME',i+1,'#######')
        print('dealer\'s first card',state.dealerFirstCard().num)
        
        while state != None:
            print('sum=' , state.sumOfmine())
            print('reward:',reward)
            
            action = agent.act(state)
            
            next_state,reward = env.step(state,action)
            transition = [state,action,reward,next_state]
            transition_list.append(transition)
            if len(transition_list) > maximum_memory:
                del(transition_list[0])
            
            size = min(batch_size,len(transition_list))
            sample_transition = rd.sample(transition_list,size)
            X = np.zeros((1,3))
            Y = np.zeros((1,1))
            for j in range(size):
                state_term,action_term,reward_term,next_state_term = sample_transition[j]
                x_term = np.array([state_term.dealerFirstCard().num,state_term.sumOfmine(),action_term]).reshape(1,-1)
                if next_state_term == None:
                    y_true = reward
                else:
                    y_true = reward + gamma*agent.Q.predict(x_term)
                y_true = np.array(y_true).reshape(1,-1)
                if j == 0:
                    X = x_term
                    Y = y_true
                else:
                    X = np.concatenate((X,x_term))
                    Y = np.concatenate((Y,y_true))
            agent.Q.train_on_batch(X,Y)
            state = next_state
            step += 1
            if step > renew_step:
                step = 0
                agent.renew()
        reward_list.append(reward)
    Q_DQN = agent.Qmat()
    V_DQN = np.sum(Q_DQN,axis=-1)[1:10,1:22]
                

            
                
            
            
            
