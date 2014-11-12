-----------------------------------------------------
DAVID STEINER RIOT APPLICATION
-----------------------------------------------------
Hi, this is my spell efficiency cruncher, creatively named

SteinLoL.

========================================================================================
USAGE 
========================================================================================
Install python 2.7.8 and requests on your computer (requires pip to install)

I AM RUNNING 2.7.8, I APOLOGIZE IF THERE ARE ANY ERRORS, BUT THE PYTHON COMMUNITY
IS VERY DIVIDED ON WHICH VERSION PEOPLE SHOULD USE.

Python:
https://www.python.org/downloads/

Requests:
http://docs.python-requests.org/en/latest/user/install/#install

PIP:
https://pip.readthedocs.org/en/latest/installing.html

then run:

python steinLoL.py

Input cues should take it from there.
!!!!!!!!IMPORTANT!!!!!!
I want you to input CDR as a whole number, not a decimal.
That means, if you want 20% CDR, just input 20, NOT .2

========================================================================================
WHY PYTHON?
========================================================================================
A programmer has to be versatile, and has to know when to use what language. Python
has a great http request library (Requests), and dictionaries improve JSON parsing
exponentially. I'm not at my most comfortable in Python (compared to C/Lua), but the
advantages far outweigh my relative unfamiliarity with the language.


========================================================================================
EFFICIENCY? 
========================================================================================

I believe given the input of the problem (Solely AP, AD, and CDR), the focus
of my program should be on what spell uses the stats it's given most efficiently.

There's a whole lot of things that *could* be thrown in were the input different, 
but since the end result is a ratio that doesn't get improved by any of those stats
(Range, AoE, DoT, yadda yadda), these factors would cancel out. Gains are made on 
AP ratio, AD ratio, and cooldown.

So, let's talk about our two types of efficiency.

Damage efficiency: Simply Damage per second per
cost unit (mana/energy/heat/what-have-you):

d = damage
m = mana
c = spell casts.
	  BaseDamage(d/c) + ADcoefficient(d/AD) * AD + APcoefficient * AP
DPS=  ----------------------------
	             cooldown(s/c)
Dimensional analysis proves this a solid formula:

1 spell    |  300 Damage
20 seconds |  1 spell
^Inverse of Cool Down, which is seconds/spell
DE = DPS/cost, final unit of
Damage/(mana * seconds)



Stat efficiency (SE): What spell improves its DPS/mana
the most with these stats? Here's my equation:

DEi = Damage Efficiency improved by stats
DEo = Base Damage Efficiency

SE = DEi/DEo

The ratio DEi/DEo will tell us how well the stats affect
a certain spell. A high Stat Efficiency is a good thing.

========================================================================================
CONSIDERATIONS
========================================================================================

Dealing with Charges?
	* Some champions have abilities with low cooldown but a high recharge time
	so they can use abilities in a quick succession. I'm adding a penalty to all 
	their cooldowns. Penalty = RechargeTime/MaxAmt. For example, Corki's missiles
	would have a penalty of (8*cdr)/7.This means having high stacks and low
	recharge is better!

Twisted Fate's Pick a Card:
	* Pick a Card is super weird. Obviously I can't say its cooldown is only 6 seconds,
	that would be ludicrous. Abusing the nature of TF's Pick A Card and assuming perfect 
	play (Really, how hard is it to draw anymore? Back when GC was imba, sure, but now
	not so much.), it will take 0, 1, and then 2 cycles, each a second long. So, 1/3 of 
	the time it takes 0, 1, 2 seconds to pick the card you want. Meaning the average
	time to pick a card is 1 second.


I was going to add AoE/DoT considerations, but there's no way of reliably accessing
whether or not a spell is AoE or DoT other than sentence parsing, which I DEFINITELY
don't want to do for all 400-odd spells in the game. I won't waste your time like that.

========================================================================================
SUGGESTIONS/BUGS
========================================================================================
So, I ran into some challenges using the API. Here are some things I would like
to improve on should I get the chance:

	* Improve Documentation on the website
	* Add programmatic access for duration fields and AoE targeting.
		- The best way I see to do this (That is, without interrupting the
		structure of the JSON all that much) is changing the positions of 
		certain values in the effect array to correspond with the 
		[leveltip][label] elements. Or making a separate effect descriptor 
		array (Much more readable, but harder to bring everything up to parity)
	* Frequently there are mystery numbers in the "effects" array. Examples:
		- 200/300/400 KarthusRequiem {{e2}} - probably the old mana cost
		- 80/110/140/170/200 ThreshQ{{e3}} - the old, pre-buff damage
		- 1/1.25/1.5/1.75/2 ThreshQ {{e2}} - Duration being changed soon?
		- 4/4/4/4 Lunar Rush {{e1}} - I legitimately don't know what this is
		- 110/115/120/125/130 {{e2}} and 6/6/6/6/6 {{e3}} Excessive Force
	* Riftwalk's tooltip is completely bugged. It doesn't indicate that it scales
	with mana at all. There used to be AP scaling, but that got patched out.
	This tooltip bug has been here since March.
	* Corki's tooltip is also bugged, as his recharge should scale with levels.


I realize it may take some time to patch in some dependencies, but it's totally
worth it. The more consistent the API is, the cooler stuff people can do with it!

========================================================================================
LICENSE 
========================================================================================

MIT. I hope no one plagiarizes me, that wouldn't be cool (FINGERS CROSSED KIDS)


-DAVID STEINER (THEFARKINATOR). - www.homepages.rpi.edu/~steind5