import tdl

from entity import Entity
from input_handlers import handle_keys
from map_utils import make_map
from render_functions import clear_all, render_all

def main():
	# Defining variables for screen size.
	screen_width = 80;
	screen_height = 50;

	map_width = 80;
	map_height = 45;

	room_max_size = 10;
	room_min_size = 6;
	max_rooms = 30;

	colors = {
		'dark_wall' 	: ( 255, 255, 255),
		'dark_ground' 	: ( 0, 0, 0)
	};

	player = Entity(int(screen_width/2), int(screen_height/2), '@', (255, 255, 255));
	# npc = Entity(int(screen_width/2 - 5), int(screen_height/2), '@', (255, 255, 0));

	entities = [player];

	# We're telling which font to use.
	tdl.set_font('consolas12x12.png', greyscale=True, altLayout=True);

	# Creating screen.
	root_console = tdl.init(screen_width, screen_height, title='Roguelike Tutorial Revised');
	game_console = tdl.Console(screen_width, screen_height);
	game_map = tdl.map.Map(map_width, map_height);
	## Generate game map.
	make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player);

	# Game Loop.
	while not tdl.event.is_window_closed():

		# UPDATE
		render_all(
			game_console, 
			entities, 
			game_map, 
			root_console, 
			screen_width, 
			screen_height, 
			colors
		);

		tdl.flush(); # RENDER SCREEN

		clear_all(game_console, entities)

		# CAPTURE EVENTS
		for event in tdl.event.get():
			if event.type == 'KEYDOWN':
				user_input = event;
				break;
		else:
			user_input = None;

		if not user_input: # If user press nothing, do nothing.
			continue;

		action = handle_keys(user_input);

		move = action.get('move');
		exit = action.get('exit');
		fullscreen = action.get('fullscreen');

		if move:
			dx, dy = move;
			if(game_map.walkable[player.x + dx, player.y + dy]):
				player.move(dx, dy);

		if exit:
			return True;

		if fullscreen:
			tdl.set_fullscreen(not tdl.get_fullscreen());


if __name__ == '__main__':
	main();