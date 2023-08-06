Brutal Maze is a fast-paced hack and slash game which aims to bring players a
frustrating, horror-like experience. It tries to mimic real-life logic in a way
that truly represents our loneliness, mortality and helplessness in the
universe.

The game features a solitary hero in a trigon shape who got lost in world of
squares. Unlucky for him (or her, who can tell the gender of a trigon anyway),
the squares have no intention to let their visitor leave in peace. Together,
they form a greater being called The Maze. Naturally, The Maze is dynamically
and infinitely generated. As our poor hero tries to find a way out, it releases
its minions (we will call them *enemies* from here) to stop him. Since The Maze
*sees it all* and *knows it all*, it keeps creating more and more enemies for
the hero to fight. It also keeps track of which type of squares can do most
damages to our trigon, in order to send out the most effective belligerents.

Your mission is to help the hero go the furthest distance possible, while
fighting those aggressive enemies. Extra information below will give you a
better understanding of what you fight and how you fight them.

## Hero

The hero is a regular [trigon](https://www.pygame.org/docs/ref/gfxdraw.html#pygame.gfxdraw.aatrigon)
in Aluminium color (from the [Tango palette](http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines#Color_Palette)).
He's multitasking, which means he has the ability to attack and move (both
horizontally and vertically) simultaneously. However, close- and long-range
attacks can't be stricken at the same time. When swinging his blade, our hero
may also avoid getting damages caused by enemies' bullets.

Like heroes in other hack and slash games, the trigon can heal too, but irony,
his HP recovery rate decreases as he gets wounded. Been warned you have,
bravery will only give you regrets.

## Enemies

Enemies are put into hibernation and blend into The Maze at the time of their
creation. When the hero comes across, they become awake and show their
(physical) colors. Enemy of each color has an unique power as described below:

1. *Butter*: May strike critical hits.
2. *Orange* (also known as *Agent Orange*): May prevent the hero from healing
   or blocking bullets. Poisoned hero will be drawn as a square.
3. *Chocolate* (a.k.a. *MDMA in Disguise*): May make the hero high and shoot
   uncontrollably. Still, Chocolate is good for your health (and so is MDMA).
4. *Chameleon*: become invisible, only shows itself when attacking or being
   attacked.
5. *Sky Blue* (a.k.a. *Lightning Sky*): May immobilize the hero. If this happen
   our hero can only see the enemies, including Chameleons, on a blank
   background. What a blessing in disguise!
6. *Plum* (a.k.a. *Plum Wine*): May replicate. Very quickly.
7. *Scarlet Red* (a.k.a. *Vampire's Eye*): Moves faster and drains hero's HP.

The possibility that an enemy attack with its special power increases when it's
able to prove its effectiveness to The Maze. In other words, the more a kind of
enemy hit the hero, the more chance they *may* use their unique abilities.
Lucky for you, squares are unitasking so they have to stop moving to perform
attacks. This slows them down a bit, however the ones which fall off the
display will respawn elsewhere in The Maze.

## Attacks

In this game, attack's damage is contingent on the distance between the
attacker and its target. The closer they are, the more damage caused. There is
at least an one-third-second delay between two attacks of any character.

### Long-range attacks

While projectiles are often called *bullets* in the code and the documentation,
they are more similar to stones propelled by slingshots, as they don't fly very
far (about 6 times the width of an enemy). Those fired by enemies can fly
though walls but the ones shot by the hero turn the grid into a new enemy.
A bullet is counted as hitting the target when the distance between the center
of the two object is less than the circumradius of a cell.

### Close-range attacks

It is needless to explain any further on how this kind of attack works, so we
only provide the size of the characters for you to calculate when the strike
can wound the target. To do so, the attacker must *touch* its opponents, or
simplistically, the distance between the central points of the two characters
must not be any greater than the sum of their circumradiuses. Do the
calculations yourself, a square's side is a fifth of the walls', and covers the
same area as a trigon.

Specially, hero's closed-range attacks also block opponents' bullets. If this
happens, the hero won't be able to attack in the next turn.

### Manual slashing

As the hero always follow the mouse, he perform close-range attack while doing
so. Unlike the automatic ones, there isn't any delay between two manual
slashings.
