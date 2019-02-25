import tdl

from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from input_handlers import handle_keys
from map_utils import GameMap, make_map
from render_functions import clear_all, render_all

def main():
	# Defining variables for screen size.
	screen_width = 80;
	screen_height = 50;

	map_width = 80;
	map_height = 50;

	room_max_size = 12;
	room_min_size = 6;
	max_rooms = 30;

	# FIELD OF VIEW Algorithm;
	fov_algorithm = 'BASIC';
	fov_light_walls = True;
	fov_radius = 7;

	max_monsters_per_room = 3;

	colors = {
		'dark_wall' 		: (46, 64, 64),
		'dark_ground' 		: (4, 32, 42),
		'light_wall'		: (199, 207, 198),
		'light_ground'		: (90, 110, 101),
		'desaturated_green' : (221, 226, 218),
		'darker_green' 		: (221, 226, 218)
	};

	player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True);
	entities = [player];

	# We're telling which font to use.
	tdl.set_font('consolas12x12.png', greyscale=True, altLayout=True);

	# Creating screen.
	root_console = tdl.init(screen_width, screen_height, title='Roguelike Tutorial Revised');
	game_console = tdl.Console(screen_width, screen_height);
	game_map = GameMap(map_width, map_height);
	## Generate game map.
	make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, colors);

	fov_recompute = True;

	# Define o primeiro turno do jogo como do PLayer.
	game_state = GameStates.PLAYERS_TURN

	# Game Loop.
	while not tdl.event.is_window_closed():

		if fov_recompute:
			game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls);

		# UPDATE
		render_all(game_console, entities, game_map, fov_recompute, root_console, screen_width, screen_height, colors);

		tdl.flush(); # RENDER SCREEN

		clear_all(game_console, entities)

		fov_recompute = False;

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

		if move and game_state == GameStates.PLAYERS_TURN:
			dx, dy = move;
			destination_x = player.x + dx;
			destination_y = player.y + dy;

			if(game_map.walkable[destination_x, destination_y]):
				target = get_blocking_entities_at_location(entities, destination_x, destination_y);

				if target:
					print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
				else:
					player.move(dx, dy);				
					fov_recompute = True;

				# Após se mover, turno dos inimigos.
				game_state = GameStates.ENEMY_TURN;
			

		if exit:
			return True;

		if fullscreen:
			tdl.set_fullscreen(not tdl.get_fullscreen());
		
		if game_state == GameStates.ENEMY_TURN:
			# for entity in entities:
			# 	if entity != player: # Para cada entidade, tirando jogador.
			# 		# inimigo pondera o significado da sua própria existência
			# 		print('The ' + entity.name + ' ponders the meaning of its existence.');
			# Devolve o turno para o jogador.
			game_state = GameStates.PLAYERS_TURN;


if __name__ == '__main__':
	main();