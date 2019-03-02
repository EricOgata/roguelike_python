import tdl

from components.fighter import Fighter
from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from death_functions import kill_monster, kill_player
from input_handlers import handle_keys
from map_utils import GameMap, make_map
from render_functions import clear_all, render_all, RenderOrder

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
		'dark_wall' 		: (62, 25, 115),
		'dark_ground' 		: (25, 0, 43),
		'light_wall'		: (136, 75, 255),
		'light_ground'		: (95, 0, 115),
		'Orc' 				: (233, 0, 255),
		'Troll' 			: (179, 31, 255),
		'dead_char'			: (136, 75, 255)
	};

	fighter_component = Fighter(hp=30, defense=2, power=5);
	player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component);
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
		render_all(game_console, entities, player, game_map, fov_recompute, root_console, screen_width, screen_height, colors);

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

		player_turn_results = []

		if move and game_state == GameStates.PLAYERS_TURN:
			dx, dy = move;
			destination_x = player.x + dx;
			destination_y = player.y + dy;

			if(game_map.walkable[destination_x, destination_y]):
				target = get_blocking_entities_at_location(entities, destination_x, destination_y);

				if target:
					attack_results = player.fighter.attack(target);
					player_turn_results.extend(attack_results);
				else:
					player.move(dx, dy);				
					fov_recompute = True;

				# Após se mover, turno dos inimigos.
				game_state = GameStates.ENEMY_TURN;
			

		if exit:
			return True;

		if fullscreen:
			tdl.set_fullscreen(not tdl.get_fullscreen());		
		
		for player_turn_result in player_turn_results:
			message = player_turn_result.get('message')
			dead_entity = player_turn_result.get('dead')
			
			if message:
				print(message)
			
			if dead_entity:
				if dead_entity == player:
					message, game_state = kill_player(dead_entity, colors);
				else:
					message = kill_monster(dead_entity, colors)
				print(message)

		if game_state == GameStates.ENEMY_TURN:
			for entity in entities:
				if entity.ai:
					enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

					for enemy_turn_result in enemy_turn_results:
						message = enemy_turn_result.get('message')
						dead_entity = enemy_turn_result.get('dead')

						if message:
							print(message)
						if dead_entity:
							if dead_entity == player:
								message, game_state = kill_player(dead_entity, colors)
							else:
								message = kill_monster(dead_entity, colors)							
							print(message)

							if game_state == GameStates.PLAYER_DEAD:
								break
					if game_state == GameStates.PLAYER_DEAD:
						break;
			else:
				game_state = GameStates.PLAYERS_TURN;


if __name__ == '__main__':
	main();