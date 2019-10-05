# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:51:36 2019

@author: mouse
"""
import random as rd

"""
action = {0(stick),1{hit}}
"""

class env():
    def __init__(self):
        self.terminal = False
        self.player_terminal = False
        self.dealerFirstCard = Card(int(10.0*rd.random()+1),1)
        self.dealer = dealer_agent(self.dealerFirstCard.num)
        player_first_card = Card(int(10.0*rd.random()+1),1)
        self.init_sumOfplayer = player_first_card.num*player_first_card.sign
        self.reward = 0
        return 
    def init_state(self):
        return State(self.init_sumOfplayer,self.dealerFirstCard)
    
    def step(self,state,action):
        if self.terminal == True:
            print('bug')
            return None,0
        
        self.dealerFirstCard = state.dealerFirstCard()
        current_sum = state.sumOfmine()
        
        # player's turn
        next_card = self.hit()
        term_sumOfmine = next_card.num*next_card.sign + current_sum
        if (action == 1) & (self.player_terminal == False):  # hit
            print('player hits:',next_card.num*next_card.sign)
            if (term_sumOfmine < 21) & (term_sumOfmine > 0):
                next_state = State(term_sumOfmine,self.dealerFirstCard)
                self.reward = 0
            else:   # player busts
                print('【player busts】')
                next_state = None
                self.reward = -1
                self.player_terminal = True
                return next_state,self.reward
        else: # stick
            print('player sticks')
            self.reward = 0
            next_state = State(current_sum,self.dealerFirstCard)
            self.player_terminal = True
            
        # dealer's turn
        next_card = self.hit()
        self.dealer.act(next_card)
        # dealer busts
        if self.dealer.isBust() == True:
            self.reward = 1
            print('【dealer busts】')
            return None,self.reward
        
        # stick judgement
        self.terminal = self.player_terminal & self.dealer.isTerminated()
        if self.terminal == True:
            self.reward = self.gameJudge(self.dealer.sumOfdealer(),next_state.sumOfmine())
            next_state = None
        return next_state,self.reward
    
    def Restart(self):
        self.terminal = False
        self.player_terminal = False
        self.dealerFirstCard = Card(int(10.0*rd.random()+1),1)
        self.dealer = dealer_agent(self.dealerFirstCard.num)
        player_first_card = Card(int(10.0*rd.random()+1),1)
        self.init_sumOfplayer = player_first_card.num*player_first_card.sign
        self.reward = 0
        return State(self.init_sumOfplayer,self.dealerFirstCard)
    
    def hit(self):
        next_card_num = int(10.0*rd.random()+1)
        next_card_sign = 1
        term = int(3.0*rd.random()+1)
        if term > 2:
            next_card_sign = -1
        else:
            next_card_sign = 1
        return Card(next_card_num,next_card_sign)
    
    def gameJudge(self,dealer_sum,player_sum):
        if dealer_sum > player_sum:
            reward = -1
            print('【dealer win】')
        else:
            if dealer_sum < player_sum:
                reward = 1
                print('【player win】')
            else:
                reward = 0
                print('【fair】')
        return reward

"""
act on state
"""
class dealer_agent():
    def __init__(self,first_card):
        self.dealer_sum = first_card
        self.terminal = False
        self.bust = False
        return
    def act(self,next_card):
        # return action
        if self.bust == True:
            return 0
        if self.dealer_sum < 17 and self.dealer_sum > 0:
            # hit
            print('dealer hits:',next_card.num*next_card.sign)
            self.dealer_sum += next_card.num*next_card.sign
            
            if self.dealer_sum > 21 or self.dealer_sum < 1:
                self.bust = True
            return 1
        self.terminal = True
        print('dealer sticks')
        return 0
    def sumOfdealer(self):
        return self.dealer_sum
    def isTerminated(self):
        return self.terminal
    def isBust(self):
        return self.bust
        

class State():
    def __init__(self,current_sum,dealerCard):
        self.current_sum = current_sum
        self.dealerfirstcard = dealerCard
        return
    def dealerFirstCard(self):
        return self.dealerfirstcard
    def sumOfmine(self):
        return self.current_sum


class Card():
    def __init__(self,num,sign):
        self.num = num
        self.sign = sign

    
if __name__ == '__main__': 
    env = env()
    state = env.init_state()   
    reward = 0
    print(state.dealerFirstCard().num)
    while state != None:
        print('sum=' , state.sumOfmine())
        print('reward:',reward)
        state,reward = env.step(state,1)

        