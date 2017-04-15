import tkinter as tk
from tkinter import messagebox
import random
import time

# Parameters for Q-Learning
alpha = 0.1 # learning rate
gamma = 0.8 # discount factor
epsilon = 0.2 # chance to choose random action

# Visual envirnoments parameters
rectangle_size = 100
default_color = 'white'
player_color = 'red'
finish_color = 'green'
wall_color = 'black'
sleep_timer = 0.1
test_timer = 0.5

actions = [
	[0, -1], # UP
	[-1, 0], # LEFT
	[0, 1], # DOWN
	[1, 0] # RIGHT
]

class Game:
	def __init__(self, table=(20, 20), spawn=(0, 0), finish=None, max_tries=100):
		self.table = table
		self.spawn = spawn
		if finish:
			self.finish = finish
		else:
			self.finish = (self.table[0] - 1, self.table[1] - 1)
		self.Q_matrix = [[[0	for _ in range(4)]	for _ in range(self.table[0])]	for _ in range(self.table[1])]
		self.position = None
		self.last_position = None		
		
		# Creating visual envirnoment
		self.walls = []
		self.root = tk.Tk()
		self.root.resizable(0, 0) # personal preference
		self.root.title('Q-Learning AI')
		self.button = tk.Button(self.root, text='Finish', command=self.finish_choosing)
		self.canvas = tk.Canvas(self.root, width=2 + self.table[0] * rectangle_size, height=2 + self.table[1] * rectangle_size)
		self.square = [[None	for _ in range(self.table[0])] for _ in range(self.table[1])]
		for i in range(0, self.table[1]):
			for j in range(0, self.table[0]):
				self.square[i][j] = self.canvas.create_rectangle(2 + i * rectangle_size, 2 + j * rectangle_size, 2 + (i + 1) * rectangle_size, 2 + (j + 1) * rectangle_size)
				self.canvas.tag_bind(self.square[i][j], '<Button-1>', lambda event, x = j, y = i: self.set_wall(event, (x, y)))	
		self.canvas.pack()
		self.button.pack()
	
		self.choosing_walls = True
		self.reset()
		while self.choosing_walls:
			self.root.update()

		tries = 0	
		while 1:
			if self.position == None or self.position == self.finish:
				self.reset()
			rand_ch = random.random()
			if rand_ch < epsilon:
				action = int(3 * random.random())
			else:
				action = list(reversed(sorted(enumerate(self.Q_matrix[self.position[1]][self.position[0]]), key=lambda x: x[1])))[0][0]
			self.do_action(action)
			time.sleep(sleep_timer)
			tries += 1
			if tries >= max_tries:
				break

		# Test run
		messagebox.showinfo('Game info', 'It\'s time to check how AI performs.')
		time.sleep(test_timer)
		self.real_run()

		self.root.destroy()

	def finish_choosing(self):
		self.choosing_walls = False
		self.button.pack_forget()

	def set_wall(self, _, pos):
		if pos == self.spawn or pos == self.finish or not self.choosing_walls:
			return
		if pos in self.walls:
			self.walls.remove(pos)
			col = default_color	
		else:
			self.walls.append(pos)
			col = wall_color
		self.canvas.itemconfig(self.square[pos[1]][pos[0]], fill=col)

	def reset(self):
		self.last_position = None
		self.position = self.spawn
		for row in self.square:
			for col in row:
				self.canvas.itemconfig(col, fill=default_color)
		self.canvas.itemconfig(self.square[self.spawn[1]][self.spawn[0]], fill=player_color)
		self.canvas.itemconfig(self.square[self.finish[1]][self.finish[0]], fill=finish_color)
		for wall in self.walls:
			self.canvas.itemconfig(self.square[wall[1]][wall[0]], fill=wall_color)
		self.root.update()	
	
	def change_position(self, new_pos):
		self.last_position = self.position
		self.canvas.itemconfig(self.square[self.last_position[1]][self.last_position[0]], fill=default_color)
		self.position = new_pos
		self.canvas.itemconfig(self.square[self.position[1]][self.position[0]], fill=player_color)
		self.root.update()

	def reward(self, pos):
		if pos[0] not in range(self.table[0]) or pos[1] not in range(self.table[1]) or pos in self.walls:
			return False, - (self.table[0] + self.table[1])
		if pos == self.finish:
			return True, 2 * (self.table[0] + self.table[1])
		return True, -1

	def do_action(self, action):
		pos_ch = actions[action]
		new_pos = (self.position[0] + pos_ch[0], self.position[1] + pos_ch[1])
		alive, r = self.reward(new_pos)
		if alive:		
			self.Q_matrix[self.position[1]][self.position[0]][action] += alpha * (r + gamma * max(self.Q_matrix[new_pos[1]][new_pos[0]]) - self.Q_matrix[self.position[1]][self.position[0]][action]) 
			self.change_position(new_pos)
		else:
			self.Q_matrix[self.position[1]][self.position[0]][action] += alpha * (r - self.Q_matrix[self.position[1]][self.position[0]][action])
			self.reset()

	def real_run(self):
		k = 0
		self.reset()
		time.sleep(test_timer)
		while 1:
			action = list(reversed(sorted(enumerate(self.Q_matrix[self.position[1]][self.position[0]]), key=lambda x: x[1])))[0][0]
			pos_ch = actions[action]
			new_pos = (self.position[0] + pos_ch[0], self.position[1] + pos_ch[1])
			alive, _ = self.reward(new_pos)
			if not alive:
				messagebox.showinfo('Game info', 'AI died.')
				break
			self.change_position(new_pos)
			if self.position == self.finish:
				messagebox.showinfo('Game info', 'AI reached finish successfully.')
				time.sleep(test_timer)
				break
			time.sleep(test_timer)
			if k >= 2 * (self.table[0] + self.table[1]):
				messagebox.showinfo('Game info', 'AI encountered infinity loop.')
				break

def main():
	a = Game(table=(5, 5), max_tries=1000)
	
if __name__ == "__main__":
	main()	
