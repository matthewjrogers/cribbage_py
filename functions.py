#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:49:30 2020

Helper functions for cribbage simulation

@author: Matt Rogers
"""

def score_hand(hand, cut_card = None):
    score = 0
    # flush check
    if sum([c[2] == hand[0][2] for c in hand]) == len(hand):
        
        score += 4
        
        if cut_card != None and cut_card[2] == hand[0][2]:
            score += 1
    
    if cut_card != None:
        hand = hand + [cut_card]
        #hand.append(cut_card)
    
    # count fifteens
    combns = []

    for i in range(len(hand), 1, -1):
        combns.extend([1 for c in combinations(hand, i) if sum(c) == 15])

    score += len(combns)*2

    # count pairs
    score += sum([c[0].rank == c[1].rank for c in combinations(hand, 2)])*2

    # count runs
    combns = []

    for i in range(len(hand), 2, -1):
        combns.extend([sorted(c) for c in combinations(hand, i)])

    max_run_len = 3

    for c in combns:
        if all([b.rank - a.rank == 1 for a, b in zip(c[: -1], c[1 :])]):   
            if len(c) < max_run_len:
                break
            else:
                max_run_len = len(c)
                score += len(c)

    
    return score

def run_check(stack, card):
    
    # runs require at least two cards in the stack
    if len(stack) == 1:
        return [False, 0]
    
    else:
        full_stack = sorted(stack + [card])

    # a run is where, in a sorted hand of cards, all of the differences in card ranks == 1
    if all([b.rank - a.rank == 1 for a, b in zip(full_stack[: -1], full_stack[1 :])]):

        return [True, len(full_stack)]
    
    else:
        # if the stack is not a run, take the last len(stack)-1 elements and check again
        return run_check(stack[-(len(stack) - 1) : ], card)

        
def score_peg(card, peg_pile):
    peg_score = 0

    if len(peg_pile) > 0 and peg_pile[-1].rank == card.rank:

        if len(peg_pile) >= 3 and all([c == peg_pile[-1] for c in peg_pile[-3:]]):

            player_score += 12

        elif len(peg_pile) >= 2 and all([c == peg_pile[-1] for c in peg_pile[-2:]]):

            peg_score += 6

        else:

            peg_score += 2

    if len(peg_pile) >= 2 and run_check(peg_pile, card)[0]:

        peg_score += run_check(peg_pile, card)[1]

    if sum([c.rank for c in peg_pile]) < 15 and (card + sum(peg_pile)) == 15:

        peg_score += 2

    if (card + sum([c.rank for c in peg_pile])) == 31:
        
        peg_score += 2
        
    return peg_score