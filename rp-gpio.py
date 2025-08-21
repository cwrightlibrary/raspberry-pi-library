import sys
import os

if os.name == "nt":
  import msvcrt
else:
  import tty
  import termios

def get_key():
	if os.name == "nt":
		return msvcrt.getch().decode("utf-8").lower()
	else:
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			ch = sys.stdin.read(1).lower()
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

class LED:
	def __init__(self, on=False, is_wall=False, is_door=False, is_key=False):
		self.light = ""

		self.on = on
		self.is_wall = is_wall
		self.is_door = is_door
		self.is_key = is_key

		if not self.is_wall and not self.is_door and not self.is_key:
			self.light = "●" if self.on else "◌"

		if not self.on:
			if self.is_wall:
				self.light = "░"
			elif self.is_door:
				self.light = "◎"
			elif self.is_key:
				self.light = "◉"

		def switch(self):
			self.on = not self.on
			self.light = "●" if self.on else "◌"

		def __str__(self):
			return self.light


class Level:
	def __init__(self):
		self.text_layout = [
			'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
			'WIIIIIIIIIIIIIIIIIIIIIIWIIIIIW',
			'WIIIIIIIIIWWWIIIIIIIIIIDFIIIIW',
			'WIIIIIIIIIIKWIIIIIIIIIIWIIIIIW',
			'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
		]
		self.light_layout = []
		self.wall = LED(is_wall=True)
		self.inactive = LED(on=False)
		self.key = LED(is_key=True)
		self.door = LED(is_door=True)

		self.layout = []
		for x in self.text_layout:
			new_x = x.replace("W", self.wall.light).replace("I", self.inactive.light).replace("K", self.key.light).replace("D", self.door.light)
			self.layout.append(new_x)

	def __str__(self):
		return "\n".join(self.layout)


class Player:
	def __init__(self, layout):
		self.x, self.y = 2, 2
		self.layout = layout.layout
		self.on = LED(on=True)
		self.off = LED(on=False)
		self.has_key = False
		self.got_flag = False

		new_layout = self.layout
		new_layout[self.y] = new_layout[self.y][:self.x] + self.on.light + new_layout[self.y][self.x + 1:]
	
	def update_player(self):
		level = "\n".join(self.layout)
		os.system('cls' if os.name == 'nt' else 'clear')
		print(level + "\nMove with WASD:")
		prompt = get_key()
		last_x, last_y = self.x, self.y
		if prompt.lower() == "a":
			# self.x -= 1 if self.x > 1 else 0
			if self.layout[self.y][self.x - 1] != "░":
				self.x -= 1
		elif prompt.lower() == "d":
			# self.x += 1 if self.x < len(self.layout[0]) - 1 else 0
			if self.layout[self.y][self.x + 1] not in ["░", "◎"]:
				self.x += 1
		elif prompt.lower() == "s":
			# self.y += 1 if self.y < len(self.layout) - 2 else 0
			if self.y != len(self.layout) and self.layout[self.y + 1][self.x] != "░":
				self.y += 1
		elif prompt.lower() == "w":
			# self.y -= 1 if self.y > 0 else 0
			if self.y > 0 and self.layout[self.y - 1][self.x] != "░":
				self.y -= 1
		
		new_layout = self.layout

		new_layout[self.y] = new_layout[self.y][:self.x] + self.on.light + new_layout[self.y][self.x + 1:]

		if self.x != last_x or self.y != last_y:
			new_layout[last_y] = new_layout[last_y][:last_x] + self.off.light + new_layout[last_y][last_x + 1:]
		self.layout = new_layout

		if self.x == 11 and self.y == 3:
			self.has_key = True
		
		if self.has_key and self.y != 2 and self.x != 23:
			new_layout = self.layout
			new_layout[2] = new_layout[2][:23] + "◌" + new_layout[2][24:]
	
	def game_loop(self):
		playing = True
		while playing:
			self.update_player()
			if self.x == 24 and self.y == 2:
				playing = False
		if not playing:
			print("You won!")

level = Level()
player = Player(level)

player.game_loop()
