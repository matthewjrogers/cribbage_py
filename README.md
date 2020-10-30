# cribbage_py
I really enjoy game simulations and the card game cribbage. I wanted to know if, assuming two players are equally skilled, getting the first crib in cribbage conferred an advantage and, if so, how large of an advantage. 

I had previously [written a simulator in Julia](https://github.com/matthewjrogers/julia_plays_cribbage) that was designed to figure out what cards perform best in the pegging phase of the game. Because the code in that simulator was rough and highly focused on the pegging process, I decided to write a cleaner and more reusable version in python to answer my question.

Over the course of 100,000 games, I found that the player with the first crib won 56% of the time. For a full summary of my findings, see [this post on my blog](http://www.unconquerablecuriosity.com/2020/10/30/the-compulsive-optimizers-guide-to-cribbage/)
