# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:11:59 2022

@author: mattr
"""
from deck_and_card_objects import Deck
from collections import deque
from functions import run_check

#%% function to create a hand
def make_hand(iterable):
    d = Deck()
    h = deque()
    h.extend([d.cards[i] for i in iterable])
    return h
    
if __name__ == '__main__':
    
    #%% check runs
    r0 = make_hand(range(0, 10, 2))
    r3 = make_hand([0, 1, 2, 11, 12])
    r4 = make_hand([0, 1, 2, 3, 12])
    r5 = make_hand(range(5))
    doublerun3 = make_hand([0, 1, 2, 11, 13])
    doublerun4 = make_hand([0, 1, 2, 3, 13])
    trip_run = make_hand([0, 1, 2, 13, 26])
    quad_run = make_hand([0, 1, 2, 13, 14])
    
    assert run_check(r0, None) == 0, "Error in no runs"
    assert run_check(r3, None) == 3, "Error in 1 run, length 3"
    assert run_check(r4, None) == 4, "Error in 1 run, length 4"
    assert run_check(r5, None) == 5, "Error in 1 run, length 5"
    assert run_check(doublerun3, None) == 6, "Error in 2 runs, length 3"
    assert run_check(doublerun4, None) == 8, "Error in 2 runs, length 4"
    assert run_check(trip_run, None) == 9, "Error in 3 runs, length 3"
    assert run_check(quad_run, None) == 12, "Error in 4 runs, length 3"

    print("All Checks Passed")