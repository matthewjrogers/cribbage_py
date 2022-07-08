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
from functions import score_hand, score_peg

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
        """
        

        Parameters
        ----------
        other : Card
            A card

        Returns
        -------
        bool
            Returns True if rank and suit match. Suit matching is important for hand selection.
            In general Q♥ == Q♣ == Q♦ == Q♠ (i.e. same rank). However, when selecting cards for the crib, this will lead to keeping
            additional cards and violates rules regarding number of crib and hand cards.
            
            In short, this looks wrong, but don't get rid of it because bad things

        """
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
    def __init__(self, crib_player = False, risk_tolerance = 0):
        super(Hand, self).__init__()
        self.cards = []
        self.tolerance = risk_tolerance
        self.crib_player = crib_player
        self.hand_score = 0
        self.round_score = 0
        self.passed = False

    def __str__(self):
        return ' '.join(map(str, self.cards))
  
    def toggle_crib_player(self):
        self.crib_player = True if not self.crib_player else False
        
    def choose_hand(self, dealt_cards, crib):
        '''Select the highest scoring hand from the dealt cards'''
        hands = [c for c in combinations(dealt_cards, 4)]
        throws = [0]*15
        risk = [0]*15
        
        for i in range(15):
            throws[i] = [c for c in dealt_cards if c not in hands[i]]
            
        # score all hands
        scores = [score_hand(h) for h in hands]
        
        # assess thrown cards for risk/opportunity
        for i in range(len(risk)):
            risk[i] += sum((c.value == 5 for c in throws[i])) # add one to risk for each 5
            risk[i] += 2 if sum([throws[i][0].value, throws[i][1].value]) == 15 else 0 # add 2 if throw is a 15
            risk[i] += 2 if throws[i][0].rank == throws[i][1].rank else 0 # add 2 if throw is a pair
            risk[i] += 1 if abs(throws[i][0].rank - throws[i][1].rank) == 1 else 0 # add 1 if throw is two consecutive numbers
            risk[i] += .5 if abs(throws[i][0].rank - throws[i][1].rank) == 2 else 0 # add .5 if throw is either end of a run of 3
            risk[i] += .25 if abs(throws[i][0].rank - throws[i][1].rank) == 3 else 0 # add .25 if throw is either end of a run of 4
            risk[i] += .25 if throws[i][0].suit == throws[i][1].suit else 0 # add .25 if throw could contribute to flush in crib

        # calculate risk sensitive scores
        # if it's not this player's crib, total score minus the difference betwee

        if not self.crib_player:
            risk_sensitive_scores = [s - 0 if (r - self.tolerance) < 0 else (r - self.tolerance) for s, r in zip(scores, risk)]  
        else:
            risk_sensitive_scores = [s + r for s, r in zip(scores, risk)]

        idx = risk_sensitive_scores.index(max(risk_sensitive_scores))
        
        self.cards.extend([c for c in dealt_cards if c in hands[idx]])
        crib.cards.extend([c for c in dealt_cards if c not in hands[idx]])
        self.hand_score = scores[idx]
        
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
