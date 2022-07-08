#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:48:37 2020

Game object for cribbage simulation

@author: Matt Rogers
"""
from collections import  deque
from deck_and_card_objects import Hand, Deck
from functions import score_hand, score_peg

class Game(object):
    def __init__(self, p1_tolerance = 0, p2_tolerance = 0):
        self.winner = deque()
        self.p1_tolerance, self.p2_tolerance = p1_tolerance, p2_tolerance
        self.p1_cribs = deque()
        self.p2_cribs = deque()

    def simulate(self, n_games):
        if len(self.winner) > 0:
            self.winner.clear()
        
        for _ in range(n_games):
            p1, p2, crib = Hand(), Hand(), Hand()
            p1.toggle_crib_player()
            d = Deck()

            winner = []
            p1_cribs = 0
            p2_cribs = 0

            crib_player = 1
            peg_pile = []

            while p1.round_score < 121 and p2.round_score < 121:
                # begin round

                # p1 is odd, p2 is even
                # if at the beginning of the loop we set the starting to turn to crib_player + 1,
                # then we know that p2 will always play first when it's p1's crib and vice versa

                turn = crib_player + 1


                d.shuffle()
                h1, h2 = d.deal()
                p1.choose_hand(h1, crib)
                p2.choose_hand(h2, crib)
                
                assert len(crib.cards) == 4, "Unexpected number of crib cards"
                assert len(p1.cards) == 4, "Unexpected number of crib cards"
                assert len(p2.cards) == 4, "Unexpected number of crib cards"
                
                cut_card = d.cards.pop()

                # peg
                while sum([len(p1.cards), len(p2.cards)]) > 0:
                    # if no one can play, empty the peg pile and reset passed flags
                    if p1.passed == True and p2.passed == True:
                        d.collect_cards(peg_pile)
                        p1.passed, p2.passed = False, False

                    if turn % 2 != 0:
                        p1.peg(peg_pile)

                        if p1.round_score >= 121:
                            winner.append(1)
                            break
                    else:
                        p2.peg(peg_pile)
                        if p2.round_score >= 121:
                            winner.append(2)
                            break

                    turn += 1

                if len(winner) > 0:
                    break

                # score hand and crib
                # TODO: remove code repetition here -- abstract to function
                if crib_player % 2 != 0:
                    p2.round_score += p2.hand_score
                    if len(winner) == 0 and p2.round_score >= 121:
                        winner.append(2)

                    p1.round_score += p1.hand_score
                    if len(winner) == 0 and p1.round_score >= 121:
                        winner.append(1)

                    p1.round_score += score_hand(crib.cards, cut_card)
                    p1_cribs += 1
                    if len(winner) == 0 and p1.round_score >= 121:
                        winner.append(1)

                else:
                    p1.round_score += p1.hand_score
                    if len(winner) == 0 and p1.round_score >= 121:
                        winner.append(1)

                    p2.round_score += p2.hand_score
                    if len(winner) == 0 and p2.round_score >= 121:
                        winner.append(2)

                    p2.round_score += score_hand(crib.cards, cut_card)
                    p2_cribs += 1
                    if len(winner) == 0 and p2.round_score >= 121:
                        winner.append(2)

                if len(winner) == 0:
                    crib.cards.append(cut_card)
                    d.collect_cards(crib.cards)
                    p1.passed, p2.passed = False, False
                else:
                    break
                p1.toggle_crib_player()
                p2.toggle_crib_player()
                crib_player += 1

            self.winner.append(winner[0])
            self.p1_cribs.append(p1_cribs)
            self.p2_cribs.append(p2_cribs)