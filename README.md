# Python RPG Game - Assualt Of Power

## Overview
This is a text-based RPG game created with python. To store game data, this project uses a .db file with sqlite3 in python to manipulateit. I created this game in year 10 as an introduction to objects and data storage in python. 

## Game Features
### Overview
- Account Creation
- Character Creation
- Character Inventory
- Character Stats
- Stage and Difficulty Progression
### Account Creation
To first play the game you need to create an account, requiring you to enter a username and password. This account will store all of your game characters. The process of creating this account is outlined in the *Begin Playing* section.

### Character Creation
In this game, you are able to have multiple characters on the one account. Additionally, you are able to select a character name, race and class during the character creation process. 

## Character Inventory
In this game, you are able to receive gear drops as you play, increasing your character stats. There are a number of possible gear types including: helmets, weapons, chest pieces and amulets. All of these gear drops can have different rarities which decide the stat boosts that come from equiping the gear, aswell as its coin value. The chance of getting a gear drop is normally 40% but if the enemy killed is a boss, it is increased to 60%. As the player is advancing the stages, the chance of getting a gear drop of a higher rarity is increased. For example, when the player is on stage 1, it is impossible to gain a gear piece of a legendary rarity.

## Character Stats
The levelling system in my program is quite simple. When the player levels up they gain a skill point which they can allocate to either strength (Damage), vitality (Health points) or speed (Who attacks first). The amount of XP rewarded for killing an enemy is increased based on the stage the user is on. The amount of XP required to level up increases based on the player level. To calculate xp requirements for the current player level I used the formula:
$$XP = 50 * 1.2^Level$$    

## Stage and Difficulty Progression
The difficulty scaling in my game is quite simple. The enemy HP and damage output are increased with every stage. The enemy’s attack is $$13 + 0.7*stage$$ and the enemy’s HP is $$68 + 1 * stage$$ This increases the game difficulty as the user advances the stages.

## Setup
To install this game, simply clone the repo to your computer and run the python file. To manage the .db files, this project uses sqlite3 which is a part of the python standard library, so no need to install anything extra. Upon the first time running the .py file, a main.db file will be created, containing all of the sql tables required to play the game.

## Begin Playing
To play the game for the first time, follow the *setup* guide. Once the file is on your computer and running, create an account. This will require you to enter a username and a password, aswell as confirming said password. Once this account was created, you need to login and create your first character. Upon creating a character, you have the following options:  
- Character Name
- Character Race
- Character Class

Once you have created a character, select this character from the main menu and begin playing.