#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:45:19 2020

Deck and card objects for cribbage simulation

@author: Matt Rogers
"""

from collections import namedtuple, deque
from itertools import combinations
import random

class Card(namedtuple('Card', ['rank', 'value', 'suit'])):
    """A tuple that represents playing cards in the form (RANK, VALUE, SUIT)."""

    SUITS = {
        'H': ['Hearts', '♥'],
        'C': ['Clubs', '♣'],
        'D': ['Diamonds', '♦'],
        'S': ['Spades', '♠']
    }

    RANKS = { 
        1: ['Ace', 'A'], 
        11: ['Jack', 'J'],
        12: ['Queen', 'Q'],
        13: ['King', 'K']
    }
    
    def __new__(cls, rank, value, suit):
        return tuple.__new__(Card, (rank, value, suit))

    def __eq__(self, other):
        if self.rank == other.rank and self.suit == other.suit:
            return True
        else:
            return False

    def __str__(self):
        if self.rank in self.RANKS:
            rank = self.RANKS[self.rank][1]
        else:
            rank = self.rank
        return '{}{}'.format(rank, self.SUITS[self.suit][1])

    def __add__(self, other):
        if isinstance(other, int):
            return self.value + other
        else:
            return self.value + other.value
        
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    
    __repr__ = __str__

class Deck(object):
    """An iterable collection of Card objects."""
    def __init__(self):
        super(Deck, self).__init__()
        self.cards = deque([Card(rank+1, value, suit) for suit in 'HCDS' for rank, value in enumerate([*range(1, 11), 10, 10, 10])])

    def __getitem__(self, index):
        '''Access a card by its index in the deck/hand'''
        return self.cards[index]

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        '''Return number of cards in the deck.'''
        return len(self.cards)

    def shuffle(self):
        '''Shuffle the deck in place.'''
        random.shuffle(self.cards)
        return

    def collect_cards(self, hand):
        '''Return cards to a deck from a list or Hand.cards'''
        for _ in range(len(hand)):
            self.cards.append(hand.pop())
            
    def deal(self):
        '''Return two six-card hands.'''
        hand1, hand2 = deque(), deque()
        for i in range(1,7):
            hand1.append(self.cards.pop())
            hand2.append(self.cards.pop())

        return [hand1, hand2]


class Hand(Deck):
    """A small Deck. Implements methods for hand selection and scoring. Fills role of player."""
    def __init__(self):
        super(Hand, self).__init__()
        self.cards = []
        self.hand_score = 0
        self.round_score = 0
        self.passed = False

    def __str__(self):
        return ' '.join(map(str, self.cards))
  
    
    def choose_hand(self, dealt_cards, crib):
        '''Select the highest scoring hand from the dealt cards'''
        hands = [c for c in combinations(dealt_cards, 4)]
        
        scores = deque()
        
        for hand in hands:
            scores.append(score_hand(hand)) 
        
        self.cards.extend([c for c in dealt_cards if c in hands[scores.index(max(scores))]])
        crib.cards.extend([c for c in dealt_cards if c not in hands[scores.index(max(scores))]])
        
        return
    
    def score_hand(self, cut_card):
        '''Score four card hand with cut card'''
        self.hand_score = score_hand(self.cards, cut_card)
    
    def peg(self, peg_pile):
        '''Choose card for pegging'''
        pos_plays = [c for c in self.cards if c + sum(peg_pile) <= 31]
        
        if len(pos_plays) == 0:
            self.passed = True
        else:
            points = [score_peg(c, peg_pile) for c in pos_plays]
            self.round_score += max(points)
            
            # choose the max point value
            play = pos_plays[points.index(max(points))]
            hand_idx = self.cards.index(play)
            peg_pile.append(self.cards.pop(hand_idx))
    
    __repr__ = __str__
