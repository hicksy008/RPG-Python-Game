# Import libraries
import random
import sqlite3
import math
import time

# python -m trace --trace main.py
# CHECK1 for a progress check

# List of basic classes and races
classes = ['barbarian', 'crusader', 'monk', 'wizard',
           'demon hunter', 'witch doctor', 'necromancer']
races = ['Human', 'Elf', 'Dwarf', 'Halfling', 'Gnome', 'Half-Orc']


# Connecting Database and defining cursors
maindb = sqlite3.connect("main.db")
mainconn = maindb.cursor()

################################################
###############DATABASES FUNCTION###############
################################################

# Creates the login table in the login.db file


def logindbcreate():
    mainconn.execute(
        "CREATE TABLE LOGINDB(ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME varchar(12) NOT NULL, PASSWORD varchar(25) NOT NULL)")

# Create entry into the Login Database - uses username and password entered by the user


def logincreateentry(username, password):
    mainconn.execute(
        "INSERT INTO LOGINDB(USERNAME,PASSWORD) VALUES (?,?)", (username, password))
    maindb.commit()

# Creates the character table in the char.db file


def chardbcreate():
    mainconn.execute("CREATE TABLE CHARDB(ACCID INTEGER,ID INTEGER PRIMARY KEY AUTOINCREMENT,CHARNAME varchar(12) NOT NULL,RACE varchar(12) NOT NULL,CHARCLASS varchar(12) NOT NULL, LVL INTEGER NOT NULL,GOLD INTEGER,HELMET varchar(12) NOT NULL,CHEST varchar(12) NOT NULL,AMULET varchar(12) NOT NULL,WEAPON varchar(12) NOT NULL,STAGE INTEGER,CURRXP INTEGER,STRENGTH INTEGER,VITALITY INTEGER, SPEED INTEGER,SPOTIONS INTEGER,MPOTIONS INTEGER,LPOTIONS INTEGER)")

# Create a record into the Character Databases - uses the information entered in by the user, gives the user 5 small potions to start


def charactercreateentry(charname, racenum, classnum):
    global classes
    global races
    mainconn.execute("INSERT INTO CHARDB(ACCID,CHARNAME,RACE,CHARCLASS,LVL,GOLD,HELMET,CHEST,AMULET,WEAPON,STAGE,CURRXP,STRENGTH,VITALITY,SPEED,SPOTIONS,MPOTIONS,LPOTIONS) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (player.id, charname, races[racenum-1], classes[classnum-1], 1, 0, 'Not Equipped', 'Not Equipped', 'Not Equipped', 'Not Equipped', 1, 0, 0, 0, 0, 5, 0, 0))
    maindb.commit()

# Creates the inventory table in the Inv.db file


def invdbcreate():
    mainconn.execute("CREATE TABLE INVENTORY(GEARID INTEGER PRIMARY KEY AUTOINCREMENT,OWNER INTEGER,NAME varchar(12),TYPE varchar(12),RARITY varchar(12),EQUIP varchar(1),STAT INTEGER,GOLD INTEGER)")


# This is a function that tries to execute the functions to create the tables in the database files - If the table is already created, it ignores the error message
def dbcheck():
    try:
        logindbcreate()
        chardbcreate()
        invdbcreate()
    except:
        pass


# Executes the funciton above
dbcheck()

################################################
################CLASSES FUNCTION################
################################################

# This is the main character class


class Player(object):
    # This just lists all the class attributes
    def __init__(self):
        self.id = 0
        self.username = ''
        self.password = ''
        self.charid = 0
        self.charname = ''
        self.race = ''
        self.charclass = ''
        self.level = 1
        self.gold = 0
        self.helmet = ''
        self.chest = ''
        self.amulet = ''
        self.weapon = ''
        self.stage = 1
        self.xpreq = 0
        self.gearmul = -200
        self.hp = 175
        self.attack = 20
        self.attackmul = 1
        self.dead = 0
        self.speed = 0
        self.strength = 0
        self.vitality = 0
        self.spotions = 0
        self.mpotions = 0
        self.lpotions = 0

    # This defines what the class outputs when the user just enters the class (Instead of printing the memory location it prints this)
    def __str__(self):
        # Checks if the character has loaded in yet (0 is the initial charid)
        if charid == 0:
            print("Your character hasn't load in yet!")
        else:
            print("Your character is a Lv {} {} {}".format(
                self.level, self.race.title(), self.charclass.title()))


# Login Function that saves the username and password in a class

    def login(self):
        mainconn.execute('SELECT * FROM LOGINDB WHERE ID ="%s"' % (self.id))
        details = mainconn.fetchone()
        self.username = details[1]
        self.password = details[2]

# Class function that loads the character details into the class
    def charload(self, charid):
        # Searches the database for the information associated a specific charid
        mainconn.execute(
            'SELECT * FROM CHARDB WHERE ACCID ="%s" AND ID = "%s"' % (self.id, charid))
        details = mainconn.fetchone()
        self.charid = details[1]
        self.charname = details[2]
        self.race = details[3]
        self.charclass = details[4]
        self.level = details[5]
        self.gold = details[6]
        self.helmet = details[7]
        self.chest = details[8]
        self.amulet = details[9]
        self.weapon = details[10]
        self.stage = details[11]
        self.currxp = details[12]
        self.strength = details[13]
        self.vitality = details[14]
        self.speed = details[15]
        self.spotions = details[16]
        self.mpotions = details[17]
        self.lpotions = details[18]

    def mulcalc(self):
        # This is the gear multiplier that increases with the stage. This is done so it is impossible to get legendary gear at stage 1
        self.gearmul = -200 + (self.stage * 25)
        # This is the level progression. This is done so that the XP required to level up is greater as the character levels up
        self.xpreq = 50*1.5**self.level

    # Function that is used at the start of each battle
    def ready(self):
        # Sets the attack multiplier and HP to the default amount. This is done because if the user does multiple levels, he will have an unrealistic attack multiplier, which is stopped with these 2 lines
        player.attackmul = 1
        player.hp = 175
        # Simple list of the gear types which will be iterated through
        typelist = ['Helmet', 'Chest', 'Amulet', 'Weapon']
        # This checks the inventory database for any gear items that are equipped
        for type in typelist:
            mainconn.execute("SELECT * FROM INVENTORY WHERE TYPE = '%s' and equip = '%s' AND OWNER ='%s'" %
                             (type.title(), 'y', player.charid))
            equipment = mainconn.fetchall()
            # If equipment is not empty, execute the following code
            if len(equipment) != 0:
                # This checks if the item is a DMG buff item (increases player's damage output)
                if type == 'Weapon' or type == 'Amulet':
                    self.attackmul += equipment[0][6]
                else:
                    # This checks if the item is a HP buff item (increases player's total HP)
                    self.hp += equipment[0][6]
            # This adds 10 HP for every point of vitality that the player has
            self.hp += (self.vitality * 10)

    def attackgen(self):
        info = []
        # This adds 3 DMG for every point of strength the player has
        strengthbuff = player.strength * 3
        # Simple list in order to classify the type of hits
        dmgtypes = {
            'minimal': round(float(0.6*self.attack*self.attackmul+strengthbuff), 1),
            'weak': round(float(0.7*self.attack*self.attackmul+strengthbuff), 1),
            'nice': round(float(0.8*self.attack*self.attackmul+strengthbuff), 1),
            'great': round(float(0.9*self.attack*self.attackmul+strengthbuff), 1),
            'critical': round(float(1*self.attack*self.attackmul+strengthbuff), 1)
        }
        # This is a variable that calculates if the playe misses
        miss = random.randint(0, 9)
        # Calculates the 20% chance to miss
        if miss < 2:
            dmg = 0
            type = 'miss'
            # Appends the attack information to a list
            info.append(dmg)
            info.append(type)
        else:
            # Generates a random float between 60% and 100% of the players attack, float number is rounded to 1 decimal
            dmg = round(random.uniform(0.6*self.attack*self.attackmul +
                                       strengthbuff, self.attack*self.attackmul+strengthbuff), 1)
            # Appends the DMG that was just generated to the list
            info.append(dmg)
            type = ''
            # While loop that classifies the type of hit it will be
            found = False
            while found == False:
                for item in dmgtypes:
                    if int(dmg) <= dmgtypes[item]:
                        # If the damage classification is found, the loop breaks and continues the code
                        type = item
                        found = True
                        break
            # Appends the damge type to the list
            info.append(type)
        # Returns the damage information
        return info

    def checkdead(self):
        # This checks if the player's HP is lower than 0 (i.e they are dead)
        if self.hp <= 0:
            # If it is, the self.dead variable is set to 1, (This is used later in the program when the user is battling the enemy)
            self.dead = 1

    # Class function that updates the character's level, current xp and gold value based on the class attributes
    def updatefields(self):
        print(player.gold)
        mainconn.execute('UPDATE CHARDB SET LVL = "%s", CURRXP = "%s", GOLD = "%s",STRENGTH = "%s", VITALITY = "%s", SPEED = "%s" WHERE ID = "%s"' % (
            self.level, self.currxp, self.gold, self.charid, self.strength, self.vitality, self.speed))
        maindb.commit()

    # This finds the max possible HP of the player. This is done so that the player can't use potions to get an unrealistic amount of HP
    def findmaxhp(self):
        max = 175
        # Basic list of the HP affecting gear
        typelist = ['Helmet', 'Chest']
        for type in typelist:
            # for each item in the list it searches for an equipment piece is equipped
            mainconn.execute(
                "SELECT * FROM INVENTORY WHERE TYPE = '%s' and equip = '%s'" % (type.title(), 'y'))
            # Saves the query results as a variable
            equipment = mainconn.fetchall()
            # If query returned some results, add to the max variable
            if len(equipment) != 0:
                max += equipment[0][6]
        # Return max variable so It can be used in expressions
        return max

    def usepotion(self, amount):
        # This adds the potion heal amount to the player's HP
        player.hp += amount
        # Checks if the heal amount will take the player's HP over the max limit (This is done so that the player can't get an unrealistic amount of HP)
        if player.hp > self.findmaxhp():
            player.hp = self.findmaxhp()
        # This rounds up the player's HP (This is done to reduce math erros in the program)
        player.hp = math.ceil(player.hp)

# Opponent class (This is what the player battles during the game sequence)


class Opponent(object):

    # This is a list of all the opponent's attributes
    def __init__(self):
        self.race = ""
        self.attack = 0
        self.hp = 0
        self.dead = 0

    # This sets the player's race to match the stage race (self.race is printed throughout the game sequence)
    def racegen(self, race):
        self.race = race

    # This sets the player's HP and attack to a value that matches the player's current stage (HP and attack increases with stage levels)
    def regen(self, stage, num):
        self.attack = 13 + .7 * stage * num
        self.hp = 68 + 1 * stage * num
        self.dead = 0

    # This function is used to generate an attack value for the opponent
    def attackgen(self):
        info = []
        # This is a list for Damage classifications
        dmgtypes = {
            'minimal': round(float(0.6*self.attack), 1),
            'weak': round(float(0.7*self.attack), 1),
            'nice': round(float(0.8*self.attack), 1),
            'great': round(float(0.9*self.attack), 1),
            'critical': round(float(1*self.attack), 1)
        }
        # Variable that is used to calculate the chance for a miss
        miss = random.randint(0, 9)
        # There is a 20% chance to miss
        if miss < 2:
            dmg = 0
            type = 'miss'
            # Appends attack information to a list that will be used in the attack sequence
            info.append(dmg)
            info.append(type)
        else:
            # This generates an attack (60% of attack - 100% of attack)
            dmg = round(random.uniform(0.6*self.attack, self.attack), 1)
            info.append(dmg)
            type = ''
            # This loop is used to classify the type of attack is dealt (low DMG = weak hit)
            found = False
            while found == False:
                for item in dmgtypes:
                    if int(dmg) <= dmgtypes[item]:
                        type = item
                        found = True
                        break
            info.append(type)
        return info

    # This checks if the opponent is dead
    def checkdead(self):
        # If the opponent's HP is lower than or equal to 0, the opponent is dead
        if self.hp <= 0:
            self.dead = 1


# Makes instances of both classes (Player + Opponent)
player = Player()
oppo = Opponent()

################################################
################GENERAL FUNCTION################
################################################


# Checks if the password has a letter and a number
# lgd stands for login details
def checklgd(string):
    # Sets both variables to False
    letter = False
    number = False
    # Iterates through each character in the string in the functions parameters
    for character in string:
        # If the character is a letter, it sets letter to true
        if character.isalpha():
            letter = True
        # If the character is not a letter but a number, it sets number to true
        elif character.isdigit():
            number = True
    # Returns both variables to the main program so it can be used in expressions
    return letter and number

# Function that calculates the amount of spaces to organise data in a table


def spacer(num):
    result = ""
    # Adds a certain number of spaces to the result variable
    for i in range(num):
        # Add space to variable
        result = str(result) + " "
    # Returns to program so it can print that amount of spaces
    return result

################################################
################PROGRAM FUNCTION################
################################################

# Function that allows the user to create their account


def create():
    print("\nCreate an account")
    print("Username must be in-between 5 and 12 characters\nPassword must be a mix of numbers and letters and in-between 10 and 25 characters\n")
    while True:
        # Asks the user for a username. This username will be stripped(remove spaces) and made into lowercase
        username = input("Username:  ").lower().strip()
        if len(username) >= 5 and len(username) <= 12:
            # Query that checks if the username is in use
            mainconn.execute(
                'SELECT * FROM LOGINDB WHERE USERNAME ="%s"' % (username))
            # If the username is free break from the loop. If it isn't ask for another username
            if mainconn.fetchone() is None:
                break
            else:
                # tells the uesr that that username is already in use
                print("That username is already in use, please pick another one")
        else:
            print("Username must be in-between 5 and 12 characters")
    while True:
        # Asks the user for a password. ALl excess spaces will be removed on the sides
        password = input("Password:  ").strip()
        # The username must be at least 5 characters and at most 12 characters
        if len(username) > 12 or len(username) < 5:
            print("Username must be at least 5 characters but not over 12!")
        # The password must be at least 5 characters but not over 25 and it must contain a number(checklgd(password))
        elif len(password) > 25 or len(password) < 8 or checklgd(password) is False:
            print(
                "Password must be at least 8 characters but not over 25 and must contain a letter and number")
        # If the password meets the requirements, it will break from the loop
        else:
            break
    # This executes the function that is used to create a login entry (it uses username and password as its parameters)
    logincreateentry(username, password)
    print("\nYour account was successfully created!")
    # It goes back to the start page
    start()

# This is the function used to generate the rewards for killing an enemy


def loot(boss):
    # This is the list of all possi ble rarities
    # Blank is there so that I can relate the index of the rarity to their stats (hp(rarityindex) and hp(rarityindex - 1))
    raritylist = ['blank', 'common', 'rare', 'epic', 'legendary']
    # This is the type of items the user can get
    typelist = ['Helmet', 'Chest', 'Amulet', 'Weapon']
    # HP values that will be used with Helmet and Chest gear,
    hpnum = [25, 50, 100, 150, 200]
    # Damage numbers for weapons
    dmgnum = [0, 0.5, 1, 1.5, 2]
    # Damage numbers for amulets
    dmgnum2 = [0, 0.25, 0.5, 0.75, 1]
    # This is the value table (Randomised gear value based on its rarity)
    goldnums = [25, 50, 100, 150, 200]
    # Dictionary of all the possible gear names (This is done so that is easier to add more gear names)
    typetypelist = {
        'Helmet': ['crown', 'helmet', 'mask', 'priest mask'],
        'Chest': ['armor', 'armor', 'chainmail', 'robe'],
        'Amulet': ['core amulet', 'ornament', 'pendant', 'necklace'],
        'Weapon': ['Bloodscythe', 'Warhammer', 'dagger', 'flail', 'sword', 'longsword']
    }
    # This is the number used to see if the player will get a gear drop
    num = random.randint(0, 9)
    # 30% chance of a gear drop for normal enemy
    if boss == 'y':
        # If it is a boss, the chance for a gear drop will increase by 20%
        num + 2
    if num >= 7:
        # Decides what gear type it is
        type = random.choice(typelist)
        # This is the random number that will be used to decide rarity (player.gearmul is used so the player can't get legendary items at stage 1) The number starts as a negative
        raritynum = random.randint(0, 1000)+player.gearmul
        # This if statement decides what rarity the player will get based on the rarity (harder to get better gear)
        if raritynum <= 375:
            rarity = raritylist[1]
        elif raritynum > 375 and raritynum <= 700:
            rarity = raritylist[2]
        elif raritynum > 700 and raritynum <= 950:
            rarity = raritylist[3]
        elif raritynum > 950:
            rarity = raritylist[4]
        # This decides what it will be called (crown,helmet,mask)
        typetype = random.choice(typetypelist[type])
        # Executes this code if it is a helmet or a chest piece (different pieces of gear will have different stats)
        if type == 'Helmet' or type == 'Chest':
            # This geneartes a randint integer (for gear HP) between two numbers (These numbers will depend on the gear's rarity)
            stat = random.randint(hpnum[raritylist.index(
                rarity)-1], hpnum[raritylist.index(rarity)])
        elif type == 'Weapon':
            # This geneartes a randint integer (for gear DMG) between two numbers (These numbers will depend on the gear's rarity)
            stat = round(random.uniform(dmgnum[raritylist.index(
                rarity)-1], dmgnum[raritylist.index(rarity)]), 2)
        else:
            # This geneartes a randint integer (for Gear DMG, note: damge values for amulets are half that of weapons) between two numbers (These numbers will depend on the gear's rarity)
            stat = round(random.uniform(dmgnum2[raritylist.index(
                rarity)-1], dmgnum2[raritylist.index(rarity)]), 2)
        # This creates the name for the piece of gear (ie,Rarte Helmet)
        name = str(rarity.title()+" "+typetype.title())
        # This generates how much the gear piece is worth
        gold = random.randint(goldnums[raritylist.index(
            rarity)-1], goldnums[raritylist.index(rarity)])
        # This executes the command that creates an entry into the inventory database
        mainconn.execute("INSERT INTO INVENTORY(OWNER,NAME,TYPE,RARITY,EQUIP,STAT,GOLD) VALUES(?,?,?,?,?,?,?)",
                         (player.charid, name.title(), type, rarity.title(), 'n', stat, gold))
        # This commit line tells the database to make the changes (without this your data will be untouched)
        maindb.commit()
        # This prints out what gear the player got
        print("You looted a {} with a stat of {}".format(name, stat))
    else:
        # This is to notify the user that they didn't recieve a gear drop
        print("\nYou didn't recieve a gear drop")
    # If the enemy that the player killed is a boss (a boss occurs every 5 stages) , the rewards given to the character will be greater
    if boss == 'y':
        # Gold given to the plyaer increases with the player's stage
        gold = random.randint(20+player.stage, 30+player.stage)
    else:
        gold = random.randint(10+player.stage, 15+player.stage)

    # This tells the user how much gold they recieved
    print("You found {} gold!".format(gold))
    player.gold += gold
    # This variable is the XP multiplier for a boss
    add = 1
    if boss == 'y':
        # You get 150% XP if you kill a boss
        add = 1.5
    # This the amount of Xp the player will recieve (Increases if it is a boss and also increases with the player's stage)
    xp = 34 + player.stage * 2 * add
    # Xp gained will be added to the player's current XP
    player.currxp += xp
    # If the amount of XP the player has is over the required amount of XP for the level
    player.mulcalc()
    if int(player.currxp) >= player.xpreq:
        # This variable is the amount of XP left after levelling up
        gap = player.currxp - player.xpreq
        # Adds 1 to the player's level
        player.level += 1
        # Sets current XP to the amount left from the level up
        player.currxp = gap
        # Notification that the player levelled up
        print("You have levelled up to level {}\n".format(player.level))
        # Generates a new XP requirement based on the player's level
        player.mulcalc()
    # Updates the database (GOLD, LEVEL, CURRXP)
    player.updatefields()

# This function just updates the database based on how many potions the user has


def potionrefresh(type):
    # Updates the amount of small potions in the database for that specific character
    if type == "small":
        mainconn.execute('UPDATE CHARDB SET SPOTIONS = "%s" WHERE ID = "%s"' % (
            player.spotions, player.charid))
        maindb.commit()
    # Updates the amount of medium potions in the database for that specific character
    elif type == "medium":
        mainconn.execute('UPDATE CHARDB SET MPOTIONS = "%s" WHERE ID = "%s"' % (
            player.mpotions, player.charid))
        maindb.commit()
    # Updates the amount of large potions in the database for that specific character
    elif type == "large":
        mainconn.execute('UPDATE CHARDB SET LPOTIONS = "%s" WHERE ID = "%s"' % (
            player.lpotions, player.charid))
        maindb.commit()

# This function decides how attacks in the game sequence


def decideattack():
    # Player speed is normally 7 but it can be increased by adding skill points to speed
    playerspeed = 7 + player.speed
    # The opponent has a default speed of 7
    oppospeed = 7
    # The total speed is both speeds combined
    totalspeed = playerspeed + oppospeed
    # Find a random number between 1 and totalspeed
    turn = random.randint(1, totalspeed)
    # If that number is less than or equal to 7, it's the opponent's turn to attack
    if turn <= 7:
        result = 'oppo'
    else:
        result = 'player'
    # asdf
    return result


def enter():
    player.mulcalc()
    player.ready()
    race = ''
    stagename = ''
    found = False
    stagenames = [['Gnome gardens', 'Gnome', 1], ['Dwarf mountains', 'Dwarf', 6], ['Halfling Forest', 'Halfling', 11], ['Elf Kingdom', 'Elf', 16], ['Ghoul campsite', 'Ghoul', 21], [
        'Orc Cave', 'Orc', 26], ['Giant Lair', 'Lair', 31], ['Dragon dungeon', 'Dragon', 36], ['Infinte Plains', 'Forgotten', 41], ['Infinte Plains', 'Forgotten', math.inf]]
    while found == False:
        for stages in stagenames:
            if player.stage >= stages[2] and player.stage < stagenames[stagenames.index(stages)+1][2]:
                complete = stages
                stagename = stages[0]
                race = stages[1]
                found = True
                break
    oppo.racegen(race)
    mkilled = 0
    turn = decideattack()
    print("Welcome to the {}\n".format(stagename))
    while mkilled < 3:
        oppo.regen(player.stage, 1)
        print("\nYou are now facing a {} minion!".format(oppo.race.title()))
        while player.dead == 0 and oppo.dead == 0:
            if turn == 'oppo':
                info = oppo.attackgen()
                time.sleep(1)
                print("\nYour opponent is attacking\n")
                time.sleep(.5)
                player.hp -= info[0]
                player.checkdead()
                if info[0] == 0:
                    if player.hp > 0:
                        print("Your opponent missed!\nYou're on {} HP\n".format(
                            round(player.hp, 1)))
                else:
                    print("{} hit worth {} damage!!\nYou're on {} HP\n".format(
                        info[1].title(), info[0], round(player.hp, 1)))
                turn = 'player'
            else:
                attackmenu()
                turn = 'oppo'
        # LOOT GENERATION
        if oppo.dead == 1:
            mkilled += 1
            print(
                "You have killed a {} minion\n//////////////////////////".format(oppo.race.title()))
            loot("n")
            turn = decideattack()
        else:
            print("You died, try again next time!")
            break
    if player.dead != 1:
        if player.stage % 5 == 0:
            print("\nYou have encountered a {} BOSS!".format(oppo.race))
            turn = 'player'
            oppo.regen(player.stage, 1.5)
            while oppo.dead == 0 and player.dead == 0:
                if turn == 'oppo':
                    info = oppo.attackgen()
                    time.sleep(1)
                    print("\nYour opponent is attacking\n")
                    time.sleep(.5)
                    player.hp -= info[0]
                    player.checkdead()
                    if info[0] == 0:
                        print("Your opponent missed!\n")
                    else:
                        print("{} hit worth {} damage!!\nYou're on {} HP\n".format(
                            info[1].title(), info[0], round(player.hp, 1)))
                    turn = 'player'
                else:
                    attackmenu()
                    turn = 'oppo'
            if player.dead == 1:
                print("You were slayed by the boss, try again next time!")
            else:
                print("You slayed the boss!")
                if stagename == "Infinite Plains":
                    print("You completed stage {} an the {}".format(
                        player.stage, stagename))
                else:
                    print("You completed stage {} at the {}, your next journey will take you to the {}".format(
                        player.stage, stagename, stagenames[stagenames.index(complete)+1][0]))
                player.stage += 1
                mainconn.execute('UPDATE CHARDB SET STAGE = "%s" WHERE ID = "%s"' % (
                    player.stage, player.charid))
                maindb.commit()
                loot("y")
        else:
            print("You completed stage {}, your next stage is stage {}".format(
                player.stage, int(player.stage)+1))
            player.stage += 1
            mainconn.execute('UPDATE CHARDB SET STAGE = "%s" WHERE ID = "%s"' % (
                player.stage, player.charid))
            maindb.commit()

    gamemenu()


def potionshop():
    print("\nWelcome to the Potion Shop\nGold Balance - ${}\n1)Small HP Potion - $30\n2)Medium HP Potion - $40\n3)Large HP Potion - $50\n4)Exit\n".format(player.gold))
    while True:
        try:
            choice = int(input("Menu Option:  "))
            if choice > 0 and choice <= 4:
                break
            else:
                print("That is not an option!\n")
        except:
            print("That is not a correct input!\n")
    if choice == 1:
        while True:
            if player.gold >= 30:
                exit = 0
                print("How many do you want to buy?\nType 0 to Exit\n")
                amountpossible = math.trunc(player.gold/30)
                while True:
                    try:
                        amount = int(input("Potion Amount:  "))
                        if amount == 0:
                            exit = 1
                            break
                        elif amount < 0:
                            print("You can't buy a negative amount of potions!\n")
                        elif amount > amountpossible:
                            print("You cant buy that many!\n")
                        elif amount > 0 and amount <= amountpossible:
                            break
                    except:
                        print("That is an incorrect input!\n")
                if exit == 0:
                    cost = 30 * amount
                    player.gold -= cost
                    player.spotions += amount
                    player.updatefields()
                    potionrefresh('small')
                    if player.spotions > 1:
                        print("\nYou now have {} small potions!".format(
                            player.spotions))
                    else:
                        print("\nYou now have {} small potion!".format(
                            player.spotions))
                    break
            else:
                print("Sorry you don't have the gold for that")
                break
    elif choice == 2:
        while True:
            if player.gold >= 40:
                exit = 0
                print("How many do you want to buy?\nType 0 to Exit\n")
                amountpossible = math.trunc(player.gold/40)
                while True:
                    try:
                        amount = int(input("Potion Amount:  "))
                        if amount == 0:
                            exit = 1
                            break
                        elif amount < 0:
                            print("You can't buy a negative amount of potions!\n")
                        elif amount > amountpossible:
                            print("You cant buy that many!\n")
                        elif amount > 0 and amount <= amountpossible:
                            break
                    except:
                        print("That is an incorrect input!\n")
                if exit == 0:
                    cost = 40 * amount
                    player.gold -= cost
                    player.mpotions += amount
                    player.updatefields()
                    potionrefresh('medium')
                    if player.mpotions > 1:
                        print("\nYou now have {} medium potions!".format(
                            player.mpotions))
                    else:
                        print("\nYou now have {} medium potion!".format(
                            player.mpotions))
                    break
            else:
                print("Sorry you don't have the gold for that")
                break
    elif choice == 3:
        while True:
            if player.gold >= 50:
                exit = 0
                print("How many do you want to buy?\nType 0 to Exit\n")
                amountpossible = math.trunc(player.gold/50)
                while True:
                    try:
                        amount = int(input("Potion Amount:  "))
                        if amount == 0:
                            exit = 1
                            break
                        elif amount < 0:
                            print("You can't buy a negative amount of potions!\n")
                        elif amount > amountpossible:
                            print("You cant buy that many!\n")
                        elif amount > 0 and amount <= amountpossible:
                            break
                    except:
                        print("That is an incorrect input!\n")
                if exit == 0:
                    cost = 50 * amount
                    player.gold -= cost
                    player.lpotions += amount
                    player.updatefields()
                    potionrefresh('large')
                    if player.lpotions > 1:
                        print("\nYou now have {} large potions!".format(
                            player.lpotions))
                    else:
                        print("\nYou now have {} large potion!".format(
                            player.lpotions))
                    break
            else:
                print("Sorry you don't have the gold for that")
                break

    print("\nGood Luck on your journey")
    gamemenu()


def bag():
    print("--- Bag ---")
    templist = []
    exit = 0
    if player.spotions > 0:
        templist.append(["small", player.spotions])
    if player.mpotions > 0:
        templist.append(["medium", player.mpotions])
    if player.lpotions > 0:
        templist.append(["large", player.lpotions])
    i = 1
    if templist == []:
        print("\nYour bag is empty, go the potion shop next\n")
    elif player.hp == player.findmaxhp():
        print("Your already at max HP!\n")
    else:
        for potion in templist:
            print("{}){} potions - {} left".format(i,
                                                   potion[0].title(), potion[1]))
            i += 1
        print("{})Exit".format(i))
        while True:
            try:
                choice = int(input("Potion Option:  "))
                if choice > 0 and choice >= len(templist):
                    break
                elif choice == i:
                    exit = 1
                    break
                else:
                    print("That is not an option!\n")
            except:
                print("That is an incorrect input!\n")
        if choice == i:
            exit = 1

        if exit == 0:
            choice = templist[choice-1]
            while True:
                try:
                    amount = int(input("Potion Amount:  "))
                    if amount < 0:
                        print("You can't use a negative amount of potions!\n")
                    elif amount > choice[1]:
                        print("You don't have that many\n")
                    elif amount > 0 and amount <= choice[1]:
                        break
                except:
                    print("That is an incorrect input!\n")
            if choice[0] == "small":
                hpamount = 30 * amount
                player.spotions -= amount
                mainconn.execute('UPDATE CHARDB SET SPOTIONS = "%s" WHERE ID = "%s"' % (
                    player.spotions, player.charid))
                maindb.commit()
                player.usepotion(hpamount)
            elif choice[0] == "medium":
                hpamount = 40 * amount
                player.mpotions -= amount
                mainconn.execute('UPDATE CHARDB SET MPOTIONS = "%s" WHERE ID = "%s"' % (
                    player.mpotions, player.charid))
                maindb.commit()
                player.usepotion(hpamount)
            elif choice[0] == "large":
                hpamount = 50 * amount
                player.lpotions -= amount
                mainconn.execute('UPDATE CHARDB SET LPOTIONS = "%s" WHERE ID = "%s"' % (
                    player.lpotions, player.charid))
                maindb.commit()
                player.usepotion(hpamount)
            print("\nYou are now at {} HP".format(math.ceil(player.hp)))
        else:
            print("\nYou have returned to the battlefield!")

    attackmenu()


def attackmenu():
    print("\nAttack Menu:\n1)Attack\n2)Open Bag")
    while True:
        try:
            choice = int(input("Menu Option:  "))
            if choice > 0 and choice < 3:
                break
            else:
                print("That is not an option!\n")
        except:
            print("That is not a correct input!\n")
    if choice == 1:
        print("\nYou are attacking!!\n")
        info = player.attackgen()
        time.sleep(0.5)
        oppo.hp -= info[0]
        oppo.checkdead()
        if oppo.dead == 0:
            print("{} hit worth {} damage!!\n{} opponent: {} HP".format(
                info[1].title(), info[0], oppo.race.title(), round(oppo.hp, 1)))
        else:
            print("{} hit worth {} damage!!\n".format(
                info[1].title(), info[0]))
    elif choice == 2:
        bag()


# Login Function - Checks the login table for the entered data
def login():
    exit = False
    nonumber = False
    while True:
        print("\nLogin to account\nType exit to leave")
        while True:
            try:
                username = input("Username:  ").lower()
                break
            except:
                print("That is not a correct input!\n")
        if username == "exit":
            start()
        while True:
            password = input("Password:  ")
            if password == "exit":
                break
            if checklgd(password) == False:
                print("Your details are incorrect!")
                nonumber = True
                break
            else:
                break
        if password == "exit":
            start()
            break
        elif nonumber == True:
            login()
        else:
            mainconn.execute(
                'SELECT * FROM LOGINDB WHERE USERNAME ="%s" AND PASSWORD = "%s" ' % (username, password))
            if mainconn.fetchone() is not None:
                print("You are logged in!\n\nWelcome to Assault of Power")
                player.loggedin = 1
                mainconn.execute(
                    'SELECT * FROM LOGINDB WHERE USERNAME ="%s" AND PASSWORD = "%s" ' % (username, password))
                player.id = mainconn.fetchone()[0]
                player.login()
                switcher()
                break
            else:
                print("Login Failed")

# Switcher to check if the user has fully registered - If not it sends them to the begin function


def switcher():
    mainconn.execute('SELECT * FROM CHARDB WHERE ACCID = "%s" ' % (player.id))
    data = mainconn.fetchall()
    if len(data) == 0:
        begin()
    else:
        charmenu()


def skills():
    skills = ['strength', 'vitality', 'speed']
    points = player.level-player.strength-player.vitality-player.speed-1
    print("\nSkill Tree\nPoints Remaining: {}\n".format(points))
    print("1)Add Skill points\n2)View Current Stats\n3)Reset Skills - $500\n4)Exit\n")
    while True:
        try:
            choice = int(input("Menu Option:  "))
            if choice > 0 and choice <= 4:
                break
            else:
                print("That is not an option!\n")
        except:
            print("That is not a correct input!\n")
    if choice == 1:
        if points > 0:
            print("\n1)Strength - {} (+3 DMG)\n2)Vitality - {} (+10 HP)\n3)Speed - {} (+1 Speed)\n".format(
                player.strength, player.vitality, player.speed))
            while True:
                try:
                    choice = int(input("Skill Option:  "))
                    if choice > 0 and choice < 4:
                        break
                    else:
                        print("That is not an option!")
                except:
                    print("That is not a correct input!\n")
            skill = skills[choice-1]
            while True:
                try:
                    amount = int(input("How many points to allocate?  "))
                    if amount > 0 and amount <= points:
                        break
                    elif amount <= 0:
                        print("That is an incorrect number of points\n")
                    else:
                        print("You don't have that many points\n")
                except:
                    print("That is an incorrect input!\n")
            if skill == 'strength':
                player.strength += amount
                mainconn.execute('UPDATE CHARDB SET STRENGTH = "%s" WHERE ID = "%s"' % (
                    player.strength, player.charid))
                maindb.commit()
            elif skill == 'vitality':
                player.vitality += amount
                mainconn.execute('UPDATE CHARDB SET VITALITY = "%s" WHERE ID = "%s"' % (
                    player.vitality, player.charid))
                maindb.commit()
            elif skill == 'speed':
                player.speed += amount
                mainconn.execute('UPDATE CHARDB SET SPEED = "%s" WHERE ID = "%s"' % (
                    player.speed, player.charid))
                maindb.commit()
            print("You have now added {} points to {}".format(
                amount, skill.title()))
        else:
            print("You don't have enough points")
    elif choice == 2:
        print("--- {}'s Stats ---\nStrength: {}\nVitality: {}\nSpeed: {}".format(
            player.charname.title(), player.strength, player.vitality, player.speed))
    elif choice == 3:
        if player.gold >= 500:
            while True:
                choice = input(
                    "Are you sure you want to reset your skills? (yes/no):  ").lower().strip()
                if choice == "yes" or choice == "no":
                    break
                else:
                    print("That is not an option!\n")
            if choice == "yes":
                player.gold -= 500
                player.strength = 0
                player.vitality = 0
                player.speed = 0
                player.updatefields()
                points = player.level-player.strength-player.vitality-player.speed-1
                print(
                    "Your skills have been reset, you now have {} skill points".format(points))
            else:
                print("\nYour skills remain the same\n")
        else:
            print("You need 500 gold to reset your skills")
    else:
        print("\nGood Luck on your journey!")
    gamemenu()


def inventory():
    pieces = ['Helmet', 'Chest', 'Amulet', 'Weapon']
    templist = []
    print("--- INVENTORY ---\n")
    empty = 0
    i = 1
    for piece in pieces:
        mainconn.execute(
            "SELECT * FROM INVENTORY WHERE OWNER = '%s' AND TYPE = '%s'" % (player.charid, piece))
        data = mainconn.fetchall()
        if len(data) != 0:
            print(str(i)+")", piece.title())
            templist.append(piece)
            i += 1
    if i == 1:
        print("\nYour inventory is empty!")
        empty = 1
        input("Press [ENTER] to continue\n")
    else:
        while True:
            try:
                choice = int(input("Menu Option:  "))
                if choice > 0 and choice <= len(templist):
                    break
                else:
                    print("That is not an option\n")
            except:
                print("That is not a correct input\n")
    if empty == 0:
        piece = templist[choice-1]
        print("---", piece.title(), "---")
        mainconn.execute(
            "SELECT * FROM INVENTORY WHERE OWNER = '%s' AND TYPE = '%s'" % (player.charid, piece))
        details = mainconn.fetchall()
        templist = []
        max1 = 2
        max2 = 4
        max3 = 6
        max4 = 4
        max5 = 4
        max6 = 4
        max7 = 5
        i = 1
        # Gearid,Owner,Name,Type,Rarity,Equip,Stat,Gold,  6,7,5
        for character in details:
            if len(character[2]) > max2:
                max2 = len(character[2])
            if len(character[4]) > max3:
                max3 = len(character[4])
            if len(character[3]) > max4:
                max4 = len(character[3])
            if len(str(character[6])) > max5:
                max5 = len(str(character[6]))
            if len(str(character[7])) > max6:
                max6 = len(str(character[7]))
            if len(str(character[5])) > max7:
                max7 = len(str(character[5]))
            templist.append(character[0])

        for id in templist:
            if len(str(id)) > max1:
                max1 = len(str(id))
        print("\n|ID{}|NAME{}|RARITY{}|TYPE{}|STAT{}|GOLD{}|EQUIP{}|".format(spacer(
            max1-2), spacer(max2-4), spacer(max3-6), spacer(max4-4), spacer(max5-4), spacer(max6-4), spacer(max7-5),))
        mainconn.execute(
            "SELECT * FROM INVENTORY WHERE OWNER = '%s' AND TYPE = '%s'" % (player.charid, piece))
        details = mainconn.fetchall()
        for item in details:
            if item[5] == "y":
                equip = "Yes"
            else:
                equip = "No"
            print("|{}{}|{}{}|{}{}|{}{}|{}{}|{}{}|{}{}|".format(i, spacer(max1-len(str(i))), item[2], spacer(max2-len(item[2])), item[4], spacer(max3-len(
                item[4])), item[3], spacer(max4-len(item[3])), item[6], spacer(max5-len(str(item[6]))), item[7], spacer(max6-len(str(item[7]))), equip, spacer(max7-len(equip))))
            i += 1

        while True:
            try:
                choice = int(input("Gear ID:  "))
                if choice > 0 and choice <= len(templist):
                    break
                else:
                    print("That is not an option!\n")
            except:
                print("That is not a correct input!\n")
        chosenid = templist[choice-1]
        print("\nWhat do you want to do?\n1)Equip Item\n2)Sell Item\n3)Exit")
        while True:
            try:
                choice = int(input("Menu Option:  "))
                if choice > 0 and choice < 4:
                    break
                else:
                    print("That is not an option!\n")
            except:
                print("That is not a correct input!\n")
        if choice == 1:
            print(piece)
            mainconn.execute('UPDATE INVENTORY SET EQUIP = "%s" WHERE OWNER = "%s" AND EQUIP = "%s" AND TYPE = "%s"' % (
                'n', player.charid, "y", piece))
            maindb.commit()
            mainconn.execute(
                'UPDATE INVENTORY SET EQUIP = "%s" WHERE GEARID = "%s"' % ('y', chosenid))
            maindb.commit()
            details = []
            piecelist = ['Helmet', 'Chest', 'Amulet', 'Weapon']
            if piece == 'Helmet':
                mainconn.execute('SELECT NAME FROM INVENTORY WHERE OWNER = "%s" AND TYPE = "%s" AND EQUIP = "%s"' % (
                    player.charid, "Helmet", "y"))
                details = mainconn.fetchone()
                player.helmet = details[0]
                mainconn.execute('UPDATE CHARDB SET HELMET = "%s" WHERE ID = "%s"' % (
                    player.helmet, player.charid))
                maindb.commit()
            elif piece == 'Chest':
                mainconn.execute('SELECT NAME FROM INVENTORY WHERE OWNER = "%s" AND TYPE = "%s" AND EQUIP = "%s"' % (
                    player.charid, "Chest", "y"))
                details = mainconn.fetchone()
                player.chest = details[0]
                mainconn.execute('UPDATE CHARDB SET CHEST = "%s" WHERE ID = "%s"' % (
                    player.chest, player.charid))
                maindb.commit()
            elif piece == 'Amulet':
                mainconn.execute('SELECT NAME FROM INVENTORY WHERE OWNER = "%s" AND TYPE = "%s" AND EQUIP = "%s"' % (
                    player.charid, "Amulet", "y"))
                details = mainconn.fetchone()
                player.amulet = details[0]
                mainconn.execute('UPDATE CHARDB SET AMULET = "%s" WHERE ID = "%s"' % (
                    player.amulet, player.charid))
                maindb.commit()
            elif piece == 'Weapon':
                mainconn.execute('SELECT NAME FROM INVENTORY WHERE OWNER = "%s" AND TYPE = "%s" AND EQUIP = "%s"' % (
                    player.charid, "Weapon", "y"))
                details = mainconn.fetchone()
                player.weapon = details[0]
                mainconn.execute('UPDATE CHARDB SET WEAPON = "%s" WHERE ID = "%s"' % (
                    player.weapon, player.charid))
                maindb.commit()
            print("\nThat is now equipped!\n")
        elif choice == 2:
            mainconn.execute(
                'SELECT * FROM INVENTORY WHERE GEARID ="%s"' % (chosenid))
            details = mainconn.fetchone()
            player.gold += int(details[7])
            player.updatefields()
            mainconn.execute(
                'DELETE FROM INVENTORY WHERE GEARID = "%s"' % (chosenid))
            maindb.commit()
            print("\nYou sold that piece for {} gold!".format(int(details[7])))

    gamemenu()


def stats():
    print("\n---- CHARACTER INFORMATION ----\n")
    print("Character Name:", player.charname.title(), "\nRace:", player.race.title(), "\nClass:", player.charclass.title(), "\nLevel:", player.level, "\nXP:", int(player.currxp),
          "\nGold Amount:", player.gold, "\nHelmet:", player.helmet.title(), "\nChest:", player.chest.title(), "\nAmulet", player.amulet.title(), "\nWeapon:", player.weapon.title())
    input("Press [ENTER] to continue\n")
    gamemenu()


def gamemenu():
    print("\nGame Menu:")
    print("1)Enter Stage:", player.stage,
          "\n2)View Inventory\n3)Potion Shop\n4)Skill Tree\n5)Character Stats\n6)Exit\n")
    while True:
        try:
            choice = int(input("Menu Option:  "))
            if choice > 0 and choice < 7:
                break
            else:
                print("That is not a menu number\n")
        except:
            print("That is not a correct input!\n")
    if choice == 1:
        enter()
    elif choice == 2:
        inventory()
    elif choice == 3:
        potionshop()
    elif choice == 4:
        skills()
    elif choice == 5:
        stats()
    else:
        charmenu()


def charpick():
    empty = 0
    print("\nPlease select a character")
    mainconn.execute('SELECT * FROM CHARDB WHERE ACCID = "%s"' % (player.id))
    details = mainconn.fetchall()
    templist = []
    i = 1
    if len(details) == 0:
        empty = 1
        begin()
    if empty == 0:
        max1 = 2
        max2 = 9
        max3 = 4
        max4 = 5
        max5 = 5
        for character in details:
            if len(character[2]) > max2:
                max2 = len(character[2])
            if len(character[3]) > max3:
                max3 = len(character[3])
            if len(character[4]) > max4:
                max4 = len(character[4])
            if len(str(character[6])) > max5:
                max5 = len(str(character[6]))
            templist.append(character[1])

        for id in templist:
            if len(str(id)) > max1:
                max1 = len(str(id))
        print("\n|ID{}|CHARACTER{}|RACE{}|CLASS{}|LEVEL{}|".format(
            spacer(max1-2), spacer(max2-9), spacer(max3-4), spacer(max4-5), spacer(max5-5)))
        for item in details:
            print("|{}{}|{}{}|{}{}|{}{}|{}{}|".format(i, spacer(max1-len(str(i))), item[2].title(), spacer(max2-len(item[2])), item[3].title(
            ), spacer(max3-len(item[3])), item[4].title(), spacer(max4-len(item[4])), item[5], spacer(max5-len(str(item[5])))))
            i += 1
        totallength = 6 + max1 + max2 + max3 + \
            max4 + max5 - len(" 0 TO EXIT ") - 2
        space1 = math.floor(totallength/2)
        space2 = totallength - space1
        print("|{} 0 TO EXIT {}|".format("-"*space1, "-"*space2))
        while True:
            try:
                num = int(input("Please enter the character ID:  "))
                if num >= 0 and num <= len(templist):
                    break
                else:
                    print("That is not a character option!\n")
            except:
                print("That is not a correct input!\n")
        if num == 0:
            charmenu()
        else:
            charid = templist[num-1]
            player.charload(charid)
            gamemenu()


def charmenu():
    print("1)Create a character\n2)Pick A Character\n3)Quit\n")
    while True:
        try:
            choice = int(input("Menu Option:  "))
            if choice > 0 and choice < 4:
                break
            else:
                print("That is not an option!\n")
        except:
            print("That is not a correct input!")
    if choice == 1:
        begin()
    elif choice == 2:
        charpick()
    elif choice == 3:
        start()


# Asks the user for more information when they log-in to their account - Use this so the user can make multiple accounts easier
def begin():
    global races
    global classes
    welcomestart = mainconn.execute(
        'SELECT * FROM LOGINDB WHERE ID ="%s"' % (player.id))
    print("Welcome", welcomestart.fetchone()[
          1]+",", "please create a game character!.\nType exit to leave")
    leave = 0
    while leave == 0:
        while True:
            try:
                charname = input("Character Name:  ").strip().lower()
                if len(charname) > 15:
                    print("That name is too long! (Must be under 15 characters)\n")
                else:
                    break
            except:
                print("That is not a correct input!\n")
        if charname == "exit":
            leave = 1
            break
        i = 1
        for race in races:
            print(str(i)+")", race.title())
            i += 1
        while True:
            while True:
                try:
                    racenum = int(
                        input("\nPlease choose a race with the corresponding number:  "))
                    break
                except:
                    print("That is not a correct input!\n")
            if racenum > 0 and racenum < (len(races))+1:
                break
            else:
                print("That is not an option!")
        racechoice = races[racenum-1]
        i = 1
        for class1 in classes:
            print(str(i)+")", class1.title())
            i += 1
        while True:
            while True:
                try:
                    classnum = int(
                        input("\nPlease choose a class with the corresponding number:  "))
                    break
                except:
                    print("That is not a correct input!\n")
            if classnum > 0 and classnum < (len(classes)+1):
                break
            else:
                print("That is not an option!")
        leave = 2
    if leave == 1:
        print("You have left\n")
        charmenu()
    else:
        charactercreateentry(charname, racenum, classnum)
        print("\nWelcome to Assault of Power")
        charmenu()

# First Menu function that allows the login


def start():
    print("\n1)Login\n2)Create Account\n3)Exit")
    while True:
        try:
            choice = int(input("Menu Number:  "))
            if choice > 0 and choice < 4:
                break
            else:
                print("That is not an option!\n")
        except:
            print("That is not a correct input!\n")
    if choice == 1:
        login()
    elif choice == 2:
        create()
    elif choice == 3:
        print("\nGoodbye")


# Code that runs when the program starts - Welcome is excluded from main program to remove unwanted clutter and to only welcome them at key points
print("Welcome to Assault of Power")
start()
