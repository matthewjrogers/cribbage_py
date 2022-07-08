# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:15:22 2022

@author: mattr
"""

from game_object import Game

if __name__ == '__main__':
    # get the number of games to simulate
    while True:
      try:
        n = int(input("Number of games to simulate (Integer): "))
        break
      except ValueError:
          print("Please input an integer only...")  
          continue
    
    # get the risk sensitivity of player 1
    while True:
      try:
        inp = input("Player 1 risk tolerance (0 if empty): ")
        
        if len(inp) == 0:
            p1_tol = 0
        else:
            p1_tol = float(inp)
        break
      except ValueError:
          print("Please input a number between 0 and 4 only...")  
          continue
     
    # get the risk sensitivity of player 2
    while True:
      try:
        inp = input("Player 2 risk tolerance (0 if empty): ")
        
        if len(inp) == 0:
            p2_tol = 0
        else:
            p2_tol = float(inp)
        break
      except ValueError:
          print("Please input a number between 0 and 4 only...")  
          continue
      
    # n = int(input("Number of games to simulate: "))
    monte_carlo = Game(p1_tol, p2_tol)
    
    monte_carlo.simulate(n)
    
    print(f"P1 Win Percentage is {(monte_carlo.winner.count(1)/len(monte_carlo.winner)) * 100}% ")
    print(f"P1 scored an average of {sum(monte_carlo.p1_cribs)/len(monte_carlo.p1_cribs)} cribs over {n} games")
    print(f"P2 scored an average of {sum(monte_carlo.p2_cribs)/len(monte_carlo.p2_cribs)} cribs over {n} games")