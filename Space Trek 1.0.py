# importing the required modules
import os
import sys
import random
import string
import time
import keyboard
import pyfiglet


#####DISPLAYMENT#####
	#enter to continue isused to move from your current section
def press_enter_to_continue():
	print("\nPress Enter to continue")
	keyboard.wait("enter")
	while keyboard.is_pressed("enter"):
		pass
	os.system('cls' if os.name == "nt" else "clear")
	#to render the choices so user can see
def render_selection(selection:list, arrow_is_at:int, description, arrow_is_before = None):
	if arrow_is_before != None:
		for i in range(len(selection)+2+(len(description[arrow_is_before].split("\n")) if description != None else 0)):
			sys.stdout.write('\x1b[1A')###Cursor up
			sys.stdout.write('\x1b[2K')###Erase whole line
	for i in range(len(selection)):
		if arrow_is_at == i:
			print('\x1b[0;30;47m' + str(selection[i]) + '\x1b[0m')
		else:
			print(selection[i])
	print("\n\n", end = "")
	if description != None:
		print(description[arrow_is_at])
	#list of the selection that will be displayed
def display_selection(selection: list):
	if isinstance(selection[0], list):
		description = selection[1]
		selection = selection[0]
	else:
		description	= None
	arrow_is_at = 0
	render_selection(selection, arrow_is_at, description)
	arrow_is_before = arrow_is_at
	while True:
		if keyboard.is_pressed("up"):
			if arrow_is_at <= 0:
				arrow_is_before	= arrow_is_at
				arrow_is_at = len(selection) - 1
			else:
				arrow_is_before	= arrow_is_at
				arrow_is_at = arrow_is_at - 1
			render_selection(selection, arrow_is_at, description, arrow_is_before)
			while keyboard.is_pressed("up"):
				pass
		if keyboard.is_pressed("down"):
			if arrow_is_at >= len(selection)-1:
				arrow_is_before	= arrow_is_at
				arrow_is_at = 0
			else:
				arrow_is_before	= arrow_is_at
				arrow_is_at = arrow_is_at + 1
			render_selection(selection, arrow_is_at, description, arrow_is_before)
			while keyboard.is_pressed("down"):
				pass
		if keyboard.is_pressed("enter"):
			while keyboard.is_pressed("enter"):
				pass
			for i in range(len(selection)+2+(len(description[arrow_is_before].split("\n")) if description != None else 0)):
				sys.stdout.write('\x1b[1A')###Cursor up
				sys.stdout.write('\x1b[2K')###Erase whole line
			break
	return selection[arrow_is_at]
	#the slider for our fighting system
def render_slider(default_str:str, start_end: tuple, arrow_is_at: int, first_time:bool):
	if not first_time:
		sys.stdout.write('\x1b[1A')###Cursor up
		sys.stdout.write('\x1b[2K')
	print(default_str, end = "")
	display_str = "<"
	for x in range(start_end[0], start_end[1]+1, 1):
		if x == arrow_is_at:
			display_str = display_str + f"({x})"
		else:
			display_str = display_str + "-"
	display_str = display_str + ">"
	print(display_str)
	#rendering the slider
def display_slider(start_end: tuple, default_str:str = ""):
	arrow_is_at = start_end[0]
	render_slider(default_str, start_end, arrow_is_at, True)
	while True:
		if keyboard.is_pressed("left"):
			if arrow_is_at <= start_end[0]:
				arrow_is_at = start_end[1]
			else:
				arrow_is_at = arrow_is_at - 1
			render_slider(default_str, start_end, arrow_is_at, False)
			while keyboard.is_pressed("left"):
				pass
		if keyboard.is_pressed("right"):
			if arrow_is_at >= start_end[1]:
				arrow_is_at = start_end[0]
			else:
				arrow_is_at = arrow_is_at + 1
			render_slider(default_str, start_end, arrow_is_at, False)
			while keyboard.is_pressed("right"):
				pass
		if keyboard.is_pressed("enter"):
			while keyboard.is_pressed("enter"):
				pass
			break
	return arrow_is_at
	#for the scavenging system
def gacha(luck): ###Use float(luck) percentage and output a good or bad stuff
	luck = random.randint(int(luck*100) - 100, int(luck*100)) ### Ex: 0.3 would mean 30/100 --> (30 - 100, 30) --> (-70,30)
	while luck == 0:
		luck = random.randint(int(luck*100) - 100, int(luck*100))
	return luck/abs(luck)  ###Would output either 1 or -1
	#rendering the health bar
def health_bar(health, max_health):
	print(f"HEALTH: [{health}/{max_health}]")
	print(f"|{"█"*(int(health*20/max_health))}{"▒"*((20 - int(health*20/max_health)) if health > 0 else 20)}|")
def random_distribution(summ, p, minn, maxx):
	maxx = maxx - minn
	summ -= p * minn
	if summ < 0:
		return None
	if p * maxx  >=  summ * 2:
		lst = [0] * p
		while summ > 0:
			r = random.randrange(p)
			if lst[r] < maxx:
				summ -= 1
				lst[r] += 1
	else:
		lst = [maxx] * p
		summ = maxx * p - summ
		while summ > 0:
			r = random.randrange(p)
			if lst[r] > 0:
				summ -= 1
				lst[r] -= 1
	for i in range(len(lst)):
		lst[i] += minn
	return lst


#####INITIAL VARIABLE#####
	# possible scraps that the user can get in game
scrap = [["Big bolt", "Bottles", "Brass bell", "Candy", "Clock", "Coffee mug", "Control pad", "Cookie mold pan", "Dust pan", "Fancy lamp", "Garbage lid", "Cash register", "Brass bell"], [20, 44, 48, 6, 44, 24, 34, 12, 12, 60, 20, 80, 40]]
	# possible potions 
potion = [["Strength potion", "Health potion", "Defence potion", "Cancel Charge", "Spear Charge", "Predict Future potion","Luck potion"], ["Increase damage you deal to opponent by 3", "Heal your health by 20", "Decrease damage receive from opponent by 3", "Remove the last card you pick", "Remove the last card your opponent pick", "Predict the next card in the deck", "Increase 30% of your luck (luck stat are only for scavenging, does not affect combat outcome)"]]
	# game difficulty
	# each difficulty will affect the gameplay 
		# things it will effect:
		# player stats
		# monster stats
		# quota days
game_difficulty = {
	"deadline_day": 5,
	"initial_quota": 100,
	"luck_stat": 0.7,
	"health": 150,
}
difficulty_setting = "Default"
player_action_log = []
#####CLASS#####
class Player:
	def __init__(self, health, defence, luck, strength):
		# player stats 
		# health is your hp pretty self explainatory
		self.health = health
		# defence willsubtract the total damage directed at the player
		self.defence = defence
		#luck doesn't affect the fighting only the scavenging part
		self.luck = luck
		#strength is the stat that gets multiplied by your bet amount to see how much damage you do
		self.strength = strength
		# player's inventory 
		self.inventory = [] # a list of item INDEX!!!!?!
		# seperate inventory for potions
		# potions help the user: increase strength,health,luck etc.
		self.potion_inventory = [] # a list of potion Index !!!!!REMEMBER TO DELETE ALL OF CHEAT ITEM!!!!! 
		self.money = 0

		# to add item to the inventory list
	def add_inventory(self, item_index, type):
		if type == "scrap":
			self.inventory.append(item_index)
		else:
			self.potion_inventory.append(item_index)
		# To check the player's inventory 
		# (both inventory)
	def check_inventory(self):
		self.inventory.sort()
		self.potion_inventory.sort()
		return [self.inventory, self.potion_inventory]
		#update the player current health after being dealt damage
	def got_damaged(self, damaged):
		self.health = self.health - damaged
		# for the health potion which basically heals them
	def got_healed(self, healed):
		self.health = self.health + healed

#creation of the enemy in game
class Monster:
	def __init__(self, health, defence, strength):
		#monster's hp
		self.health = health
		# all the stats have the same use as player's one but for the monster
		self.defence = defence
		self.strength = strength
		self.max_health = self.health

		# when player hits
	def got_damaged(self, damaged):
		self.health = self.health - damaged

	def got_healed(self, healed):
		self.health = self.health + healed

class Planet:
	def __init__(self, len_scrap, len_potion):
		self.name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
		self.len_scrap = len_scrap
		self.len_potion = len_potion
		self.scrap_list = [] ###Nest List of list of scrap in planet with tuple: [index_item, good_or_bad_item]
		self.potion_list = [] ###All potion considered as good item
		##################MAP STRUCTURE GENERATION######################### (this is probably the hardest part i lowkey want to die lol)
		self.room_cordinate_list = [[0,0]]
		self.have_been_there_room_list = []
		n_room = 10
		before_room_cor = [0,0]
		def check_direction(before_room_cor, room_cordinate_list):
			possible_direction = []
			up_available = [before_room_cor[0],before_room_cor[1]+1] not in room_cordinate_list
			if up_available:
				possible_direction.append("UP")
			right_available = [before_room_cor[0]+1,before_room_cor[1]] not in room_cordinate_list
			if right_available:
				possible_direction.append("RIGHT")
			down_available = [before_room_cor[0],before_room_cor[1]-1] not in room_cordinate_list
			if down_available:
				possible_direction.append("DOWN")
			left_available = [before_room_cor[0]-1,before_room_cor[1]] not in room_cordinate_list
			if left_available:
				possible_direction.append("LEFT")
			return possible_direction

		class Room:
			def __init__ (self, room_index, neighbor_room):
				self.room_index = room_index
				self.neighbor_room = neighbor_room ###List INDEX of neighbor room ["Up", "Right", "Down", "Left"]
				if self.room_index == 0:
					self.room_type = "START ROOM"
				else:
					if [1,1,1,0,0][random.randint(0,4)] == 0:
						self.room_type = "MOB ROOM"
					else:
						self.room_type = "TREASURE ROOM"
				if self.room_type == "TREASURE ROOM":
					self.treasure_position_list = []
					for i in range(random.randint(1,3)):
						treasure_position = [random.randint(1,5), random.randint(1,5)]
						while treasure_position in (self.treasure_position_list and [[3,5], [3,1], [5,3], [1,3]]):
							treasure_position = [random.randint(1,5), random.randint(1,5)]
						self.treasure_position_list.append(treasure_position)
				elif self.room_type == "MOB ROOM":
					self.room_monster = Monster(health = 20, defence = 3, strength = random.randint(4,6))
					self.monster_killed = False
				#####
				self.main_struc_wall = [[0,0], [1,0], [5,0], [6,0], [0,1], [6,1], [0,5], [6,5], [0,6], [1,6], [5,6], [6,6]]
				if neighbor_room[0] == "": #Upper wall
					for i in range(2,5):
						self.main_struc_wall.append([i, 0])
				if neighbor_room[1] == "": #Right wall
					for i in range(2,5):
						self.main_struc_wall.append([6, i])
				if neighbor_room[2] == "": #Down wall
					for i in range(2,5):
						self.main_struc_wall.append([i, 6])
				if neighbor_room[3] == "": #Left wall
					for i in range(2,5):
						self.main_struc_wall.append([0, i])
				#####

			def destroy_treasure(self, player_cor):
				self.treasure_position_list.remove(player_cor)
			def room_render(self, player_cor):
				printout_string = f"{self.room_type}\n"
				for y in range(7):
					for x in range(7):
						if [x,y] in self.main_struc_wall:
							printout_string = f"{printout_string}# "
						elif [x,y] == player_cor:
							printout_string = f"{printout_string}♥ "
						elif self.room_type == "TREASURE ROOM":
							if [x,y] in self.treasure_position_list:
								printout_string = f"{printout_string}‼ "
							else:
								printout_string = f"{printout_string}  "
						elif self.room_type == "MOB ROOM":
							if [x,y] == [3,3]:
								if self.monster_killed == False:
									printout_string = f"{printout_string}o "
								else:
									printout_string = printout_string+"\x1b[1;31;40m"+" Φ"+'\x1b[0m'
							else:
								printout_string = f"{printout_string}  "
						else:
							printout_string = f"{printout_string}  "
					printout_string = f"{printout_string}\n"
				return printout_string

		while len(self.room_cordinate_list) < n_room:
			possible_direction = check_direction(before_room_cor, self.room_cordinate_list)
			while len(possible_direction) == 0:
				for room in range(len(self.room_cordinate_list)-1, -1, -1):
					if len(check_direction(self.room_cordinate_list[room], self.room_cordinate_list)) != 0:
						room_with_direction = room
						break
				before_room_cor = self.room_cordinate_list[room_with_direction]
				possible_direction = check_direction(before_room_cor, self.room_cordinate_list)
			else:
				gacha_direction = possible_direction[random.randint(0,len(possible_direction)-1)]
				if gacha_direction == "UP":
					before_room_cor = [before_room_cor[0],before_room_cor[1]+1] #(x,y+1)
					self.room_cordinate_list.append(before_room_cor)
				elif gacha_direction == "RIGHT":
					before_room_cor = [before_room_cor[0]+1,before_room_cor[1]] #(x+1,y)
					self.room_cordinate_list.append(before_room_cor)
				elif gacha_direction == "DOWN":
					before_room_cor = [before_room_cor[0],before_room_cor[1]-1] #(x,y-1)
					self.room_cordinate_list.append(before_room_cor)
				elif gacha_direction == "LEFT":
					before_room_cor = [before_room_cor[0]-1,before_room_cor[1]] #(x-1,y)
					self.room_cordinate_list.append(before_room_cor)
		self.room_list = []
		for room in range(len(self.room_cordinate_list)):
			room_cord = self.room_cordinate_list[room]
			neighbor_room_list = ["","","",""] #Up right down left
			for neighbor_room in range(len(self.room_cordinate_list)):
				if [self.room_cordinate_list[room][0],self.room_cordinate_list[room][1]+1] == self.room_cordinate_list[neighbor_room]: #Up
					neighbor_room_list[0] = neighbor_room
				elif [self.room_cordinate_list[room][0]+1,self.room_cordinate_list[room][1]] == self.room_cordinate_list[neighbor_room]: #Right
					neighbor_room_list[1] = neighbor_room
				elif [self.room_cordinate_list[room][0],self.room_cordinate_list[room][1]-1] == self.room_cordinate_list[neighbor_room]: #Down
					neighbor_room_list[2] = neighbor_room
				elif [self.room_cordinate_list[room][0]-1,self.room_cordinate_list[room][1]] == self.room_cordinate_list[neighbor_room]: #Left
					neighbor_room_list[3] = neighbor_room
			self.room_list.append(Room(room, neighbor_room_list))
		self.total_treasure = sum([len(room.treasure_position_list) for room in self.room_list if room.room_type == "TREASURE ROOM"]) #To statisticize how many treasure in a whole map
	def map_render(self, player_at_room):
		for y in range(max([self.room_cordinate_list[i][1] for i in range(len(self.room_cordinate_list))]), min([self.room_cordinate_list[i][1] for i in range(len(self.room_cordinate_list))]) - 1, -1):
			for x in range(min([self.room_cordinate_list[i][0] for i in range(len(self.room_cordinate_list))]), max([self.room_cordinate_list[i][0] for i in range(len(self.room_cordinate_list))]) + 1, 1):
				if [x,y] == self.room_cordinate_list[player_at_room]:
					print("█", end = "")
				elif [x,y] == [0,0]:
					print("▲", end = "")
				elif [x,y] in self.room_cordinate_list:
					if self.room_cordinate_list.index([x,y]) in self.have_been_there_room_list:
						print(('\x1b[1;32;40m' if self.room_list[self.room_cordinate_list.index([x,y])].room_type == "TREASURE ROOM" else '\x1b[1;31;40m') + "#" + '\x1b[0m', end = "")
					else:
						print("#", end = "")
				else:
					print(".", end = "")
			print("")
		print("_________")
	###############################################################################################################################
	def item_generation(self, player_luck): #Item will be generate: (good_item) = (total_item) * (player_luck) - (potion); Condition: (total_item)*(player_luck) >= (potion)
		for i in range(self.len_potion): #Gacha potion
			self.potion_list.append(random.randint(0, len(potion[0])-1))
		for i in range(int(self.len_scrap*player_luck) - self.len_potion): #Gacha good item
			gacha_item_index = random.randint(0,len(scrap[0])-1)
			while scrap[1][gacha_item_index] <= 40: ###Gacha until found good stuff
				gacha_item_index = random.randint(0,len(scrap[0])-1)
			self.scrap_list.append([gacha_item_index, "good"])
		for i in range(int(self.len_scrap*(1-player_luck)) + self.len_potion): #(bad_item) = (total_item) - (good_item) = (total_item) * (1 - (player_luck)) + (potion)
			gacha_item_index = random.randint(0,len(scrap[0])-1)
			while scrap[1][gacha_item_index] > 40: ###Gacha until found good stuff
				gacha_item_index = random.randint(0,len(scrap[0])-1)
			self.scrap_list.append([gacha_item_index, "bad"])
	def distribute_loot_to_treasure(self):
		self.treasure_lenitem_list = random_distribution(len(self.scrap_list) + len(self.potion_list), self.total_treasure, 0, 100)
	def scavage(self, player_luck):
		num_of_item_founded = self.treasure_lenitem_list[0]
		self.treasure_lenitem_list.pop(0)
		item_founded = [[],[]]
		for cycle in range(num_of_item_founded):
			#########Check for avaiablility of scraps and potions in planet
			item_flag_avaiable = 0
			first_difference = self.scrap_list[0][1]
			if first_difference == "good":
				if "bad" in [item[1] for item in self.scrap_list]:
					item_flag_avaiable = 2
			else:
				if "good" in [item[1] for item in self.scrap_list]:
					item_flag_avaiable = 2
			if item_flag_avaiable != 2:
				if first_difference == "good":
					item_flag_avaiable = 1
				else:
					item_flag_avaiable = 0
			if len(self.potion_list) != 0:
				potion_flag_avaiable = 1
			else:
				potion_flag_avaiable = 0
			##########
			gacha_luck = gacha(current_player.luck)
			if gacha_luck == 1: ###Good luck
				if potion_flag_avaiable == 1 and (item_flag_avaiable == 2 or item_flag_avaiable == 1):
					if random.randint(0,1) == 0:
						gacha_item_index = random.randint(0, len(self.potion_list)-1)
						item_founded[1].append(self.potion_list[gacha_item_index])
						self.potion_list.pop(gacha_item_index)
					else:
						i = 0
						while self.scrap_list[i][1] == "good":
							i = i + 1
						item_founded[0].append(self.scrap_list[i][0])
						self.scrap_list.pop(i)
				elif potion_flag_avaiable == 1:
					gacha_item_index = random.randint(0, len(self.potion_list)-1)
					item_founded[1].append(self.potion_list[gacha_item_index])
					self.potion_list.pop(gacha_item_index)
				elif (item_flag_avaiable == 2 or item_flag_avaiable == 1):
					i = 0
					while self.scrap_list[i][1] == "good":
						i = i + 1
					item_founded[0].append(self.scrap_list[i][0])
					self.scrap_list.pop(i)
				else:
					item_founded[0].append(self.scrap_list[0][0])
					self.scrap_list.pop(0)
			else: ###Bad luck
				if item_flag_avaiable == 2 or item_flag_avaiable == 0:
					if item_flag_avaiable == 2:
						i = 0
						while self.scrap_list[i][1] == "bad":
							i = i + 1
						item_founded[0].append(self.scrap_list[i][0])
						self.scrap_list.pop(i)
					else:
						item_founded[0].append(self.scrap_list[0][0])
						self.scrap_list.pop(0)
				else:
					if potion_flag_avaiable == 1 and item_flag_avaiable == 1:
						if random.randint(0,1) == 0:
							gacha_item_index = random.randint(0, len(self.potion_list)-1)
							item_founded[1].append(self.potion_list[gacha_item_index])
							self.potion_list.pop(gacha_item_index)
						else:
							item_founded[0].append(self.scrap_list[0][0])
							self.scrap_list.pop(0)
					elif potion_flag_avaiable == 1:
						gacha_item_index = random.randint(0, len(self.potion_list)-1)
						item_founded[1].append(self.potion_list[gacha_item_index])
						self.potion_list.pop(gacha_item_index)
					else:
						item_founded[0].append(self.scrap_list[0][0])
						self.scrap_list.pop(0)
		return item_founded

#### Menu screen
title_answer = 0
while title_answer != "Play":
	os.system('cls' if os.name == "nt" else "clear")
	title = pyfiglet.figlet_format("Intergalactic Battle", font = "big")
	print(title)
	title_answer = display_selection(["Play", "Option", "Help", "Quit"])
	os.system('cls' if os.name == "nt" else "clear")
	if title_answer == "Option":
		option = pyfiglet.figlet_format("Option", font = "small")
		print(option)
		print(f"--Difficulty is setting at: [{difficulty_setting}]--")
		option_answer = display_selection(["Default","Intermediate", "Hard", "Hardcore 💀", "Back"])
		if option_answer == "Default":
			difficulty_setting = "Default"
			game_difficulty["deadline_day"] = 5
			game_difficulty["initial_quota"] = 100
			game_difficulty["luck_stat"] = 0.7
			game_difficulty["health"] = 150
		if option_answer == "Intermediate":
			difficulty_setting = "Intermediate"
			game_difficulty["deadline_day"] = 5
			game_difficulty["initial_quota"] = 200
			game_difficulty["luck_stat"] = 0.5
			game_difficulty["health"] = 80
		if option_answer == "Hard":
			difficulty_setting = "Hard"
			game_difficulty["deadline_day"] = 4
			game_difficulty["initial_quota"] = 300
			game_difficulty["luck_stat"] = 0.5
			game_difficulty["health"] = 30
		if option_answer == "Hardcore 💀":
			difficulty_setting = "Hardcore 💀"
			game_difficulty["deadline_day"] = 3
			game_difficulty["initial_quota"] = 500
			game_difficulty["luck_stat"] = 0.25
			game_difficulty["health"] = 10
	if title_answer == "Help":
		print("General Gameplay:")
		print("Depend on your difficulty, you will have a quota and deadline for that quota")
		print("You have to collect scraps, sell in shop to have enough money")
		print("You can buy items in shop for healing or support in fight")
		press_enter_to_continue()
		print("Scavenging system:")
		print("There will be 10 rooms in each planet")
		print("Room can be a treasure or monster room, you can see the map structure on top too")
		print("Treasure room will be labeled in green and monster room will be labeled in red, undiscovered room will be labeled in white until being discovered")
		print("Press WASD to move around")
		print("In treasure room, you can interact with ‼ to collect scraps and potions")
		print("To return to spaceship, go back to \"START ROOM\" and press [b]")
		press_enter_to_continue()
		print("Fighting system:")
		print("A game of BlackJack but instead of cards and bets, you will have strength and health")
		print("There are [1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11] energy orbs in one battle field (Caution: one and ONLY one, no repititions)")
		print("Each player will first recieve 2 cards, 1 will be hidden and the other will be seen by the opponent")
		print("Each player will take turn picking up card until the two player choose to stay")
		print("Whoever reach closest to 21 will win the clash and deal [bet] amount of damage to the other. If both player have equal range to 21, the one didn't overpast 21 will win")
		print("Whoever lost their health first lose the battle")
		print("There will be potion to use for their advantage, this include: {")
		print("Strength potion: increase [bet] amount (deal more damage)")
		print("Defence potion: decrease [bet] amount (deal less damage)")
		print("Cancel Charge: cancel player last card picked")
		print("Spear Charge: cancel opponent last card picked")
		print("Predict future: predict next card picked")
		press_enter_to_continue()

	if title_answer == "Quit":
		exit()

today_date = 1
###PLAYER GENERATION###
current_player = Player(health = game_difficulty["health"], defence = 3, luck = game_difficulty["luck_stat"], strength = 5)
###GAME GENERATION###
planets = []
for i in range(3): 
	planets.append(Planet(
		len_scrap = random.randint(14,20), #Condition: (total_item)*(player_luck) >= (potion)
		len_potion = random.randint(2,4)
		))
while (game_difficulty["deadline_day"] - today_date) > 0:
	today_date = today_date + 1
	current_player.health = game_difficulty["health"]
	while True:
		os.system('cls' if os.name == "nt" else "clear")
		print("WELCOME BACK TO THE INTERVAL GATEWAY")
		print(f"You have {game_difficulty["deadline_day"] - today_date} days left to reach the quota")
		print(f"PROFIT QUOTA: {current_player.money}/{game_difficulty["initial_quota"]}")
		gateway_answer = display_selection([["MOONS", "STORE","Quit game"], ["To see the lists of moons the autopilot can route to.", "To see the company store's selection of useful items.",""]])
		if gateway_answer == "Quit game":
			exit()
		os.system('cls' if os.name == "nt" else "clear")
		if gateway_answer == "STORE":
			shop_answer = 0
			while shop_answer != "Back":
				print("Welcome to the")
				print(pyfiglet.figlet_format("COMPANY SHOP", font = "drpepper"))
				print("You can buy items by selecting an item")
				print("You can sell all of your scraps in your inventory to cashout")
				print("----------------------------------------")
				print(f"Money: {current_player.money}$")
				shop_answer = display_selection([[potion[0][i] for i in range(len(potion[0]))] + ["--> SELL ALL YOUR ITEM <--", "Back"], [f"{potion_description}  //  Price: 50$" for potion_description in potion[1]] + ["", ""]])
				if shop_answer == "--> SELL ALL YOUR ITEM <--":
					os.system('cls' if os.name == "nt" else "clear")
					inventory, potion_inventory = current_player.check_inventory()
					print("----Inventory----")
					if len(inventory) == 0:
						print('\x1b[3;37;40m'+"-Empty-"+'\x1b[0m')
						print("You have nothing to sell")
					else:
						for i in range(len(inventory)):
							print(f"{scrap[0][inventory[i]]} -- {scrap[1][inventory[i]]}$")
						print(f"-> You earn: {sum([scrap[1][inventory[i]] for i in range(len(inventory))])}$")
						player_action_log.append(f"You sell all of your scraps and you have {current_player.money}$")
						current_player.money = current_player.money + sum([scrap[1][inventory[i]] for i in range(len(inventory))])
						current_player.inventory = []
					print(f"You now have: {current_player.money}$")
					press_enter_to_continue()
				elif shop_answer == "Back":
					pass
				else:
					if current_player.money >= 50:
						current_player.potion_inventory.append(potion[0].index(shop_answer))
						print(f"You have bought {shop_answer} for 50$")
						player_action_log.append(f"You buy {shop_answer} for 50$")
						current_player.money = current_player.money - 50
						press_enter_to_continue()
					else:
						print(f"You don't have enough money to buy {shop_answer}")
						press_enter_to_continue()
		else:
			print("Welcome to the exomoons catalogue.")
			print("Select the moon you want to go to route the autopilot")
			print("----------------------------------------")
			moon_go_to_answer = display_selection([f"* Planet {planet.name}" for planet in planets] + ["Back"])
			if moon_go_to_answer != "Back":
				player_action_log.append(f"You choose to go to {moon_go_to_answer} planet")
				break


	###PLANET GENERATION###
	current_planet = planets[[planet.name for planet in planets].index(moon_go_to_answer.split()[2])]
	current_planet.item_generation(current_player.luck)
	current_planet.distribute_loot_to_treasure()

	idle_answer = 0
	while (idle_answer != "Return to INTERVAL GATEWAY") and (current_player.health > 0) :
		os.system('cls' if os.name == "nt" else "clear")
		print(f"Your spaceship have arrived at planet [{current_planet.name}]")
		print(f"\n\n")
		idle_answer = display_selection(["Scavage", "Check Inventory", "Check Player's stat", "Return to INTERVAL GATEWAY"])
		os.system('cls' if os.name == "nt" else "clear")
		if idle_answer == "Scavage":
			player_cor = [3,3]
			player_at_room = current_planet.room_list[0]
			current_planet.map_render(player_at_room.room_index)
			print(player_at_room.room_render(player_cor))
			while True:
				if player_at_room.room_index not in current_planet.have_been_there_room_list:
					current_planet.have_been_there_room_list.append(player_at_room.room_index)
				if player_at_room.room_type == "TREASURE ROOM":
					if [player_cor[0], player_cor[1]] in player_at_room.treasure_position_list: #If player touch treasure
						os.system('cls' if os.name == "nt" else "clear")
						player_at_room.destroy_treasure(player_cor)
						item_founded = current_planet.scavage(current_player.luck)
						print("-----SCRAP FOUND:-----")
						if len(item_founded[0]) == 0:
							print('\x1b[3;37;40m'+"-Empty-"+'\x1b[0m')
						else:
							print(f"You found {len(item_founded[0])} items:")
							player_action_log.append(f"You found {[scrap[0][item_index] for item_index in item_founded[0]] + [potion[0][item_index] for item_index in item_founded[1]]}")
							for item_index in item_founded[0]:
								print(f"{scrap[0][item_index]}   {scrap[1][item_index]}$")
								current_player.add_inventory(item_index, "scrap")
						###Show found potion
						print("-----POTION FOUND:-----")
						if len(item_founded[1]) == 0:
							print('\x1b[3;37;40m'+"-Empty-"+'\x1b[0m')
						else:
							print(f"You found {len(item_founded[1])} potions:")
							for potion_index in item_founded[1]:
								print(f"{potion[0][potion_index]}")
								current_player.add_inventory(potion_index, "potion")
						press_enter_to_continue()
						current_planet.map_render(player_at_room.room_index)
						print(player_at_room.room_render(player_cor))
				elif player_at_room.room_type == "MOB ROOM":
					if player_at_room.monster_killed == False:
						print('\x1b[5;30;41m'+"YOU ENCOUNTER A MONSTER!!!"+'\x1b[0m')
						player_action_log.append(f"You encouter and fight a monster")
						press_enter_to_continue()
						monster1 = player_at_room.room_monster
						while (current_player.health > 0) and (monster1.health > 0):
							deck = [1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11]
							random.shuffle(deck)
							player_stand = False
							bet_amount = display_slider((1, 10), "How much do you want to bet?: ")
							print("-----")
							player_hand = []
							opponent_hand = []
							for i in range(2):
								player_hand.append(deck[0])
								deck.pop(0)
							for i in range(2):
								opponent_hand.append(deck[0])
								deck.pop(0)
							###
							strength_potion_buff = 0
							defence_potion_buff = 0
							###
							print(f"You have {player_hand}")
							opponent_hand_display = [i for i in opponent_hand]
							opponent_hand_display[0] = "Hidden"
							print(f"Your opponent have {opponent_hand_display}")
							###Player turn
							move_answer = display_selection(["Hit", "Stand","Inventory","Instant Kill (for DEV)","Quit game (for DEV)"])
							n_player_pick = 0
							while True:
								if move_answer == "Stand": ###STAND
									print("---You stand---")
									break
								elif len(deck) == 0:
									print("There is no card left, you have to stay")
									break
								elif move_answer == "Hit": ###HIT
									player_hand.append(deck[0])
									print(f"You hit a {deck[0]} --> Total: {sum(player_hand)}")
									deck.pop(0)
									move_answer = display_selection(["Hit", "Stand","Inventory","Instant Kill (for DEV)","Quit game (for DEV)"])
								elif move_answer == "Inventory": ###USE INVENTORY
									potion_inventory = current_player.check_inventory()[1]
									potion_description = [potion[1][i] for i in potion_inventory]
									potion_inventory = [potion[0][i] for i in potion_inventory] ###We have to convert the list of index to the list of name potion
									inventory_answer = display_selection([potion_inventory + ["Back"],potion_description + [""]])
									if inventory_answer == "Back":
										pass
									elif inventory_answer == "Strength potion":
										strength_potion_buff = strength_potion_buff + 3
										current_player.potion_inventory.remove(0)
										print(f"You use strength potion. Your strength is now {current_player.strength+strength_potion_buff}")
									elif inventory_answer == "Health potion":
										print("You can not heal while in combat")
									elif inventory_answer == "Defence potion":
										defence_potion_buff = defence_potion_buff + 3
										print(f"You use defence potion. Your defence is now {current_player.defence+defence_potion_buff}")
										current_player.potion_inventory.remove(2)
									elif inventory_answer == "Cancel Charge":
										if len(player_hand) > 0:
											print(f"You use cancel charge, card {player_hand[-1]} will be removed and insert back to deck")
											card_number = player_hand[-1]
											player_hand.pop(-1)
											deck.append(card_number)
											print(f"You have: {player_hand} --> Total: {sum(player_hand)}")
											current_player.potion_inventory.remove(3)
										else:
											print("You don't have any card, you can't use this potion")
									elif inventory_answer == "Spear Charge":
										if len(opponent_hand) > 0:
											print(f"You use spear charge on your enemy, card {opponent_hand[-1]} will be removed and insert back to deck")
											card_number = opponent_hand[-1]
											opponent_hand.pop(-1)
											deck.append(card_number)
											opponent_hand_display = [card for card in opponent_hand]
											if len(opponent_hand_display) > 0:
												opponent_hand_display[0] = "Hidden"
											print(f"Your opponent have: {opponent_hand_display}")
											current_player.potion_inventory.remove(4)
										else:
											print("Your opponent don't have any card, you can't use this potion")
									elif inventory_answer == "Predict Future potion":
										if len(deck) > 0:
											print(f"You use predict future potion, your opponent got confused and distracted, you can see the next card is: {deck[0]}")
											current_player.potion_inventory.remove(5)
										else:
											print("There is no card left on the deck, you can't use this potion")
									elif inventory_answer == "Luck potion":
										print("This potion can only be used when scavenging, luck stat does not affect the outcome of the combat")
									move_answer = display_selection(["Hit", "Stand","Inventory","Instant Kill (for DEV)","Quit game (for DEV)"])
								elif move_answer == "Instant Kill (for DEV)":
									monster1.health = 0
									break
								else:
									exit()
							###Opponent turn
							n_opponent_pick = 0
							while True:
								time.sleep(1)
								if len(deck) == 0:
									break
								else:
									if (deck[0] + sum(opponent_hand)) <= 21:
										opponent_hand.append(deck[0])
										print(f"Your opponent hit a {deck[0]}")
										deck.pop(0)
									else:
										break
							print("---Your opponent stand---")
							###############
							player_win_flag = 0
							oppo_win_flag = 0
							if sum(player_hand) == sum(opponent_hand):
								player_win_flag	= 1
								oppo_win_flag = 1
							elif (sum(player_hand) <= 21) and (sum(opponent_hand) <= 21):
								if (21 - sum(player_hand)) < (21 - sum(opponent_hand)):
									player_win_flag = 1
								else:
									oppo_win_flag = 1
							else:
								if (sum(player_hand) <= 21) or (sum(opponent_hand) <= 21):
									player_win_flag	= int(bool(sum(player_hand) <= 21))
									oppo_win_flag = int(bool(sum(opponent_hand) <= 21))
								else:
									if (sum(player_hand) - 21) < (sum(opponent_hand) - 21):
										player_win_flag = 1
									else:
										oppo_win_flag = 1
							print(f"You have {player_hand} ==> {sum(player_hand)}")
							print(f"Your opponent have {opponent_hand} ==> {sum(opponent_hand)}")
							if (player_win_flag	== 1) and (oppo_win_flag == 1):
								print(f"Draw. So charge got cancelled and no one deal damage")
								print("------------------------------------------------------------")
							else:
								if player_win_flag == 1:
									print('\x1b[1;32;40m'+"You won"+'\x1b[0m'+f"\nYou deal {(bet_amount * current_player.strength - monster1.defence) if current_player.strength > monster1.defence else 0} damage to your opponent")
									monster1.got_damaged((bet_amount * current_player.strength - monster1.defence) if current_player.strength > monster1.defence else 0)
									print("------------------------------------------------------------")
								elif oppo_win_flag == 1:
									print('\x1b[1;31;40m'+"Your opponent won"+'\x1b[0m'+f"\nThey deal {(bet_amount * monster1.strength - current_player.defence) if monster1.strength > current_player.defence else 0} damage to you")
									current_player.got_damaged((bet_amount * monster1.strength - current_player.defence) if monster1.strength > current_player.defence else 0)
									print("------------------------------------------------------------")
							if current_player.health != 0 and monster1.health != 0:
								print(f"Your current health: ")
								health_bar(current_player.health,game_difficulty["health"])
								print(f"Your opponent current health: ")
								health_bar(monster1.health,monster1.max_health)
							else:
								if current_player.health <= 0:
									print(f"Your current health: ",end = ' ')
									health_bar(0,game_difficulty["health"])
								if monster1.health <= 0:
									print(f"Your opponent current health: ", end= ' ')
									health_bar(0,monster1.max_health)
							press_enter_to_continue()
						if current_player.health > 0:
							you_win = pyfiglet.figlet_format("You win", font = "chunky")
							print('\x1b[1;32;40m'+you_win+'\x1b[0m')
							player_action_log.append(f"You win and kill the monster")
							player_at_room.monster_killed = True
						else:
							you_lose = pyfiglet.figlet_format("You lose",font = "chunky")
							print('\x1b[1;31;40m'+you_lose+'\x1b[0m')
							player_action_log.append(f"You lose and the monster killed you")
							time.sleep(1)
							print("You will be respawned at the INTERVAL GATEWAY, but all of your inventory will be gone")
							current_player.potion_inventory = []
							current_player.inventory = []
							time.sleep(1)
							press_enter_to_continue()
							break
						press_enter_to_continue()
						current_planet.map_render(player_at_room.room_index)
						print(player_at_room.room_render(player_cor))
				if keyboard.is_pressed("up"):
					os.system('cls' if os.name == "nt" else "clear")
					if [player_cor[0],player_cor[1]-1] not in player_at_room.main_struc_wall: #If player not touch wall
						door = []
						for i in range(2,5):
							door.append([i,0])
						if [player_cor[0], player_cor[1]-1] in door: #If player touch door
							player_at_room = current_planet.room_list[player_at_room.neighbor_room[0]]
							player_cor = [3,5]

						else:
							player_cor = [player_cor[0], player_cor[1]-1]
					current_planet.map_render(player_at_room.room_index)
					print(player_at_room.room_render(player_cor))
					if player_at_room.room_index == 0:
						print("HINT: YOU ARE CURRENTLY AT [START ROOM]. TO RETURN TO SPACESHIP, PRESS \"B\"")
					while keyboard.is_pressed("up"):
						pass
				if keyboard.is_pressed("down"):
					os.system('cls' if os.name == "nt" else "clear")
					if [player_cor[0],player_cor[1]+1] not in player_at_room.main_struc_wall: #If player not touch wall
						door = []
						for i in range(2,5):
							door.append([i,6])
						if [player_cor[0], player_cor[1]+1] not in door: #If player not touch door
							player_cor = [player_cor[0], player_cor[1]+1]
						else:
							player_at_room = current_planet.room_list[player_at_room.neighbor_room[2]]
							player_cor = [3,1]
					current_planet.map_render(player_at_room.room_index)
					print(player_at_room.room_render(player_cor))
					if player_at_room.room_index == 0:
						print("HINT: YOU ARE CURRENTLY AT [START ROOM]. TO RETURN TO SPACESHIP, PRESS \"B\"")
					while keyboard.is_pressed("down"):
						pass
				if keyboard.is_pressed("left"):
					os.system('cls' if os.name == "nt" else "clear")
					if [player_cor[0]-1,player_cor[1]] not in player_at_room.main_struc_wall: #If player not touch wall
						door = []
						for i in range(2,5):
							door.append([0,i])
						if [player_cor[0]-1, player_cor[1]] not in door: #If player not touch door
							player_cor = [player_cor[0]-1, player_cor[1]]
						else:
							player_at_room = current_planet.room_list[player_at_room.neighbor_room[3]]
							player_cor = [5,3]
					current_planet.map_render(player_at_room.room_index)
					print(player_at_room.room_render(player_cor))
					if player_at_room.room_index == 0:
						print("HINT: YOU ARE CURRENTLY AT [START ROOM]. TO RETURN TO SPACESHIP, PRESS \"B\"")
					while keyboard.is_pressed("left"):
						pass
				if keyboard.is_pressed("right"):
					os.system('cls' if os.name == "nt" else "clear")
					if [player_cor[0]+1,player_cor[1]] not in player_at_room.main_struc_wall: #If player not touch wall
						door = []
						for i in range(2,5):
							door.append([6, i])
						if [player_cor[0]+1, player_cor[1]] not in door: #If player not touch door
							player_cor = [player_cor[0]+1, player_cor[1]]
						else:
							player_at_room = current_planet.room_list[player_at_room.neighbor_room[1]]
							player_cor = [1,3]
					current_planet.map_render(player_at_room.room_index)
					print(player_at_room.room_render(player_cor))
					if player_at_room.room_index == 0:
						print("HINT: YOU ARE CURRENTLY AT [START ROOM]. TO RETURN TO SPACESHIP, PRESS \"B\"")
					while keyboard.is_pressed("right"):
						pass
				if keyboard.is_pressed("b") and player_at_room.room_index == 0:
					break
		if idle_answer == "Check Inventory":
			print(f"Money: {current_player.money}$")
			inventory, potion_inventory = current_player.check_inventory()
			print("----Inventory----")
			if len(inventory) == 0:
				print('\x1b[3;37;40m'+"-Empty-"+'\x1b[0m')
			else:
				for i in range(len(inventory)):
					print(f"{scrap[0][inventory[i]]} -- {scrap[1][inventory[i]]}$")
				print(f"-> Potential total money: {sum([scrap[1][inventory[i]] for i in range(len(inventory))])}$")
			print("---Potion Inventory---")
			if len(potion_inventory) == 0:
				print('\x1b[3;37;40m'+"-Empty-"+'\x1b[0m')
				press_enter_to_continue()
			else:
				potion_inventory = current_player.check_inventory()[1]
				potion_description = [(('\x1b[1;31;40m' if i in [0,2,3,4,5] else '\x1b[0;37;40m') + potion[1][i] + (" (CAN ONLY USE IN COMBAT)" if i in [0,2,3,4,5] else "") + '\x1b[0m') for i in potion_inventory]
				use_potion_in_inventory_answer = display_selection([[potion[0][i] for i in potion_inventory] + ["Back"],potion_description + [""]])
				while use_potion_in_inventory_answer != "Health potion" and use_potion_in_inventory_answer != "Luck potion" and use_potion_in_inventory_answer != "Back":
					use_potion_in_inventory_answer = display_selection([[potion[0][i] for i in potion_inventory] + ["Back"],potion_description + [""]])
				if use_potion_in_inventory_answer == "Health potion":
					current_player.health = current_player.health + 20
					if current_player.health > game_difficulty["health"]:
						current_player.health = game_difficulty["health"]
					current_player.potion_inventory.remove(1)
					health_bar(current_player.health, game_difficulty["health"])
					press_enter_to_continue()
				elif use_potion_in_inventory_answer == "Luck potion":
					prev_luck = current_player.luck
					current_player.luck = current_player.luck + (1 - current_player.luck) * 0.3
					current_player.potion_inventory.remove(6)
					print(f"Your luck have been increase from {prev_luck} ---> {current_player.luck}")
					press_enter_to_continue()

		if idle_answer == "Check Player's stat":
			print("---STAT---")
			health_bar(current_player.health, game_difficulty["health"])
			print(f"Strength: {current_player.strength}")
			print(f"Defence: {current_player.defence}")
			print(f"Luck: {current_player.luck*100}%")
			press_enter_to_continue()
print("Your time has end")
if current_player.money >= game_difficulty["initial_quota"]:
	print("You have reached quota. Congrat, you win yipee")
	print("---log---")
	for log in player_action_log:
		print(log)
	press_enter_to_continue()
else:
	print("You have not reached quota. u lose, womp womp")
	print("---log---")
	for log in player_action_log:
		print(log)
	press_enter_to_continue()





