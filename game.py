import os, sys

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

class Game:
  def __init__(self):
    self.x, self.y = 2, 2
    with open("level.txt", "r", encoding="utf-8") as f:
      layout = f.readlines()
    layout = [l.strip() for l in layout]
    self.layout = layout
    self.objects = {"W":"░", "D": "◎", "K": "◉", "P": "●", "I": "◌", "F": "F"}
    self.key_loc, self.door_loc, self.flag_loc = None, None, None
    self.has_key = False

    self._init_map()
    self._update()

  def _init_map(self):
    new_layout = []
    for y in self.layout:
      letters = list(y)
      nl = [self.objects[l] for l in letters]
      new_layout.append("".join(nl))
    self.layout = new_layout

    for idx in range(len(self.layout)):
      if self.objects["K"] in self.layout[idx]:
        self.key_loc = (self.layout[idx].index(self.objects["K"]), idx)
      if self.objects["D"] in self.layout[idx]:
        self.door_loc = (self.layout[idx].index(self.objects["D"]), idx)
      if self.objects["F"] in self.layout[idx]:
        self.flag_loc = (self.layout[idx].index(self.objects["F"]), idx)
  
  def _update(self):
    level = "\n".join(self.layout)
    os.system("cls" if os.name == "nt" else "clear")
    print(level + "\nMove with WASD:")
    prompt = get_key()
    
    last_x, last_y = self.x, self.y
    if prompt.lower() == "a":
      if self.layout[self.y][self.x - 1] != self.objects["W"]:
        self.x -= 1
    elif prompt.lower() == "d":
      if self.layout[self.y][self.x + 1] not in [self.objects["W"], self.objects["D"]]:
        self.x += 1
    elif prompt.lower() == "s":
      if self.layout[self.y + 1][self.x] != self.objects["W"]:
        self.y += 1
    elif prompt.lower() == "w":
      if self.layout[self.y - 1][self.x] != self.objects["W"]:
        self.y -= 1
    
    new_layout = self.layout
    
    new_layout[self.y] = new_layout[self.y][:self.x] + self.objects["P"] + new_layout[self.y][self.x + 1:]
    
    if self.x != last_x or self.y != last_y:
      new_layout[last_y] = new_layout[last_y][:last_x] + self.objects["I"] + new_layout[last_y][last_x + 1:]
    self.layout = new_layout
    
    if self.x == self.key_loc[0] and self.y == self.key_loc[1]:
      self.has_key = True
    
    if self.has_key and self.x != self.door_loc[0] and self.y != self.door_loc[1]:
      new_layout = self.layout
      new_layout[self.door_loc[1]] = new_layout[self.door_loc[1]][:self.door_loc[0]] + self.objects["I"] + new_layout[self.door_loc[1]][self.door_loc[0] + 1:]
  
  def _game_loop(self):
    playing = True
    while playing:
      self._update()
      if self.x == self.flag_loc[0] and self.y == self.flag_loc[1]:
        playing = False
    if not playing:
      print("You won!")

game = Game()
game._game_loop()