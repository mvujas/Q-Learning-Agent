import tkinter as tk
from tkinter.colorchooser import *

class Application:
	def __init__(self, canv_dim=(50, 25)):
		self.pallete = {
			'default': 'white',
			'player': 'red',
			'finish': 'green',
			'walls': 'black'
		}
		self.root = tk.Tk()
		self.root.resizable(0, 0)
		self.root.title('Q-Learning AI')

		tk.Label(self.root, text='Choose width of the table:').pack()
		self.widthSV = tk.StringVar()
		self.widthSV.trace("w", lambda name, index, mode, sv=self.widthSV: self.entry_callback(sv))
		self.widthB = tk.Entry(self.root, width=2, textvariable=self.widthSV)
		self.widthB.insert(0, '5')
		self.widthB.pack()

		tk.Label(self.root, text='Choose height of the table:').pack()
		self.heightSV = tk.StringVar()
		self.heightSV.trace("w", lambda name, index, mode, sv=self.heightSV: self.entry_callback(sv))
		self.heightB = tk.Entry(self.root, width=2, textvariable=self.heightSV)
		self.heightB.insert(0, '5')
		self.heightB.pack()


		self.canvas = [None for _ in range(4)]
		self.col = {}
		for i in range(len(self.canvas)):
			self.canvas[i] = tk.Canvas(self.root, width=canv_dim[0], height=canv_dim[1])
			tmp = list(self.pallete)[i]
			self.col[tmp] = self.canvas[i].create_rectangle(0, 0, canv_dim[0] + 1, canv_dim[1] + 1, fill=self.pallete[tmp])
			self.canvas[i].tag_bind(self.col[tmp], '<Button-1>', lambda event, can=i, x=tmp: self.get_color(can, x))
			tk.Label(self.root, text=tmp.title() + ' color').pack()
			self.canvas[i].pack()

		self.button = tk.Button(self.root, text='Finish choosing')
		self.button.bind('<Button-1>', self.quit)
		self.button.pack()
		
		self.root.mainloop()

	def entry_callback(self, StrVar):
		StrVar.set(StrVar.get()[:2])
		
	def quit(self, _):
		self.root.destroy()
	
	def get_color(self, i, item):
		color = tk.colorchooser.askcolor()
		if color[1]:
			self.pallete[item] = color[1]
			self.canvas[i].itemconfig(self.col[item], fill=self.pallete[item])

	def get_info(self):
		return {
			'pallete': self.pallete,
			'table': (int(self.widthSV.get()) if self.widthSV.get().isdigit() else 5, int(self.heightSV.get()) if self.heightSV.get().isdigit() else 5)	
		}
