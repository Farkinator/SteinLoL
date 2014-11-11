-----------------------------------------------------
DAVID STEINER RIOT APPLICATION
-----------------------------------------------------
Hi, this is my spell efficiency cruncher, creatively named

SteinLoL.

=================== USAGE ==================
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


================ EFFICIENCY? =================

To me, there are two types of efficiency when
we talk about spells. I'll call them damage
efficiency and stat efficiency. 

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


========================= HEURISTICS AND OTHER CONSIDERATIONS ==============

Dealing with Charges?
	* Where

(NOTE: THIS IS ONLY IF I HAVE TIME TO DO TEXT PARSING.)
DoT's don't normally stack. If it is a DoT, the duration of the DoT is added to the cooldown
in a 1v1 situation.

Teamfight scenario or 1v1?:
	* Hitting multiple heroes DEFINITELY increases your efficiency, just a question of 
	* 3 profiles: optimistic(2x the damage, 2 enemies hit), realistic (1.5x sometimes you hit 2,
	sometimes you hit 1. evens out.), and mean(1. At least you hit).

AoE DoT (Lookin at you, Tormented Soil/Absolute Zero): an interesting problem. Will get to it on Sunday.
Three profiles(?):
	* Optimistic: full duration, enemies stand in it the AoE for full duration
	* Realistic: Half duration :)
	* Mean: minimum duration (1 tick). You missed big-time, bub.

============================ SUGGESTIONS/BUGS ===================================
So, I ran into some challenges using the API. Here are some things I would like
to improve on should I get the chance:

	* Make the documentation and the JSON key/value pairs more usable.
	Currently there are some rules I found, but they're broken just enough times
	to be annoying, and there's little to no consistency outside of where to find
	the damage (PRIORITY: the "effect" array)
	* There is no "duration" field on some spells. Tormented Soil's duration, 
	for example, is not accessible programatically.
	* There is no way to programatically tell whether or not a spell does damage 
	over time or instantaneous damage.
	* Frequently there are mystery numbers in the "effects" array. Examples:
		- 200/300/400 KarthusRequiem {{e2}} - probably the old mana cost
		- 80/110/140/170/200 ThreshQ{{e3}} - the old, pre-buff damage
		- 1/1.25/1.5/1.75/2 ThreshQ {{e2}} - Duration being changed soon?
		- 4/4/4/4 Lunar Rush {{e1}} - I legitimately don't know what this is
		- 110/115/120/125/130 {{e2}} and 6/6/6/6/6 {{e3}} Excessive Force
	  Anyways, this could use some cleaning up.
	* Riftwalk's tooltip is completely bugged. It doesn't indicate that it scales
	with mana at all. There used to be AP scaling, but that got patched out.
	This tooltip bug has been here since March.


I realize it may take some time to patch in some dependencies, but it's totally
worth it. The more consistent the API is, the cooler stuff people can do with it!

=============================== LICENSE ====================================

MIT. I hope no one plagiarizes me, that wouldn't be cool (FINGERS CROSSED KIDS)


-DAVID STEINER (THEFARKINATOR)