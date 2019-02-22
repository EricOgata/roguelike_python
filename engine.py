import tdl

from input_handlers import handle_keys

def main():
	print("HELLO WORLD!");
	# Defining variables for screen size.
	screen_width = 80;
	screen_height = 50;

	# PlayerPosition.
	player_x = int(screen_width / 2); # Initial X axis position
	player_y = int(screen_height / 2);	# Initial Y axis position

	# We're telling which font to use.
	tdl.set_font('consolas12x12.png', greyscale=True, altLayout=True);

	# Creating screen.
	root_console = tdl.init(screen_width, screen_height, title='Roguelike Tutorial Revised');
	game_console = tdl.Console(screen_width, screen_height);


	# Game Loop.
	while not tdl.event.is_window_closed():

		# UPDATE
		game_console.draw_char(player_x, player_y, '@', bg=None, fg=(255, 255, 255));
		root_console.blit(game_console, 0, 0, screen_width, screen_height, 0, 0)
		tdl.flush(); # RENDER SCREEN

		game_console.draw_char(player_x, player_y, ' ', bg=None);

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
			player_x += dx;
			player_y += dy;

		if exit:
			return True;

		if fullscreen:
			tdl.set_fullscreen(not tdl.get_fullscreen());


if __name__ == '__main__':
	main();