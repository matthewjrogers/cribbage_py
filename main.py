# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:15:22 2022

@author: mattr
"""

from game_object import Game

if __name__ == '__main__':
    n = int(input())
    monte_carlo = Game()
    
    monte_carlo.simulate(n)
    print(f"P1 Win Percentage is {(monte_carlo.winner.count(1)/len(monte_carlo.winner)) * 100}% ")
    print(f"P1 scored an average of {sum(monte_carlo.p1_cribs)/len(monte_carlo.p1_cribs)} cribs over {n} games")
    print(f"P2 scored an average of {sum(monte_carlo.p2_cribs)/len(monte_carlo.p2_cribs)} cribs over {n} games")