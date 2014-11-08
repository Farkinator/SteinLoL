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
DoT's don't normally stack. If it is a DoT, the duration of the DoT is added to the cooldown
in a 1v1 situation.

Teamfight scenario or 1v1?:
	* 

AoE DoT (Lookin at you, Tormented Soil/Absolute Zero): an interesting problem. Will get to it on Sunday.
Three profiles(?):
	* Optimistic: full duration, enemies stand in it the AoE for full duration
	* Realistic: Half duration :)
	* Mean: minimum duration (1 tick). You missed big-time, bub.





=============================== LICENSE ====================================

MIT. I hope no one plagiarizes me, that wouldn't be cool (FINGERS CROSSED KIDS)


-DAVID STEINER (THEFARKINATOR)