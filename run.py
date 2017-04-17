from game import Game
from app import Application

def main():
	a = Application()
	data = a.get_info()
	Game(pallete=data['pallete'], table=data['table'], max_tries=data['epochs'])

if __name__ == "__main__":
	main()
