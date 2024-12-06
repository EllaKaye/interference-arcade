# Interference 

#### Video demo: URL (when recorded and uploaded!)
#### Description: A solitaire card game in Python

## About the game and name

This is a patience (or solitaire) game, 
where a deck of cards is shuffled and dealt into four rows of thirteen cards.
The Aces are then removed, leaving spaces. 
The aim is to sort each row into ascending order, from 2 to King, ending with a space, one row per suit, 
by moving cards into spaces, one at a time, according to the rules. 
See the ['How to Play'](#how-to-play) section below for full details of the rules and how to play.

I learnt this patience from my grandparents when I was young. 
In my family, we know it as "interference", 
because whenever anybody sits down to play, 
someone else comes and stands over their shoulder and interferes by suggesting what the next move should be.

I couldn't find any information about a patience called "interference"
and finally discovered (as I was writing this page) that it is actually known as [Gaps](https://en.wikipedia.org/wiki/Gaps). 
That said, to me (and in honour of my grandparents) it's still "interference" and
I'm sticking with that as the name of the game as I've built it here.

## How to play

- The aim is to arrange each row in ascending order, from 2 to King (followed by a space), one row per suit.
- At the start, the deck is shuffled and dealt into four rows of thirteen cards, then the Aces are removed to create spaces.
- Click on a card to select it, then click on a space to move it there, according to the following rules:
    - If there's a space at the beginning of the row, any 2 can go there.
    - Otherwise, you can only move a card into a space if it's the same suit and one rank higher than the card to the left of the space, e.g. only the 3S can be placed after the 2S, only the JH can be placed after 10H.
    - Nothing can go after a King, or after a space.
- The layout is blocked if there are no valid moves left, i.e. if all spaces are after Kings or other spaces.
- When the layout is blocked, you can start a new round, up to three rounds. For a new round, all the cards that are not yet arranged by suit in ascending order at the start of a row are collected, shuffled, and then dealt out again to fill the rows, leaving one space in each row, after the ordered cards (or a space at the start of the row, if it doesn't yet start with a 2).
- A new round can be triggered from the 'Round Over' screen, or at any time by pressing 'R'.
- Because there are up to four valid moves at any time, this version of patience/solitaire requires skill. You have a better chance of success if you think strategically. What's the sequence of consequences of each valid move? What card would you like to be able to move, and what other cards need to move to make that possible?
- The game ends when all rows are arranged in ascending order by suit, or when the third round is stuck.
- Toggle the instructions at any time by pressing 'I' (i.e. to return to the game if you were in the middle of one).
- Click to return to previous screen.
- A new game can be triggered at any time by pressing 'ENTER'.

## About the development history

I first learnt to code back in 2013 by taking an "Introduction to Programming" online course which taught Python by building simple games.
After the course, I wanted to challenge myself and so I made v1 of Interference, using the CodeSkultpur platform and the simplegui package (as we'd used in the course). It's still available to [play](https://py2.codeskulptor.org/#user51_AaJ8ZQvnxh3PPb7.py). The game is far more complex than anything we built during the course. It took me weeks to figure out the logic and the corresponding code and, at the time, I was really proud of it. Looking back on it now, it's definitely newbie code (limited understanding of classes, so many global variables!) The appearance also looks dated, simplegui is no longer developed, it's in Python 2, and the instructions have disappeared.

Several times over the last decade, as I've improved as a developer (primarily in R), I've thought about reworking the game as a way to learn new technologies. In particular, I considered Python 3, R Shiny or Observable JS, but it was never a priority.

This year (2024), I worked through weeks 1-5 of [CS50](https://cs50.harvard.edu/x/2024/), Harvard's excellent Introduction to Computer Science course, as part of the [C Study Group for R Contributors](https://contributor.r-project.org/events/c-study-group-2024/). I enjoyed it so much that I decided to complete the course, so I needed a [final project](https://cs50.harvard.edu/x/2024/project). I finally had a good reason to return to Interference.

## About the design choices

### Why Python?

I already had v1 of Interference in Python, which was obviously a useful starting point! (Though I ended up rewriting the game from scratch).

I have wanted for a while to learn modern Python. I very much enjoyed the [Python week of CS50](https://cs50.harvard.edu/x/2024/weeks/6/), and was particularly intrigued about what it is for code to be 'Pythonic'. The final project provided a great opportunity to bring my Python knowledge up-to-date. 

I did contemplate using Lua with LÖVE, as the CS50 final project page lists that as an idea for developing a game. 
I've been intrigued by Lua for a while because it's used for writing [Quarto extensions](https://quarto.org/docs/extensions/).
Ultimately, though, I thought that up-skilling in Python would be more useful.

### Why Python Arcade?

There are a number of [game engines for Python](https://realpython.com/top-python-game-engines/).
After much deliberation, I opted to use the [Python Arcade](https://api.arcade.academy/en/latest/) library. 
Their [solitaire tutorial](https://api.arcade.academy/en/latest/tutorials/card_game/index.html) was a great place to start. 

One notable difference between the way that I implemented Interference and the Solitaire tutorial 
is that I use clicking to move the cards around, rather than drag-and-drop as in the tutorial.
This is because, as I worked through the tutorial, I found drag-and-drop to be buggy in Arcade.
Moving cards around by clicking is more consistent (though does still occasionally freeze).

## About the use of LLMs

Since I'm submitting this as my final project for CS50, 
I've used LLMs in accordance with their policy:

> For your final project (and your final project only!) it is reasonable to use AI-based software other than CS50’s own (e.g., ChatGPT, GitHub Copilot, Bing Chat, et al.), but the essence of the work must still be your own. You’ve learned enough to use such tools as helpers. Treat such tools as amplifying, not supplanting, your productivity. But you still must cite any use of such tools in the comments of your code.

My main focus has been bringing the Python code I'd written 13 years earlier for v1 up-to-date. I didn't want an LLM to write any of the game code for me.
They were invaluable in other ways though. I used ChatGPT to ask about the most Pythonic way of achieving particular goals (providing it with the minimum context/example to get a useful response), and in doing so developed a much greater understanding of Python features like list comprehension and effective use of classes. I also used ChatGPT to help debug error messages, and for questions about the Arcade library. 

As I continued to work on the game, I started to prefer Claude.ai over ChatGPT, especially for code. In particular, I asked it for help with creating the different views for the game (i.e. the menu, instructions, round over and game over screens, in addition to the game itself), and how to switch between them, maintaining game state.

## About next steps

Although I have a working game, 
and I'm satisfied enough with it to submit it for my CS50 final project,
I haven't between particularly happy with the Python Arcade library.
I don't love the look of the game, particularly the text rendering.
I don't like that you can't responsively resize the window, 
nor that it is only playable on a computer.

For all these reasons, in retrospect, 
I wish I'd implemented a web browser-based version of Interference.
I've already made [good progress towards such a version](https://github.com/EllaKaye/interference), using [Shiny for Python](https://shiny.posit.co/py/) 
and I prefer it in every respect to this one. 
However, for a variety of reasons too tedious to go into here, 
I won't get round to finishing that implementation in 2024 
and it felt important to me to complete and submit the Arcade version this year.

## About me

I'm [Ella Kaye](https://ellakaye.co.uk). Professionally, I'm a Research Software Engineer at the University of Warwick, UK, 
working to foster a larger and more diverse community of contributors to base R. 
I also run [rainbowR](https://rainbowr.org), a community for LGBTQ+ folks who code in R.
For fun, I do things like this.

## Credits and code

Developed by: [Ella Kaye](https://ellakaye.co.uk)

GitHub: [EllaKaye/interference-arcade](https://github.com/EllaKaye/interference-arcade)

Version: 2.0.0 (September 2024)

License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en)
