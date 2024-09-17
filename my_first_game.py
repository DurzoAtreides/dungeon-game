import random

##This will be a dungeon crawler RPG where the player can change rooms and fight random enemies to gain EXP and delve farther

##The item class has a health effect, a challenge/value rating ##and/or is equippable and augments attributes
class Item():
    def __init__(self, item_name, health_boost = 0, strength_boost = 0, defense_boost = 0, challenge_rating = 1):
        self.item_name = item_name
        self.health_boost = health_boost
        self.strength_boost = strength_boost
        self.defense_boost = defense_boost
        self.challenge_rating = challenge_rating

    def __repr__(self):
        ##when an object gets printed and is of the item class a print statement put together by what attributes it has gets made and returned
        item_descript = f"A {self.item_name}"
        if (self.health_boost >= 1) and (self.challenge_rating == 3):
            item_descript += f" that adds {self.health_boost} points to health, {self.strength_boost} to strength, and {self.defense_boost} to defense"
        elif (self.health_boost >= 1) and (self.challenge_rating < 3):
            item_descript += f" that adds {self.health_boost} points to health"
        elif (self.strength_boost > 0) and (self.challenge_rating == 2):
            item_descript += f" that adds {self.strength_boost} to strength"
        elif (self.defense_boost > 0) and (self.challenge_rating == 2):
            item_descript += f" that adds {self.defense_boost} to defense"
        return item_descript

    def use_item(self, player):
        ##the use item function checks the inventory list for at least one occurance of the item and the checks what kind of boost it gives and applies it to the player
        if player.inventory.count(self) >= 1:
            player.gain_health(self.health_boost)
            player.defense_boost += self.defense_boost
            player.strength_boost += self.strength_boost
            player.inventory.remove(self)

    def gain_item(self, player):
        ##the gain item function adds the item to the inventory list of the player
        player.inventory.append(self)
        player.current_location.loot = None

        print(f"You added a {self.item_name} to your inventory.")

super_potion = Item('Super Potion', health_boost= 20, challenge_rating=2)
potion_high = Item('High Potion', health_boost = 15)
potion_reg = Item('Potion', health_boost = 10)
strength_up = Item('Strength Boost', strength_boost = 1, challenge_rating = 2)
defense_up = Item('Defense Boost', defense_boost = 1, challenge_rating = 2)
super_boost = Item('Super Boost', 10, 1, 1, 3)

item_mapping = {
    "potion": potion_reg,
    "high potion": potion_high,
    "super potion": super_potion,
    "strength boost": strength_up,
    "defense boost": defense_up,
    "super boost": super_boost
    }

loot_table_1 = [potion_reg, potion_reg, potion_reg, potion_high, potion_high, super_potion]
loot_table_2 = [potion_high, super_potion, super_potion, strength_up, defense_up]
loot_table_3 = [super_potion, super_potion, strength_up, defense_up, super_boost]

##The player class has health, a max health, a name, a STR attr, a DEF attr, an inventory, a level, and an EXP counter. The player will also have an attack function, a use item function, a move function, a print function, a gain EXP function, a check level up function and a level up function
class Player():
    def __init__(self, input_name, health = 15, input_strength = 3, input_defense = 3):
        self.name = input_name
        self.level = 1
        self.exp = 0
        self.base_health = health
        self.base_strength = input_strength
        self.base_defense = input_defense
        self.max_health = self.base_health + (self.level * 5)
        self.health = self.max_health
        self.strength = self.base_strength * self.level
        self.defense = self.base_defense * self.level
        self.strength_boost = 0
        self.defense_boost = 0
        self.effective_strength = self.strength + self.strength_boost
        self.effective_defense = self.defense + self.defense_boost
        self.inventory = []
        self.is_knocked_out = False
        self.current_enemy = None
        self.current_location = None
        self.last_enemy = None

    def __repr__(self):
        ##Printing a player tells the name, current health, and level
        return f'This adventurer named {self.name} is at level {self.level} and has {self.health} health points'

    def gain_exp(self, amount):
        ##the gain exp function adds an exp amount and runs the check level up function
        self.exp += amount
        self.check_level_up()

    def check_level_up(self):
        ##the check level up function compares the current exp to the exp thresholds and run the level up function if they meet a new higher threshold
        level_up_thresholds = {2: 20, 3: 50, 4: 150}
        new_level = self.level
        for level, exp_required in level_up_thresholds.items():
            if self.exp >= exp_required:
                new_level = level
            else:
                break

        if new_level > self.level:
            self.level_up(new_level)

    def level_up(self, new_level):
        ##the level up function adjusts the player's max health, current health, strength, and defense
        self.level = new_level
        print(f"{self.name} leveled up to level {new_level}. ")
        self.max_health = self.base_health + (self.level * 5)
        self.health = self.max_health
        self.strength = self.base_strength * self.level
        self.defense = self.base_defense * self.level
        self.effective_strength = self.strength + self.strength_boost
        self.effective_defense = self.defense + self.defense_boost
        print(f"Strength is now at {self.effective_strength}, defense is now at {self.effective_defense}, and your max health is at {self.max_health}.")

    def gain_health(self, amount):
        ##the gain health function resets the health to 1 if it was negative or 0, adds health up to the max health value, and sets knocked out to false
        if self.health <= 0:
            self.health = 1
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        self.is_knocked_out = False

    def lose_health(self, amount):
        ##the lose health function subtracts health down to the minimum health value of 0, if it reaches 0 it sets knocked out to true, and prints remaining hit points or a knocked out notification
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_knocked_out = True
            print(f"{self.name} was knocked out!")

    def attack(self, enemy):
        ##the attack function deals damage to the current enemy's health based on the strength of the player and defense of the enemy
        if self.health <= 0:
            print(f"{self.name} can't attack while knocked out!")
        else:
            base_damage = (self.strength - enemy.defense)
            rand_bonus = random.randint(-1, 3)
            bonus_damage = (rand_bonus * self.level) + self.strength_boost
            total_damage = base_damage + bonus_damage
            if total_damage < 0:
                total_damage = 0
            print(f'{self.name} attacked the {enemy.name} and dealt {total_damage} damage')
            if rand_bonus == 3:
                print("It was a critical hit!")
            enemy.lose_health(total_damage, self)

            try:
                self.current_enemy.attack(self)
            except AttributeError:
                pass

    def change_location(self, new_location):
        ##the change location function takes a string parameter and checks it against the location mapping dictionary and if it matches a key it changes the current location variable and resets the enemy and then prints a line about what is in the room. If it does not match, it prints a line saying it was an invalid location choice.
        location_mapping = {"a1": a1, "a2": a2, "a3": a3, "b1": b1, "b2": b2, "b3": b3, "c1": c1, "c2": c2, "c3": c3, "c4":c4}
        if new_location in location_mapping:
            self.current_location = location_mapping[new_location]
            location_mapping[new_location].reset_enemy()
            if self.current_enemy == None:
                print('An empty room')
            else:
                print(f"{self.current_enemy}")
        else:
            print("Invalid location!")

##The enemy class has a name, health, a challenge rating, a STR attr, a DEF attr, and an EXP value. The enemy will also have an attack function, a lose health function, and a reward/death function
class Enemy():
    def __init__(self, input_name, input_health, challenge_rating, input_strength, input_defenese, exp_value,):
        self.name = input_name
        self.base_health = input_health
        self.current_health = self.base_health
        self.challenge_rating = challenge_rating
        self.strength = input_strength
        self.defense = input_defenese
        self.exp_value = exp_value

    def __repr__(self):
        ##printing an object of the enemy class makes a string that uses the name variable
        return f"A {self.name} is in this room!"

    def lose_health(self, amount, player):
        ##the lose health function reduces the health value and if the health value reaches 0 or lower runs the death function to reward the player
        self.current_health -= amount
        if self.current_health <= 0:
            print(f'The {self.name} has been deafeated!')
            self.death(player)

    def attack(self, player):
        ##the attack function deals damage to the player based on the strength of the enemy and the defense of the player
        base_damage = (self.strength - player.defense)
        rand_bonus = random.randint(-1, 2)
        bonus_damage = (rand_bonus * self.challenge_rating) - player.defense_boost
        total_damage = base_damage + bonus_damage
        if total_damage < 0:
            total_damage = 0
        print(f"The {self.name} attacked {player.name} and dealt {total_damage} damage")
        player.lose_health(total_damage)
        if rand_bonus == 2:
            print("It was a critical hit!")

    def death(self, player):
        ##the death function rewards the player with the enemy's exp value and a choice from a loot table
        player.gain_exp(self.exp_value)
        player.last_enemy = self
        player.current_enemy = None
        player.current_location.enemy = None
        if self.challenge_rating == 1:
            loot = random.choice(loot_table_1)
            player.inventory.append(loot)
            print(f"You found {loot}")
        elif self.challenge_rating == 2:
            loot = random.choice(loot_table_2)
            player.inventory.append(loot)
            print(f"You found {loot}")
        elif self.challenge_rating == 3:
            loot = random.choice(loot_table_3)
            player.inventory.append(loot)
            print(f"You found {loot}")
        elif self.challenge_rating == 4:
            print("The boss is dead! You Win!")

rat = Enemy("Rat", 5, 1, 3, 3, 5)
spider = Enemy("Spider", 8, 1, 4, 2, 8)
wolf = Enemy("Wolf", 12, 2, 6, 5, 15)
bear = Enemy("Bear", 18, 2, 8, 6, 20)
slime = Enemy("Slime", 30, 3, 9, 12, 30)
oily = Enemy("Oil Monster", 35, 3, 12, 11, 35)
skelly = Enemy("Possessed Skeleton", 50, 4, 15, 15, 10000)

monster_table_1 = [rat, rat, rat, spider, spider]
monster_table_2 = [spider,spider, wolf, wolf, wolf, bear, bear]
monster_table_3 = [bear, bear, slime, slime, oily, oily]
monster_table_4 = [slime, oily, skelly]

## the location class has a location name and a challenge rating that determines what loot table and monster table the location will fill itself from
class Location():
    def __init__(self, location_name, loot_table, monster_table, challenge_rating = 1):
        self.location_name = location_name
        self.challenge_rating = challenge_rating
        self.loot_table = loot_table
        self.loot = random.choice(loot_table)
        self.monster_table = monster_table
        self.enemy = random.choice(monster_table)

    def __repr__(self):
        ##printing an object of the location class makes a string put together of the name variable and loot variable
        return f"You are in {self.location_name} and you found a {self.loot} in the corner"

    def reset_enemy(self):
        ##the reset enemy function chooses an enemy from the location's monster table and resets its health, and then sets the enemy as the current enemy for the player
        self.enemy = random.choice(self.monster_table)
        self.enemy.current_health = self.enemy.base_health
        player_1.current_enemy = self.enemy

    def reset_loot(self):
        ##the reset loot function chooses another item from the item table and populates the loot variable with it
        self.loot = random.choice(self.loot_table)

a1 = Location("A1", loot_table_1, monster_table_1)
a2 = Location("A2", loot_table_1, monster_table_1)
a3 = Location("A3", loot_table_1, monster_table_1)
b1 = Location("B1", loot_table_2, monster_table_2, 2)
b2 = Location("B2", loot_table_2, monster_table_2, 2)
b3 = Location("B3", loot_table_2, monster_table_2, 2)
c1 = Location("C1", loot_table_3, monster_table_3, 3)
c2 = Location("C2", loot_table_3, monster_table_3, 3)
c3 = Location("C3", loot_table_3, monster_table_3, 3)
c4 = Location("C4", loot_table_3, monster_table_4, 4)

##starting the game prompts the player to name their adventurer and then proceeds into the main game loop

player_name = input("What is your adventurer's name? ")

player_1 = Player(player_name)

##the main game loop consists of a choice between actions to fight, move, use items, search or wait in the current location. The game loop continues until an enemy with a challenge rating attribute of 4 is killed.

while (player_1.last_enemy == None) or (player_1.last_enemy.challenge_rating != 4):
    print(player_1)
    action = input("\nWhat would you like to do? (1: attack, 2: change location, 3: use item, 4: search, 5: wait) ")

    if action == "1":
        ##the attack choice checks to see if there's a current enemy, prints a no enemy statement if there isnt one, and runs the player attack function if there is one
        if player_1.current_enemy == None:
            print("No enemy to attack here!")
        else:
            player_1.attack(player_1.current_enemy)

    elif action == "2":
        ##the change location choice feeds a player input into the player change location function
        new_location = input("Where do you want to go? (a1, a2, a3, b1, b2, b3, c1, c2, c3, c4) ")
        player_1.change_location(new_location)

    elif action == "3":
        ##the use item choice prints the player's inventory and then checks if the player's item choice is an item and then runs the item's use item function
        print(player_1.inventory)
        used_item = input ("Which item would you like to use from the above list? ")
        item_to_use = item_mapping.get(used_item)
        if item_to_use:
            item_to_use.use_item(player_1)
        else:
            print("Item not in inventory")

    elif action == "4":
        ##the search choice prints the players current location and then runs the item in the loot variable's gain item function, if there isnt a current item it will print a no item statement
        try:
            if player_1.current_location:
                print(player_1.current_location)
                player_1.current_location.loot.gain_item(player_1)
            else:
                print("You didn't find anything in your search")
        except AttributeError:
            print("You didn't find anything in your search")

    elif action == "5":
        ##the wait choice runs the current location's reset enemy and reset loot function and also prints a statement about the new enemy
        if player_1.current_location:
            player_1.current_location.reset_enemy()
            player_1.current_location.reset_loot()
            player_1.current_enemy = player_1.current_location.enemy
            print(f"You waited and now {player_1.current_enemy}")
        else:
            print("You waited and nothing happened. Try changing location")

    else:
        ##if the player input doesnt match any of the choices provided it prints a statement saying invalid command
        print("Invalid command")