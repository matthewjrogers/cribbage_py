#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:49:30 2020

Helper functions for cribbage simulation

@author: Matt Rogers
"""

from itertools import combinations
from typing import Optional
from deck_and_card_objects import Card

def score_hand(hand, cut_card : Optional[Card]) -> int:
    """
    

    Parameters
    ----------
    hand : Hand
        A Hand of Cards.
    cut_card : Optional[Card]
        Cut card if using for final scoring.

    Returns
    -------
    int
        Score for the combined hand and optional cut card.

    """
    score = 0
    # flush check
    if sum((c[2] == hand[0][2] for c in hand)) == len(hand):
        
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

    score += sum(combns)*2

    # count pairs
    score += sum((c[0].rank == c[1].rank for c in combinations(hand, 2)))*2

    # score runs
    score += score_runs(hand, None)
    
    return score

def score_runs(stack, card: Optional[Card]) -> int:
    """
    

    Parameters
    ----------
    stack : Hand
        Collection of cards, representing either a hand or a pegging pile.
    card : Card
        An optional .

    Returns
    -------
    int
        Score for all runs in the collection of cards, or 0 if none present.

    """
    # runs require at least two cards in the stack
    if len(stack) < 2:
        return 0
    
    else:
        full_stack = sorted(stack + [card]) if card is not None else sorted(stack)

    score = {'rl' : 1, 'mult' : 1, 'pairs' : set()}
    
    for i, j in zip(range(0, len(full_stack)-1), range(1, len(full_stack))):
        if full_stack[i].rank == full_stack[j].rank:
            score['pairs'].add(full_stack[i].rank)
            score['mult'] += 1
        elif full_stack[j].rank - full_stack[i].rank == 1:
            score['rl'] += 1
        else:
            if score['rl'] < 3:
                score['rl'] = 1
            else:
                break
    if score['rl'] < 3:
        score['rl'] = 0
    
    if len(score['pairs']) == 2:
        score['mult'] += 1
        
    return score['rl'] * score['mult']


        
def score_peg(card, peg_pile) -> int:
    """
    

    Parameters
    ----------
    card : Card
        The card being played
    peg_pile : Hand
        A collection of cards already played in pegging.

    Returns 
    -------
    int
        An integer, representing the score for the card played onto the pegging pile.

    """
    peg_score = 0

    if len(peg_pile) > 0 and peg_pile[-1].rank == card.rank:

        if len(peg_pile) >= 3 and all([c == peg_pile[-1] for c in peg_pile[-3:]]):

            peg_score += 12

        elif len(peg_pile) >= 2 and all([c == peg_pile[-1] for c in peg_pile[-2:]]):

            peg_score += 6

        else:

            peg_score += 2
    
    peg_score += score_runs(peg_pile, card)

    if sum([c.rank for c in peg_pile]) < 15 and (card + sum(peg_pile)) == 15:

        peg_score += 2

    if (card + sum([c.rank for c in peg_pile])) == 31:
        
        peg_score += 2
        
    return peg_score