15112 Term Project
Game Title: Townlet Engima
By: Iris Pan
Github repository: https://github.com/irisp34/112-Term-Project

Description: This game is a building and resource collection game. The premise 
is that the character must collect wood from trees in order to build a bridge to
the next island. New buildings can help the player advance in the game, but they
must also be aware of enemies which will spawn randomly. The player should be on
high alert! Collect resources and build a base on the main island, traveling to
other islands to collect additional resources.

Music used in tp video:  
Palms and Seagulls by Timecrawler 82
Song Sparrow Serenade (Instrumental) by Chad Crouch
Links to music:
https://freemusicarchive.org/music/Timecrawler_82/Osaka_Lights/Palms_and_Seagulls
https://freemusicarchive.org/music/Chad_Crouch/Field_Report_Vol_II_Reed_Canyon_Instrumental/Song_Sparrow_Serenade_Instrumental

How to run: The project can be run from main.py. With the current 10 x 10 island
set up, it will take approximately 15 seconds to fully load the game, but after
this point, it should run correctly. If the game is played normally and enemies
are not bumped into, when you click to exit the game, it will save automatically.
Upon running the program again, the version that was played on previously will
reload. If enemies are bumped into and the game ends, the resource.bin file 
(which stores all game play data and automatically writes back into the game 
upon reloading) will be deleted (when rerunning, a new game will start). If the
player desires a completely new game and the game has not ended, they should
locate the "resources.bin" file in the same place as all the code is and delete
this before rerunning. This ensures a fresh game.

Note: after running my game on a Mac (my primary computer) as well as a Windows
when my Mac was not accessible, I have found that the arrow keys are extremely
sensitive on the Windows (although I'm not sure if this is generalized across
all Windows computers). The game runs more properly on a Mac. 

Libraries: Pygame, numpy, pickle

Shortcut commands: No shortcut commands exist, but if you aim to build a factory
and farm first, this will give you a constant stream of resources that will help
you advance quicker in the game.


